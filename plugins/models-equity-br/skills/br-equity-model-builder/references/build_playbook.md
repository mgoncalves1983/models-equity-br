# Playbook de construção (modo CONSTRUÇÃO)

## Abas padrão

`LeiaMe | Macro | Historico | Trimestral | <uma aba por segmento> | DRE | Divida |
Impostos | Participacoes | Valuation | Multiplos` — adaptar ao perímetro da empresa.
Ordem de leitura = ordem das abas.

- **LeiaMe**: premissas-chave, decisões metodológicas, changelog, lista de UPSIDE NÃO
  MODELADO e lista de ATALHOS DECLARADOS (todo segmento projetado por inflação em vez
  de driver, com a justificativa).
- **Macro**: IPCA, fator de indexação por ano, datas de fim/meio de ano para XNPV,
  fração do ano corrente, Ke, NTN-B, alíquotas, alvo de alavancagem, g da perpetuidade.
  Tudo em nomes definidos.
- **Historico**: anual auditado/reportado, eventos do ano nos comentários, e os DOIS
  bridges (ver Calibração).
- **Trimestral**: ver seção própria (obrigatória, não "melhor esforço").
- **Abas de segmento**: um bloco por linha de negócio com o DRIVER de projeção
  acordado com o usuário (volume x preço x margem; lojas x maturação; carteira x
  spread; produção x custo caixa; etc.), calibrado no histórico, gerando receita,
  EBITDA e FCFF do segmento.
- **DRE**: histórico + projeção nas mesmas linhas.
- **Divida**: cronograma REAL de amortização (nunca % genérico), custo por indexador,
  resultado financeiro, e o bloco de política de dividendos (ver seção própria).
- **Participacoes**: equivalência patrimonial — NPV do fluxo de dividendos calibrado no
  ANO CHEIO (nunca trimestre anualizado), ou marcação em transação real recente.
- **Valuation**: DCF por segmento (ou consolidado) + bridge + TIRs.
- **Multiplos**: ver seção própria.

## Padrões técnicos (openpyxl)

- **Scripts numerados e determinísticos** (`build_part1.py` … `build_partN.py`): o
  modelo inteiro reproduzível rodando-os em sequência. A ordem IMPORTA.
- Helper de colunas único (`helpers_template.py`); grade deslocada = `colX()` próprio,
  NUNCA misturar.
- **PROIBIDO `insert_cols`/`insert_rows` em grade viva** (openpyxl não reescreve
  fórmulas): deletar a aba, recriar inteira e reapontar referências externas.
- Funções modernas SEM prefixo `_xlfn` (`=XIRR(...)`, `=XNPV(...)`).
- Recalcular via LibreOffice headless e exigir **zero erros de fórmula** antes de
  qualquer entrega (`scripts/verify_model.py`).
- Células-check com fundo amarelo: calibração ~0, memos de sanidade, coerência.

## Calibração histórica (o teste da estrutura)

1. Histórico nas MESMAS linhas da projeção (`2023A | 2024A | 2025A | 2026E…`).
2. Ano com M&A relevante → coluna **proforma** ("A pf"), auditado preservado.
3. **DOIS bridges obrigatórios (Historico E Trimestral)**: (i) soma dos segmentos →
   consolidado (plug de holding/eliminações documentado); (ii) reportado → RECORRENTE
   para EBITDA **e lucro líquido** (com IR sobre os ajustes), a partir da tabela de
   reconciliação oficial do release. **Expurgar do recorrente os itens não recorrentes
   e NÃO-CAIXA** (equivalência, MtM/valor justo, baixas, provisões extraordinárias,
   atualizações contábeis de ativos) QUANDO identificáveis; o reportado fica como
   linha de referência. Plug sem explicação = estrutura mal mapeada. A definição de
   "ajustado/recorrente" das companhias MUDA entre anos — anotar o rótulo de cada ano.
   **Verificar a base do recorrente divulgado**: consolidado (antes de minoritários)
   ou atribuível aos controladores? Reportar SEMPRE também o atribuível (P/E, payout e
   DPS sobre o consolidado saem inflados); atenção a mudança de perímetro na linha de
   minoritários.
4. Linhas do histórico em azul (inputs) com fonte no comentário; subtotais em fórmula.
5. Memo de sanidade: projeção do 1º ano vs último trimestre anualizado, com explicação
   (sazonalidade, eventos, preços).

## Aba Trimestral (versão enriquecida — OBRIGATÓRIA)

Cascata completa com as MESMAS quebras da aba Historico — versão "mínima" é erro.

- Colunas: 4-5 trimestres realizados + trimestres do ano corrente em branco +
  "ano-corrente E do modelo /4" (verde) + "último tri / modelo" (%).
- **DRE em cascata** (tudo soma até o lucro): ROL → custos → LUCRO BRUTO → EBITDA →
  D&A → EBIT → resultado financeiro → EBT → IR → lucro continuidade → descontinuadas →
  lucro total. Subtotais como FÓRMULAS encadeadas + check por tri contra a linha de
  lucro reportada.
- **Operacionais SEM lacunas** — do release do PRÓPRIO trimestre (abrir um a um):
  EBITDA recorrente (check Σ4 tris = FY recorrente), DL divulgada, ND/EBITDA, capex do
  tri, KPIs operacionais do setor (SSS, volumes, carteira, ocupação...). Registrar
  divergências internas dos releases e dados só-em-gráfico (marcar como DERIVADO).
- **Acompanhamento de caixa por trimestre** (primeira verificação de geração do PM):
  DL do BP fim do tri → Δ DL → dividendos/JCP PAGOS (DFC; tri = YTD t − YTD t−1) →
  aquisições/M&A pagas → alienações recebidas → **geração de caixa (= −ΔDL −
  dividendos pagos)** → **geração AJUSTADA ex-M&A**. Sem a linha de M&A a geração
  "desaba" em tri de aquisição e engana.
- Validação: soma dos 4 tris = FY exato (ROL, EBITDA, lucro, recorrente).

## Aba Multiplos — template em assets/example_multiples.xlsx

- Grade anual longa: histórico + projeção nas mesmas colunas; coluna de CAGR à direita.
- DRE resumida (Revenues, EBITDA, D&A, EBIT, Interest, EBT, Taxes, Net Profit) — hist
  azul, projeção linkada (verde) à DRE; EBITDA por segmento + variações a/a; margens.
- MULTIPLES: **closing price de cada ano histórico (azul)** e nº de ações por ano;
  EV/EBITDA e P/E históricos a preço do fechamento DO ANO e projetados a preço CORRENTE
  (nomes `price`/`shares`); P/B via BPS. Ajustar preços/ações por desdobramentos.
- Retorno: NOPAT, Net Debt, ROE, ROIC, ND/EBITDA (sobre RECORRENTE).
- Dividendos: payout, DY, dividends pagos (DFC) e declarados no exercício, DPS, BPS.
- Bloco FCF: **FCFF**, **FCFE**, FCF yield = FCFE/mkt cap, FCFF yield = FCFF/EV;
  histórico derivado como input azul com a derivação no comentário
  (FCFF = EBITDA recorrente − IR caixa − capex; FCFE = FCFF − juros pós-IR + ΔDL).

## Dívida e política de dividendos — dividendo é a POLÍTICA; a DL é a RESULTANTE

- Cronograma REAL de amortização (nota do ITR mais recente); "após 20XX" distribuído
  linearmente com pendência declarada; custo por indexador.
- **Arquitetura padrão** — nunca o contrário (DL-alvo gerando dividendo mecânico):
  - `dividendo(t) = MAX( payout_min × LL(t) ; FCFE_antes_div(t) + alvo × EBITDA_rec(t)
    − DL(t−1) )`, piso zero. `payout_min` = política divulgada da companhia; **default
    sem política: 25% (mínimo legal, art. 202 da Lei 6.404; JCP conta; base = LL
    ajustado)**. O 2º termo é o *sweep* que mantém a DL no alvo (alvo: divulgado;
    senão ND/EBITDA atual se ≤ 3,5x, ou 3,5x com convergência em 3 anos).
  - `DL(t) = DL(t−1) − FCFE_antes_div(t) + dividendo(t)` — roll-forward; **ND/EBITDA
    vira OUTPUT** (checks amarelos vs banda e vs covenant), não input.
  - **Juros sobre a DL de ABERTURA (t−1)** — mata a circularidade sem cálculo
    iterativo. Declarar a convenção.
  - Consequência: **FCFE ≡ dividendo por construção** → TIR FCFE e TIR DDM colapsam
    numa só (reportar as duas linhas com a nota).
  - No pico de capex o piso de payout manda e a alavancagem PASSA do alvo (realista);
    a convergência é endógena via sweep.
- **Custo da dívida projetado**: calibrar contra o reportado em **>= 2 anos, expurgando
  MtM de derivativos** (um ano só engana). Preferir DECOMPOR a fator único: (i) juros
  ao custo bruto divulgado (% do CDI) sobre a DL; (ii) receitas financeiras
  RECORRENTES em linha separada, indexada; (iii) juros capitalizados ligados ao capex.
  O valuation por FCFF a Ke é INVARIANTE a esse fator — ele move TIR, LL e payout.
- **Circuito de impostos no FCFE — duas pernas, sem linha extra**: (1) IR operacional
  DENTRO do FCFF de cada segmento (alíquota × MAX(0; EBITDA − D&A fiscal)); (2) escudo
  dos juros colado no próprio juro (juros × (1 − alíquota consolidada)). NÃO criar
  linha de "IR pago" na aba de dívida — dupla contagem. Caveats a declarar: D&A fiscal
  proxy pode superestimar IR em ciclo de capex pesado (conservador); sem consolidação
  fiscal no BR, o escudo real depende de ONDE está a dívida (holding sem lucro
  tributável → escudo diferido via prejuízo fiscal com trava de 30%); se o NPV do DTA
  entra no bridge, o fluxo da TIR idealmente recebe o cronograma de realização.
- **Reconciliar SEMPRE o payout implícito vs o histórico/anúncios da companhia** e
  comentar a diferença. Rotular o critério de alavancagem: covenant oficial vs
  analítico (recorrente) — qual está no alvo.

## Bridge do valuation — checklist (nenhum item pode faltar)

1. **Dívida líquida do ÚLTIMO trimestre divulgado** (nunca referência congelada).
2. **Minoritários a book value** (não capitalizar lucros; anotar o viés; book NEGATIVO
   soma). Abrir por controlada quando material. **Quasi-equity** (PNs bancárias em
   holdings intermediárias): book no SOTP; no fluxo da TIR tratar como SALDO DEVEDOR —
   `saldo(t) = saldo(t−1) × (1 + CDI + spread) − pagamento(t)` (pagamento = % econômico
   × fluxo, piso zero) até extinção; spread default CDI+1%; saldo inicial = book
   (proxy; declarar).
3. **Déficit previdenciário (CPC33)**: deduzir o estoque; NO valuation não duplicar com
   contribuições no fluxo; NA TIR entram os desembolsos — cálculos separados, ambos
   corretos.
4. **Provisões de litígios com perda PROVÁVEL**: deduzir o estoque (líquido de ativos
   de indenização vinculados); perdas possíveis FORA, listadas como risco.
5. **MtM de contratos**: memo NÃO somado (dupla contagem com o fluxo).
6. **Prejuízo fiscal**: NPV do cronograma de realização divulgado, ativo separado,
   caveat de realizabilidade por entidade.
7. **Participações relevantes**: transação real recente quando existir; senão NPV de
   dividendos calibrado no ANO CHEIO.
8. **Arrendamentos (IFRS16)** se fora da DL divulgada: deduzir (e coerência com o
   EBITDA usado — pós ou pré IFRS16, declarar).
9. **Sem dupla contagem entre segmentos** (capex/despesa alocada em dois lugares).

## Valuation e TIR

- DCF do FCFF por segmento (ou consolidado) a Ke nominal: XNPV com datas reais (ano
  corrente fracionado; demais em meio de ano).
- **Perpetuidade going concern**: valor terminal = FCFF normalizado × (1+g) / (Ke − g),
  com g default = IPCA (g real > 0 só com justificativa documentada). **NUNCA ancorar
  no último ano da grade se ele for distorcido** (pico/vale de capex, transição) —
  usar ano normalizado e DECLARAR qual. Ativos com prazo contratual finito (concessões,
  arrendamentos com termo): runoff no vencimento para aquele segmento, sem perpetuidade.
- **TIR implícita na tela**: XIRR do fluxo de dividendos/FCFE ao acionista com
  investimento = −tela×ações (na arquitetura padrão FCFE ≡ dividendo). No último ano
  do horizonte, capturar o valor residual (valor terminal do equity ou liquidação da
  DL) — senão a TIR fica artificialmente baixa. XIRR exige arrays CONTÍGUOS: montar
  bloco espelho dedicado (datas + fluxos).
- **Check de coerência obrigatório**: upside < 0 ⇒ TIR < Ke (e vice-versa). CAVEAT:
  com |upside| < ~5% e alavancagem alta o check por sinal falha por construção — usar
  tolerância e comparar com Ke blended, documentando no LeiaMe.
- Conclusão SEMPRE na régua: **TIR real (Fisher) vs NTN-B longa**, com spread em p.p.
  Se Ke real (Fisher) < NTN-B real, ALERTAR em destaque.

## Armadilhas de execução (openpyxl/ambiente — lições de campo)

- **Scripts >150 linhas: NUNCA editar trecho via ferramenta de edição direta** (trunca
  a cauda — perdeu-se até `wb.save()` em casos reais). Editar via patch python ancorado
  (`str.replace` numa linha única). Após QUALQUER edição: `ast.parse` + `grep wb.save`
  + rodar a sequência build_part1..N COMPLETA do zero.
- **PDF grande**: NUNCA ler o arquivo inteiro no contexto — converter com
  `pdftotext -layout` para um arquivo temporário e processar em disco com python/regex
  por janelas.
- **Arquivo entregável aberto no Excel do usuário = PermissionError ao regravar**:
  build em diretório temporário + cópia final; avisar o usuário para fechar o arquivo.

## Entrega

Excel + resumo com: preço-alvo, TIR real (Fisher) e spread vs NTN-B, reconciliação
quantificada vs premissas do usuário (R$/ação por item), upside não modelado, atalhos
declarados (segmentos projetados por inflação e por quê) e pendências declaradas.
Opiniões rotuladas como opinião.
