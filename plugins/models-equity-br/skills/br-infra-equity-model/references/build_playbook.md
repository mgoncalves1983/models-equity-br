# Playbook de construção (modo CONSTRUÇÃO)

## Abas padrão

`LeiaMe | Macro | Historico | Trimestral | Portfolio | Comerc | DRE | Divida | Impostos |
RecebPart | Valuation | Multiplos` — adaptar ao perímetro/chaveamento (ex.: +`Transmissao`,
+`Distribuicao`, +`Eolicas`). Ordem de leitura = ordem das abas. (A antiga aba
`Sensibilidade` foi APOSENTADA — substituída pela `Multiplos`.)

- **LeiaMe**: premissas-chave, decisões metodológicas, changelog de versões, a lista de
  UPSIDE NÃO MODELADO (compensações regulatórias pendentes, correções de recebíveis,
  ecossistemas, visão de preço da companhia acima do LP do modelo) e a lista de ATALHOS
  DECLARADOS (todo segmento projetado sem decomposição por driver, com justificativa).
- **Macro**: IPCA, fator de indexação por ano, datas de fim de ano, datas de meio de ano
  para XNPV, fração do ano corrente, Ke, NTN-B, alíquotas (efetivas por entidade e/ou
  estatutária), alvo de alavancagem. Tudo em nomes definidos.
- **Historico**: anual auditado/reportado (todos os anos confirmados no início), com
  eventos do ano nos comentários e reconciliação do EBITDA ajustado.
- **Trimestral**: ver seção própria abaixo (versão enriquecida).
- **Portfolio**: um bloco por cluster (usinas com mesmo vencimento/regime), com inputs
  estruturais (GF, vencimento, contratação) e o FCFF do cluster; inclui cluster de
  receita de potência/LRCAP quando houver.
- **DRE**: histórico + projeção nas mesmas linhas (ver Calibração).
- **Divida**: cronograma REAL de amortização da DF/release (nunca % genérico), custo por
  indexador (mix IPCA/CDI/TJLP + spread), resultado financeiro, e o bloco de POLÍTICA DE
  DIVIDENDOS por alavancagem (ver seção própria).
- **Valuation**: SOTP por cluster + bridge + TIR implícita do FCFE + TIR do DDM.
- **Multiplos**: ver seção própria abaixo.

## Padrões técnicos (openpyxl)

- **Scripts numerados e determinísticos** (`build_part1.py` … `build_partN.py`): o modelo
  inteiro deve ser reproduzível rodando-os em sequência. Nunca editar o arquivo "na mão"
  sem registrar no script. A ordem IMPORTA — documentar no cabeçalho de cada script.
- Helper de colunas único (`helpers_template.py`): grade anual com `col(ano)`; se uma aba
  tiver grade deslocada (ex.: DRE com colunas históricas extras), criar um `colX()`
  próprio e NUNCA misturar.
- **PROIBIDO `insert_cols`/`insert_rows` em grade viva**: openpyxl desloca células mas NÃO
  reescreve fórmulas. Para mudar a grade de uma aba: deletar a aba, recriá-la inteira e
  reapontar TODAS as referências externas a ela (grep pelas refs antes).
- Funções modernas SEM prefixo `_xlfn` (escrever `=XIRR(...)`, `=XNPV(...)` — o prefixo
  quebra no LibreOffice/recalc).
- Recalcular via LibreOffice headless e exigir **zero erros de fórmula** antes de
  qualquer entrega (usar `scripts/verify_model.py`).
- Células-check com fundo amarelo: diferenças que devem ser ~0 (calibração), memos de
  sanidade (projeção vs run-rate), coerência TIR↔SOTP.
- ATENÇÃO a arquivos com histórico de corrupção por recálculo (caso ISAE4): se o usuário
  avisar, edições só via XML cirúrgico/openpyxl, NUNCA recalc LibreOffice no arquivo.

## Calibração histórica (o teste da estrutura)

1. Histórico nas MESMAS linhas da projeção (colunas `2023A | 2024A | 2025A | 2026E…`).
2. Ano com M&A relevante → coluna **proforma** (rotular "A pf"), auditado preservado na
   aba Historico com comentário citando os dois números.
3. **DOIS bridges obrigatórios, distintos e ambos nas abas Historico E Trimestral**:
   (i) soma dos segmentos → consolidado ("plug de holding/eliminações documentado");
   (ii) reportado → RECORRENTE — para EBITDA **e lucro líquido** (com IR sobre os
   ajustes), a partir da tabela de reconciliação oficial do release (MtM, litígios,
   não recorrentes, indenizações, baixas, VNR, equivalência). Plug sem explicação =
   estrutura mal mapeada. ATENÇÃO: a definição de "ajustado/recorrente" das companhias
   MUDA entre anos (caso Copel: 2022/23 incluíam equivalência; 2024/25 excluem) —
   anotar o rótulo de cada ano. **VNR: nunca no recorrente, nunca caixa** (regra de
   ouro do SKILL.md) — reportado fica como linha de referência; alavancagem, política
   de dividendos e ND/EBITDA do Multiplos SEMPRE sobre o recorrente ex-VNR.
   **Base do recorrente divulgado — verificar minoritários**: checar no bridge do
   release se o LL ajustado/recorrente parte do lucro CONSOLIDADO (antes de
   minoritários) ou do atribuído aos controladores — há companhias cujo recorrente
   oficial embute a fatia dos minoritários (~20% num caso real), inflando P/E
   recorrente, payout e DPS calculados direto sobre o número divulgado. Reportar
   SEMPRE também o "recorrente atribuível ao controlador"; atenção a mudança de
   perímetro na linha de minoritários (recompra de quasi-equity derruba a linha sem
   melhora recorrente).
4. Linhas do histórico em azul (inputs) com fonte no comentário; subtotais em fórmula.
5. Memo de sanidade: projeção do 1º ano vs último trimestre anualizado, com explicação da
   diferença (sazonalidade, GSF, eventos, degrau tarifário).
6. Distribuição: bloco de calibração adicional obrigatório (motor vs recorrente ex-VNR —
   ver segment_modules).

## Aba Trimestral (versão enriquecida — OBRIGATÓRIA, não "melhor esforço")

A cascata completa e os blocos abaixo são ENTREGÁVEL PADRÃO com as MESMAS quebras da
aba Historico — entregar versão "mínima" (só ROL/EBITDA/LL) é erro, não pendência.

- Colunas: 4-5 trimestres realizados + trimestres do ano corrente em branco (para
  preencher a cada resultado) + "ano-corrente E do modelo /4" (verde) + "último tri /
  modelo" (%).
- **DRE em cascata** (tudo soma até o lucro): ROL → custos não gerenciáveis (energia
  comprada, encargos de rede, insumos, custo de construção) → LUCRO BRUTO (proxy — a
  DRE CVM é por natureza; comentar) → EBITDA → D&A → EBIT → resultado financeiro → EBT →
  IR → lucro continuidade → descontinuadas → lucro total. EBIT/EBT/lucros como FÓRMULAS
  encadeadas + check por tri contra a linha de lucro do CVM.
- **Operacionais SEM lacunas** — buscar no release do PRÓPRIO trimestre (abrir um a um;
  não há atalho): EBITDA recorrente (com check Σ4 tris = FY recorrente), DL ajustada
  divulgada, ND/EBITDA, capex do tri, GSF, curtailment por fonte, PLD médio, modulação,
  provisões de ressarcimento. Registrar divergências INTERNAS dos releases (ex.: dois
  valores de curtailment no mesmo doc; reapresentações no release seguinte) e dados
  só-em-gráfico (marcar valor inferido como DERIVADO).
- **Acompanhamento de caixa por trimestre** (primeira verificação de geração do PM):
  DL do BP CVM fim do tri → Δ DL → dividendos/JCP PAGOS (do DFC; tri = YTD t − YTD t−1,
  marcar derivação) → aquisições/outorga pagas (DFC: "aquisição de investimentos" +
  "aquisições de controladas, efeito caixa") → alienações recebidas → **geração de
  caixa (= −ΔDL − dividendos pagos)** → **geração AJUSTADA ex-M&A**. Sem a linha de
  M&A a geração "desaba" em tri de aquisição e engana (lição Copel 2T25: Baixo Iguaçu).
- Validação obrigatória: soma dos 4 tris = FY exato (ROL, EBITDA, lucro, recorrente).
- Nota de vintage: registrar quando cada abertura começou a ser divulgada.

## Aba Multiplos (substituiu a Sensibilidade) — template em assets/example_multiples.xlsx

- Grade anual longa: histórico + projeção nas mesmas colunas; coluna de CAGR (ex.:
  último A / A+5) à direita.
- Bloco DRE resumida: Revenues, EBITDA, D&A, EBIT, Interest expense, EBT (=EBIT+juros),
  Taxes, Net Profit — hist em azul (CVM), projeção linkada (verde) à aba DRE.
- Bloco EBITDA por segmento + variações a/a; bloco MARGINS (net, EBITDA, tax bracket).
- Bloco MULTIPLES: **Closing price de cada ano histórico (input azul, fechamento do
  ano)** e nº de ações por ano; mkt cap; EV/EBITDA e P/E históricos a preço do
  fechamento DO ANO e projetados a preço CORRENTE (nomes definidos `price`/`shares`);
  P/B via BPS.
- Bloco retorno: NOPAT, Invested Capital, Net Debt (hist ajustada dos releases; proj da
  aba Divida), FCF/FCFE, ROE, ROIC, FCF yield, ND/EBITDA.
- Bloco dividendos: Payout, Dividend yield, Dividends (pagos, DFC) e "Dividends for the
  year" (declarados sobre o exercício), DPS, BPS.
- Bloco FCF (padrão do template): **FCFF (ex-indenizações terminais)**, **FCFE**,
  FCF yield = FCFE/market cap e FCFF yield = FCFF/EV; histórico DERIVADO como input
  azul com a derivação no comentário (FCFF = EBITDA recorrente − IR caixa − capex;
  FCFE = FCFF − juros pós-IR + ΔDL).
- ND/EBITDA do Multiplos: sobre EBITDA RECORRENTE (nunca o reportado com VNR).

## Alavancagem — TRÊS VISÕES OBRIGATÓRIAS na aba dedicada

Nunca uma só. As três, lado a lado, com bridge quantificado entre elas:

1. **Analítica** (a que o PM olha): TODAS as dívidas — inclusive instrumentos
   quase-dívida que a companhia classifica em patrimônio (preferenciais resgatáveis sem
   put do minoritário), passivos negociados a desembolsar (acordos tributários) e
   aquisições liquidadas DEPOIS da data-base do balanço. EBITDA recorrente ex-VNR,
   ex-equivalências, líquido de holding e eliminações.
2. **Visão da companhia**: como ela divulga no release, reconstruída linha a linha.
3. **Visão covenant**, quando diferente da anterior, com o **limite contratual das
   escrituras** ao lado (nota de dívida da DFP traz o índice apurado por controlada).

**A diferença entre as visões pode passar de 1,5x, e boa parte dela evapora sozinha.**
Ganho de capital de venda de ativo e EBITDA do ativo vendido saem da janela de 12 meses
sem nada operacional acontecer. Num caso real isso valia 0,76x, e a companhia já publicava
a versão ex-ganho justamente por isso. Decompor no bridge item a item.

Assimetria frequente do covenant: a companhia SOMA a equivalência patrimonial de
participações ao EBITDA mas NÃO soma a dívida que financiou a compra. Não é irregular —
a escritura define assim — mas registrar.

## Dívida e política de dividendos — dividendo é a POLÍTICA; a DL é a RESULTANTE

- Cronograma REAL de amortização (nota de empréstimos/debêntures do ITR mais recente);
  "após 20XX" distribuído linearmente com pendência declarada; custo por indexador.
- **Arquitetura padrão (jul/2026)** — nunca o contrário (DL-alvo gerando dividendo
  mecânico):
  - `dividendo(t) = MAX( payout_min × LL(t) ; FCFE_antes_div(t) + alvo × EBITDA_rec(t)
    − DL(t−1) )`, com piso zero. `payout_min` = política divulgada da companhia
    (inclusive sobre "lucro caixa"/LL ex-VNR; default sem política: 40%; mínimo legal
    25%, art. 202 da 6.404 — JCP conta; base = LL ajustado). O 2º termo é o *sweep*
    que distribui o excedente mantendo a DL no alvo (alvo: divulgado; senão ND/EBITDA
    atual se ≤ 3,5x, ou 3,5x com convergência em 3 anos).
  - `DL(t) = DL(t−1) − FCFE_antes_div(t) + dividendo(t)` — roll-forward; **ND/EBITDA
    vira OUTPUT** (células-check amarelas vs banda e vs covenant), não input.
  - **Juros sobre a DL de ABERTURA (t−1)** — mata a circularidade
    dividendo→DL→juros→LL→dividendo sem cálculo iterativo (que o gate de recálculo não
    tolera). Declarar a convenção.
  - Consequência: **FCFE ≡ dividendo por construção** → TIR FCFE e TIR DDM colapsam
    numa só (reportar as duas linhas com a nota).
  - Comportamento esperado: no pico de capex o piso de payout manda e a alavancagem
    PASSA do alvo (realista — companhias alavancam para sustentar payout); a
    convergência é endógena via sweep.
  - Escudo de juros na alíquota EFETIVA consolidada se o modelo usa efetivas (nunca
    34% — dobraria o JCP).
- **Custo da dívida projetado — calibração**: calibrar o resultado financeiro projetado
  contra o reportado em **>= 2 anos, expurgando MtM de derivativos** (um ano só engana:
  caso real deu fator 0,70x CDI num ano com ganho de MtM de ~R$ 1 bi vs 0,80x no ano
  limpo). Preferir DECOMPOR a usar fator único: (i) juros líquidos ao custo bruto
  divulgado (% do CDI) sobre a DL; (ii) linha separada de receitas financeiras
  RECORRENTES (acréscimos moratórios, atualização de ativos regulatórios), indexada;
  (iii) juros capitalizados em obras como redutor explícito ligado ao capex. Lembrete:
  o SOTP (FCFF a Ke) é INVARIANTE a esse fator — ele só move TIR, LL, payout e covenant.
- **Circuito de impostos no FCFE — duas pernas, sem linha extra**: (1) IR operacional
  DENTRO do FCFF de cada cluster (efetiva × MAX(0; EBITDA − D&A fiscal)); (2) escudo
  dos juros colado no próprio juro (juros × (1 − efetiva consolidada)). NÃO criar linha
  de "IR pago" na aba de dívida — dupla contagem. Caveats a declarar sempre: ver a
  seção de impostos do segment_modules.
- **Reconciliar SEMPRE o payout implícito do modelo vs o histórico/anúncios da
  companhia** e comentar a diferença (capacidade de dívida para crescimento, pico de
  capex, mínimo estatutário). Distinguir e ROTULAR os dois critérios de alavancagem:
  covenant oficial (ex.: pro forma proporcional com JVs, mútuos, TVM) vs analítico
  (recorrente ex-VNR) — qual está no alvo da política.

### Política com TRÊS parâmetros (piso, teto e sweep)

`dividendo = MIN( teto × LL ; MAX( piso × LL ; sweep ) )` — os três azuis e editáveis
ano a ano.

- **Piso**: dividendo obrigatório estatutário. **Default 25%** (art. 202 da Lei 6.404,
  JCP conta), mas **VERIFICAR O ESTATUTO**: a lei permite fixar abaixo de 25% desde que
  definido com precisão e sem sujeitar ao arbítrio dos administradores, e há companhia em
  ciclo pesado de capex operando com 1%.
- **Sweep**: `FCFE antes de dividendo + alvo × EBITDA − dívida líquida de abertura`.
  Testado POR ENTIDADE quando há múltiplas concessionárias.
- **Teto**: percentual máximo do lucro. **Sem teto o sweep leva a companhia a se
  realavancar para distribuir indefinidamente** — o EBITDA crescendo cria capacidade de
  dívida nova e o sweep manda devolvê-la. Payout de 148% em caso real. Ancorar no payout
  histórico da própria companhia.
- Nota contraintuitiva: teto BAIXO retém mais e desalavanca mais rápido; teto baixo
  perpétuo faz a alavancagem furar PARA BAIXO do alvo. Subir o teto na maturidade deixa o
  sweep SEGURAR no alvo.
- Cuidado: se o "lucro" da base incluir equivalência patrimonial de participações
  marcadas a mercado, o teto fica frouxo — está calibrado sobre resultado que não gera
  caixa no fluxo. Declarar ou usar lucro da operação.

### ANTI-PADRÃO — trava de alavancagem com caixa paralelo na holding

**NÃO construir.** Conta de caixa na holding que reduz a dívida líquida consolidada sem
amortizar dívida nas entidades é aproximação aceitável enquanto é pequena e **se
contradiz quando fica grande** (indenizações, venda de ativo). Erros reais gerados numa
única sessão: duplo cômputo do caixa nos dois lados do teste, vaivém de dezenas de bilhões
de dívida líquida entre anos consecutivos, e aporte artificial de R$ 143 bn no vencimento
das concessões.

Se precisar de restrição de financiamento, duas saídas honestas: (a) reescrever o
roll-forward de dívida das entidades para receber amortização da holding; ou (b) deixar a
alavancagem como LEITURA na aba dedicada, sem realimentar o fluxo, e avisar no LeiaMe que
o modelo não impõe restrição de financiamento.

Regra de processo: **se duas correções seguidas geraram efeito colateral novo, o defeito é
de arquitetura** — parar e reavaliar em vez de corrigir o sintoma.

## Bridge do SOTP — checklist completo (nenhum item pode faltar)

1. **Dívida líquida do ÚLTIMO trimestre divulgado** (nunca referência congelada).
2. **UBP/concessões a pagar**: se a receita correspondente está no fluxo, deduzir o
   estoque. Lei 15.235/2025 permitiu repactuação (pagamento único a VP com desconto;
   24 de 34 geradoras aderiram em 2026) — verificar adesão: se aderiu, deduzir o
   pagamento único e ZERAR o fluxo de UBP.
3. **Minoritários a book value** (decisão do autor — não capitalizar lucros; anotar o
   viés; book NEGATIVO soma). Recomendar abrir SPE por SPE quando material; atenção a
   ações preferenciais com dividendo prioritário.
   **Quasi-equity em subsidiárias** (PNs bancárias em holdings intermediárias, ex.:
   estrutura EPNE/banco): no SOTP deduzir a BOOK; **no fluxo da TIR tratar como SALDO
   DEVEDOR**: `saldo(t) = saldo(t−1) × (1 + CDI + spread) − pagamento(t)`, com
   pagamento = % econômico do banco × fluxo do cluster (piso zero), até extinção —
   quando o saldo zera, o vazamento MORRE e 100% do cluster (inclusive indenização
   terminal) volta ao acionista. Spread default CDI+1%; saldo inicial = book do
   minoritário (proxy — strike da call raramente é público; declarar). Isso torna
   NPV(fluxo) ≈ book e restaura a coerência TIR↔SOTP (vazamento % perpétuo
   superestima a dedução).
4. **Déficit previdenciário (CPC33)**: endêmico em utilities com legado estatal (CESP,
   Eletrobras, Copel, Cemig). Deduzir o estoque contábil; NO SOTP não duplicar com as
   contribuições no fluxo; NA TIR (FCFE) entram os desembolsos — são cálculos separados
   e ambos corretos.
5. **Provisões de litígios com perda PROVÁVEL**: deduzir o estoque (líquido de ativos de
   indenização vinculados, ex.: garantias de vendedor em M&A); perdas possíveis ficam
   FORA, listadas como risco com o valor.
6. **Estoque de provisões de ressarcimento/curtailment** (renováveis, pós-2023): vive no
   BP, não na DRE — deduzir; o fluxo futuro de provisões é linha própria da projeção.
   Recebível de compensação JÁ RECONHECIDO (Lei 15.269/2025): somar.
7. **MtM de contratos de energia**: memo NÃO somado (dupla contagem com o runoff do book).
8. **Prejuízo fiscal**: NPV do cronograma de realização divulgado, como ativo separado,
   com caveat de realizabilidade por entidade no comentário.
9. **Participações relevantes**: marcar em transação real recente quando existir; senão
   NPV do fluxo de dividendos calibrado no ANO CHEIO (nunca trimestre anualizado).
10. **Arrendamentos (IFRS16)** se estiverem fora da DL ajustada divulgada: deduzir.
11. **Capex por segmento sem dupla contagem** (capex de transmissão dentro do FCFF de
    geração E deduzido de novo no NPV de transmissão = erro clássico).

## Valuation e TIR

### O número principal é VPL(FCFE @ Ke), não o SOTP

O SOTP desconta **FCFF (fluxo desalavancado) ao Ke** e deduz a dívida a **valor de face**.
Quando Kd < Ke isso **descarta o benefício do endividamento**, e com alavancagem alta a
diferença passa de 20% do equity (caso real: R$ 22,3 bn, ou R$ 17,75/ação).

O modelo já constrói um FCFE completo, com roll-forward de dívida por entidade e serviço
da dívida explícito. **VPL desse FCFE ao Ke É o valor do equity**, direto: sem problema de
pesos, sem supor estrutura de capital constante, com o escudo fiscal já no fluxo pela
alíquota de cada entidade. O SOTP vira **atribuição de valor por ativo**.

**Não usar WACC** quando a alavancagem varia no horizonte — WACC pressupõe estrutura de
capital fixa. Se precisar de rigor formal com alavancagem variável: APV (valor
desalavancado ao Ku + VP dos escudos fiscais sobre a trajetória de dívida que o modelo já
calcula). Atenção ao efeito cruzado: alíquota efetiva baixa (SUDAM/SUDENE) REDUZ o
benefício da alavancagem — os dois incentivos competem pela mesma base.

Reportar as duas medidas com a diferença rotulada como "benefício da alavancagem
descartado pelo SOTP". O check de coerência TIR ↔ upside passa pelo FCFE por construção;
pelo SOTP pode falhar legitimamente.

### FCFE yield — linha padrão da aba Valuation

Definição do autor, obrigatória em todo modelo:

```
FCFE       = dividendos pagos − Δ dívida líquida        (+ aporte como fluxo negativo)
FCFE yield = FCFE / market cap
```

É a geração de caixa real para o acionista, independente de ter sido distribuída ou usada
para desalavancar. Muito mais informativa que o dividend yield em companhia com payout
suprimido: com piso de 1%, o DY mostra quase zero enquanto o FCFE yield revela a
realidade — frequentemente NEGATIVA nos anos de capex pesado. Usar a **dívida líquida
analítica** (visão 1 acima).

- SOTP: XNPV por cluster a Ke, fluxos com datas reais (ano corrente fracionado pela
  fração já decorrida; demais em meio de ano).
- **Runoff + indenização como base** (terminal zero no fim de concessão/autorização,
  com a indenização de ativos não amortizados como recebível na data — distribuição:
  RAB líquida integral; transmissão: blindada por laudo, default zero declarado) +
  cenário de renovação: valor da extensão como anuidade crescente a IPCA, descontada a
  Ke, vezes (1 − régua de outorga). Na DISTRIBUIÇÃO, renovar = manter o FCFF e ABRIR MÃO
  da indenização (descontá-la do valor da extensão). Expor: régua 0% = grátis; 100% =
  NPV zero ≡ runoff; e o **"% do valor da extensão embutido na tela"** = (tela×ações −
  equity runoff) / valor da extensão — é o output de tese mais poderoso do método.
- **TIR implícita na tela**: XIRR do fluxo FCFE ao acionista com investimento =
  −tela×ações. O FCFE deve deduzir serviço da dívida (juros pós-IR − Δ dívida da
  política) E os desembolsos das obrigações deduzidas no bridge (ressarcimento,
  litígios, contribuições previdenciárias, pagamento único de UBP).
- **TIR do DDM**: XIRR do fluxo de DIVIDENDOS da política com investimento =
  −tela×ações. Na arquitetura padrão (dividendo = política, DL = resultante), FCFE ≡
  dividendo por construção e as duas TIRs COLAPSAM numa só — manter as duas linhas com
  a nota explicando a equivalência.
- **Perpetuidade/anuidade de renovação: NUNCA ancorar em ano de transição/expiração**
  (runoff distorce o FCFE final com ΔND gigante) — usar FCFF normalizado de um ano
  intermediário limpo, projetado a IPCA, e DECLARAR qual ano foi usado.
- No fluxo final da TIR (FCFE), LIQUIDAR a dívida líquida remanescente no último ano
  do horizonte (senão o acionista "fica" com a dívida sem pagá-la).
- **Check de coerência obrigatório**: upside < 0 ⇒ TIR < Ke (e vice-versa). Se não
  fechar, há inconsistência entre bridge e fluxo — encontrar; se não resolver, LISTAR o
  motivo na entrega. CAVEAT ESTRUTURAL: com |upside| < ~5% e alavancagem alta, o check
  por sinal falha por construção (o FCFE captura o valor do spread da dívida que o SOTP
  a Ke puro não dá) — usar tolerância e comparar a TIR com o Ke BLENDED (ajustado pelo
  mix dívida/equity), documentando no LeiaMe.
- Conclusão SEMPRE na régua: TIR real (Fisher) vs NTN-B longa, com spread em p.p.
  Se Ke real (Fisher) < NTN-B real, ALERTAR em destaque no LeiaMe e na entrega (upside
  positivo pode ainda perder da NTN-B).

## Armadilhas de execução (openpyxl/ambiente — lições de campo)

- **Scripts >150 linhas: NUNCA editar trecho via ferramenta de edição direta** (trunca a
  cauda do arquivo — perdeu-se até `wb.save()` em casos reais). Editar via patch
  python ancorado (`str.replace` numa linha única e inequívoca). Após QUALQUER edição:
  `ast.parse` + `grep wb.save` + rodar a sequência build_part1..N COMPLETA do zero.
- **XIRR exige arrays contíguos**: a grade anual (uma coluna por ano com colunas
  históricas no meio) não serve direto — montar bloco espelho contíguo (ex.: B..AI)
  com datas e fluxos dedicados ao XIRR.
- **PDF grande**: NUNCA ler o arquivo inteiro no contexto — converter com
  `pdftotext -layout` para um arquivo temporário e processar em disco com python/regex
  por janelas.
- **Arquivo entregável aberto no Excel do usuário = PermissionError ao regravar**:
  fazer o build em diretório temporário + cópia final, e avisar o usuário para fechar
  o arquivo antes da substituição.

## Entrega

Excel + resumo com: TP runoff, TP renovação (régua), % da extensão na tela, TIR real
FCFE e TIR real DDM com spread vs NTN-B, reconciliação quantificada vs premissas do
usuário (R$/ação por item), upside não modelado, atalhos declarados (regra anti-atalho)
e pendências declaradas (o que não foi lido/feito e por quê).
Opiniões rotuladas como opinião.
