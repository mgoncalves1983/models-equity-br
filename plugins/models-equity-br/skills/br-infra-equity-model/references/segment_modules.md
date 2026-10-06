# Módulos por segmento (o "chaveamento")

Montar um bloco/aba por segmento presente no perímetro. O chaveamento é definido na
pergunta de perímetro do SKILL.md: liga-se o módulo de cada segmento que existir —
**inclusive os pequenos** (comercialização, serviços, holding): a maioria das empresas
tem segmentos secundários e modelá-los com o módulo próprio evita o erro clássico de
diluí-los num "outros" crescendo a IPCA. **Nunca projetar um segmento como "EBITDA
indexado a inflação até a perpetuidade"** — cada módulo abaixo tem drivers próprios; se
o atalho for inevitável (segmento imaterial sem dado), declarar e justificar na entrega.

Clusters agrupam ativos com o mesmo vencimento e regime. Cada cluster produz FCFF
próprio (EBITDA − imposto do cluster − capex) e morre no vencimento (**runoff +
indenização** como base, sem renovação — para geração E distribuição), salvo cenário de
renovação explícito com régua de outorga.

## Hidrelétricas

- Inputs estruturais por cluster: GF (MWm), fim da concessão, contratação ACR/ACL por ano
  (balanço de energia do release — usar o MAIS RECENTE), preços implícitos calculados
  (receita ÷ volume, com fonte), GSF LP (input do usuário; default 0,85), hedge de GSF se
  houver (volume, preço, vigência — ex.: Mauá/Copel com seguro a 96% da GF: volume =
  GF x MAX(GSF; 0,96)).
- Energia descontratada líquida = recursos×GSF + compras − vendas, valorada a energ_lp.
  Posição líquida pode ser NEGATIVA (compra a mercado) — tratar simétrico.
- Se as eólicas/solares vendem PPAs DENTRO do balanço de energia divulgado do grupo,
  subtraí-las das vendas antes de ratear entre os clusters hídricos (não duplicar).
- Ganhos de modulação/otimização (SIN horário, submercado): linha própria, calibrada no
  realizado do ANO CHEIO (trimestres são atípicos).
- **Cotas/RAG** (usinas cotistas renovadas pela 12.783): risco hidrológico é do cotista —
  TIRAR da base de GSF; receita = RAG indexada.
- Encargos de rede/uso por cluster; PMSO por cluster em R$ do ano-base, indexado.

## Receita de potência / LRCAP (leilões de reserva de capacidade)

- Contratos de potência (LRCAP) viram **cluster próprio**: potência contratada (MW) x
  receita fixa (R$/kW.ano, indexada a IPCA) x fração do ano no início/fim do suprimento,
  pelo prazo do contrato (tip. 15 anos).
- Se for AMPLIAÇÃO (novas unidades geradoras): incluir o capex com cronograma até a
  entrada, O&M incremental (~1-1,5% do capex a.a.) e D&A para o IR. Por default, SEM
  energia/GF adicional (motorização agrega pouca energia média — listar como upside).
- A receita fixa exata do contrato raramente está no release — buscar o resultado do
  leilão (CCEE/EPE/imprensa especializada) e marcar como input azul A CONFIRMAR no
  contrato. Precedente Copel (LRCAP mar/2026, produto ampliação-UHE 2030): ~R$ 1.392/kW.ano,
  deságio 0,4%, 15 anos desde ago/2030.

## Eólicas e solares

- Curtailment por fonte como INPUT do usuário (perguntar no início; solar estruturalmente
  pior — corte de meio-dia). Aplicar sobre a geração esperada (P50 ajustado ao realizado);
  rampa de curto prazo (realizado recente > LP) com convergência em 2-3 anos.
- **Provisões de ressarcimento** (contratos com garantia física entregável): fluxo anual
  de provisão na projeção (calibrar no run-rate realizado) + ESTOQUE no bridge.
- Compensações regulatórias por cortes (Lei 15.269/2025 e regulamentação MME/ANEEL):
  base = zero compensação FUTURA; recebível JÁ RECONHECIDO no balanço entra no bridge;
  potencial adicional divulgado pela companhia vai no LeiaMe como upside.
- Sazonalidade forte (2S >> 1S no NE): NUNCA calibrar anualizando um trimestre.
- Capex de projetos em construção: cronograma da companhia (%, investido vs total).
- Cluster por complexo: PPA (preço do leilão, indexado da data-base) até o fim do
  contrato → descontratado a energ_lp até o fim da autorização.

## Comercializadora

- Modelar pelo BOOK: margem contratual divulgada (R$/MWh) × volumes vendidos por ano de
  vigência — runoff do book como base (sem going concern), salvo ordem contrária.
- Atenção a cessões intercompany (distorcem margem do segmento — ler notas do release) e
  a "ecossistemas" (empresas irmãs de serviços) fora do book → LeiaMe como upside.
- MtM do book: memo, não somar no bridge.

## Transmissão — o IF

Calcular RAP/EBITDA de transmissão ÷ EBITDA consolidado:

- **> ~15-20% (ou a pedido do usuário)** → módulo completo padrão ISAE/Copel: DRE
  REGULATÓRIA (não IFRS) linha a linha; RAP por contrato/lote com data de revisão e
  ciclo tarifário; parcela de ajuste; runoff no vencimento de cada contrato; **valor
  terminal/indenização de ativos não depreciados ("blindada")** como recebível na data
  de vencimento (default zero se não houver laudo — declarar a pendência).
- Contratos renovados pela 12.783 (ex.: 060/2001 da Copel): separar **ex-RBSE**
  (O&M indexado até o vencimento) do bloco **RBSE** (indenização escalonada — os
  componentes econômico/financeiro da PRT 120 TERMINAM em data conhecida; pós-término
  só resta RBNI/O&M — abrir por componente com a NT ANEEL; não perpetuar o RBSE cheio).
- **≤ 15%** → mini-cluster: RAP líquida − PMSO − imposto, runoff no vencimento médio
  ponderado, ~10 linhas. Declarar a simplificação no LeiaMe.

## Distribuição — motor regulatório completo (NUNCA proxy de EBITDA indexado)

### VNR — a armadilha nº 1 do módulo (check bloqueante)

A DRE IFRS das DisCos tem a linha não-caixa **"Atualização do Ativo Financeiro da
Concessão" (VNR)** dentro do EBITDA reportado. Regras invioláveis: (1) calibração e
EBITDA recorrente — histórico E projetado — são **ex-VNR**; (2) VNR vira linha-memo
não-caixa (fora de FCFF/FCFE/dividendos); (3) a contrapartida econômica do VNR é a
**indenização terminal da RAB** — VNR no fluxo + indenização no vencimento = DUPLA
CONTAGEM (caso real auditado: -R$ 8,5/ação, -15% de TP, upside de +17% para ~0);
(4) alavancagem e política de dividendos sobre recorrente ex-VNR; (5) em DisCos com
VNR relevante, bridge LL → "lucro caixa" (algumas companhias definem o payout oficial
sobre lucro caixa, não sobre LL IFRS). O `verify_model.py` varre e cobra confirmação.

### Obrigações especiais — BLOQUEANTE (erro real de R$ 1,4 bn/ano numa DisCo)

Capex de distribuição tem DUAS linhas: **bruto** e **líquido de obrigações especiais**.
As OE são financiadas por consumidores e governo — não entram na base de remuneração
**nem na saída de caixa da companhia**. Tratar capex bruto como próprio infla a BRR E
afunda o FCFF ao mesmo tempo. Extrair da aba de investimentos do databook, média de 3
anos; o share varia de ~0% a 42% entre concessionárias da MESMA holding (ver `casos.md`).

### Mercado Fio B — o driver de escala

Mercado relevante = **energia faturada + GD compensada** (Fio B), nunca energia faturada.
O cliente com geração própria fatura menos e continua usando a rede: o custo de operar
aquele ativo não cai. Em 2025-26 a diferença chegou a 5 p.p. numa única DisCo. Databook:
abas de mercado pré e pós CP09, que se sobrepõem num trimestre e permitem medir a quebra.

### Multi-DisCo (holdings com várias distribuidoras)

Modelar POR DisCo, nunca agregado: cada uma tem SUA data de evento tarifário, SEU ciclo
(4 ou 5 anos), SUA RTP e SEU VNR — os pesos de calendarização e os resets diferem entre
elas. Capex: usar o guidance por DisCo quando divulgado; sanity check: capex de
distribuição saudável ≈ 2-3x QRR (usar só como régua, nunca no lugar do guidance).

### Estrutura do motor (por CICLO tarifário, calendarizado)

1. **Data do evento tarifário**: reajustes e revisões ocorrem numa data fixa anual da
   concessionária (REH do último reajuste; Copel: 24/jun). Toda Parcela B roda por
   CICLO (evento→evento) e o ano-calendário pondera os dois ciclos: **peso_novo =
   fração do ano após a data do evento** (Copel jun → 48/52; um evento em abril daria
   ~25/75; calcular SEMPRE da data real — não copiar o 48/52).
2. **Parcela B do ciclo**: entre revisões, PB(ciclo t) = PB(ciclo t−1) × (1 + IPCA −
   Fator X). Nos anos de RTP, **ANCORAR NA PB VIGENTE E SOMAR O DELTA — nunca remontar a
   receita requerida do zero**:
   `PB(t) = PB(t−1) × (1 + IPCA − X)
            + (BRR_atual − BRR_referência) × (WACC + QRR/BRR)
            + CAOM_referência × (índice de escala − 1)`
   A **BRR de referência** é a homologada na última RTP, indexada pelo **IPCA REALIZADO**
   (input próprio; ~4,8% a.a. para ciclos 2021-2026) e RESETA a cada revisão.
   Remontar do zero exige reconstituir CAOM e deduções com o IPCA realizado de cada
   ciclo — na prática produz CORTE de Parcela B nas revisões, o oposto da realidade,
   porque a PB vigente já embute deduções e o histórico de reajustes.
2b. **CAOM CRESCE com a rede — não leva haircut.** O Submódulo 2.2 do PRORET determina
   que o intervalo de custos operacionais seja ATUALIZADO na revisão pela variação da
   extensão de redes e do número de consumidores. Ganho de escala =
   `CAOM_ref × ((1 + β × g_Fio_B)^n − 1)`, com **β default 0,50**. Evidência: 11 revisões
   reais, CAOM subiu em termos reais em 10 (`casos.md`). Haircut de produtividade DUPLICA
   o Fator X, que é o mecanismo formal de compartilhamento — usar um OU outro, nunca os
   dois. β < 1 reflete economia de escala: o CAOM por MWh cai mesmo com o absoluto
   subindo, e é assim que a eficiência volta para a tarifa.
3. **PB ajustada ≠ soma dos componentes**: a ANEEL deduz da receita requerida as
   "deduções da PB" — Outras Receitas (Sub. 2.7A: ~60% da receita bruta de atividades
   próprias vai à modicidade), ultrapassagem de demanda/excedente de reativos, Fator Q
   e componente Pd. Derivar a cunha = (RC+QRR+CAOM+CAIMI) − PB homologada, indexar a
   IPCA e abater nos resets. Ignorar isso superestima cada RTP futura em ~5-10%.
4. **RAB**: RAB(t) = RAB(t−1) × (1+IPCA) + capex − QRR (VNR blindada indexada).
   **QRR = razão homologada QRR/RAB × RAB do ano** (proporcional à base — proxies
   incrementais sub-depreciam no roll longo).
   **Capex = MÚLTIPLO DA QRR convergente**, nunca nível real fixo: nível fixo faz a base
   crescer sem limite e exigiria alta real insustentável da tarifa Fio B. Partir do
   múltiplo realizado no último ano cheio (tipicamente 2,5x a 3,5x em turnaround) e
   convergir ao estado estacionário em ~10 anos. **DEFAULT DE ESTADO ESTACIONÁRIO:
   crescimento de mercado convergindo a ZERO perto da perpetuidade e capex/QRR = 1,0x** —
   as duas premissas têm de ser coerentes entre si, senão o modelo escoa mais energia com
   a mesma rede indefinidamente. AVISAR o usuário nos bullet points de premissas.
   Taper para 1,0x nos últimos anos da concessão quando houver vencimento modelado.
5. **WACC regulatório = input ANUAL azul** (PRORET Sub. 2.4 recalcula todo ano com
   janelas de NTN-B + risco). O reset usa o WACC do ano da RTP. Segurar o WACC atual
   para sempre enquanto se desconta a Ke baixo é inconsistente — o usuário impõe a
   trajetória de juros.
6. **Haircut de produtividade** (input azul por RTP, default 5%): o CAOM é definido por
   benchmarking (Sub. 2.2A — custo eficiente, não custo real); precedentes mostram corte
   no ato da revisão + trajetória via componente T do Fator X ao longo do ciclo. Acoplamento:
   se o T entregar a convergência dentro do ciclo, haircut menor no reset seguinte.
7. **EBITDA = PB calendarizada − PMSO real (indexada) − provisões/PDD**; IR com D&A
   fiscal = QRR; FCFF = EBITDA − IR − capex; no vencimento da concessão, **indenização
   INTEGRAL da RAB líquida não amortizada** (runoff-base; renovar = manter FCFF e abrir
   mão da indenização — é assim que o cenário de renovação deve ser montado).
8. **O degrau nas RTPs é ESTRUTURAL** (regulatory lag: entre revisões só IPCA−X; capex >>
   QRR só é remunerado no reset). Antes de "suavizar", validar o tamanho do degrau contra
   o precedente da própria empresa na última RTP.

### Vencimento, renovação e indenização — BLOQUEANTE

**Verificar SEMPRE se há aditivo de prorrogação assinado.** O Decreto 12.068/2024 criou o
arcabouço de prorrogação por 30 anos das concessões de distribuição; renovação contratada
é FATO, não premissa, e muda o vencimento em três décadas.

Se modelar **sem renovação**: cada concessionária roda até o próprio vencimento e recebe
a indenização da base não amortizada (BRR líquida do ano), com **haircut e defasagem como
inputs azuis**. A grade explícita tem de ir até o último vencimento — não truncar e
perpetuar, porque o valor da indenização é grande e o perfil de fluxo é muito irregular.

**A entidade tem de LIQUIDAR no ano do vencimento**: dividendo = `FCFE − dívida de
abertura`, SEM piso em zero, e fluxo zero depois. Se ficar `MAX(0; ...)`, o sweep deixa
`alvo × EBITDA` de dívida no vencimento e ela capitaliza juros contra EBITDA zero para
sempre — erro real de R$ 86,7 bn de dívida fantasma que só apareceu 15 anos depois
(`casos.md`).

**VNR ↔ indenização é excludente**: se renova, não há indenização terminal; se não
renova, modelar a indenização e manter o VNR fora do EBITDA. Contar os dois é dupla
contagem.

### Depreciação contábil (não confundir com QRR)

A QRR é a referência REGULATÓRIA e governa o IR do motor. A **depreciação contábil** é
outra coisa e serve para fechar o lucro reportado e os múltiplos. **Nunca projetar D&A
como percentual do EBITDA** — a base cresce com CAPEX, não com EBITDA, e o proxy
subestima justamente nos anos de investimento pesado.

Roll-forward consolidado, sobre a base **BRUTA** (a taxa incide sobre custo, não sobre
líquido): obra em andamento recebe o capex e energiza um percentual do saldo por ano; a
energização entra na base depreciável; baixa proporcional no vencimento de cada concessão.
Taxas na nota de imobilizado/intangível da DFP (tipicamente 3,3% a 4,2% no intangível de
concessão). **O ativo financeiro da concessão NÃO deprecia** — é a parcela indenizável.
Ordem de grandeza: QRR consolidada roda 1,0x a 1,2x a D&A do grupo inteiro.

### Calibração obrigatória (mín. 2 anos)

Comparar `PB vigente do ano − PMSO real − provisões` com o **EBITDA recorrente ex-VNR
reportado** dos 2 últimos anos cheios, e COMENTAR o desvio (mercado real vs regulatório,
outras receitas retidas — os 40% que ficam com a concessionária —, CVA/timing, perdas
vs regulatório). Desvio de até ~10% positivo é normal; o motor é piso conservador.
Ativos/passivos financeiros setoriais (CVA): estoque no bridge.

### EXEMPLO CANÔNICO — Copel DIS, 6ª RTP (homologada 23/06/2026)

> **ATENÇÃO: os números abaixo são o exemplo trabalhado da Copel. NUNCA usar em outra
> empresa — coletar os equivalentes na NT/REH da concessionária modelada.**
> RAB líquida homologada R$ 19.936,2 mn; PB homologada R$ 5.720,9 mn = RC 2.530,6 +
> QRR 1.004,6 + CAOM 2.238,3 + CAIMI 422,7 − deduções 475,3; QRR/RAB = 5,04% (taxa
> regulatória 3,88% s/ base bruta); WACC pré implícito 12,69% (NT: 12,28%); Fator X
> 0,95% (componente T 0,403%); CAOM cortado 5,0% no ato (cobertura estava 8,85% acima
> do intervalo eficiente); PB +32,6% vs ciclo anterior (o degrau real); evento tarifário
> 24/jun (pesos 48/52); ciclo de 5 anos, RTP seguinte 2031; concessão até 07/07/2045.
> Fontes: NT 44/2026-STR/ANEEL, NT 100/2026, FR Copel 04/26, REH 3.472/2025.

## Participações minoritárias (equivalência)

- Preferir marcar a TRANSAÇÃO REAL recente quando existir.
- Senão: NPV do fluxo de dividendos, calibrado no ANO CHEIO mais recente (nunca
  trimestre anualizado — dividendos seguem PLD/sazonalidade), com % societário e
  desproporcionalidades (dividendo preferencial, mais-valia em amortização) do anexo
  societário das DFs.

## Holding e impostos

- PMSO de holding: linha própria, indexada, perpetuada até o fim do último cluster.
- Imposto por cluster — duas opções (perguntar, com a primeira como default sugerido):
  1. **Alíquota EFETIVA por entidade** = IR total/EBT do último ano cheio (reportado).
     Embute JCP dedutível e presumido das SPEs. Caveats obrigatórios: é medida sobre
     EBT (pós-financeiro) e com itens do ano; equivalência não tributada infla o
     benefício; o ESCUDO DE JUROS do FCFE deve usar a MESMA efetiva consolidada (não
     34%); combinada com WACC regulatório pré-imposto (gross-up a 34%) é generosa →
     sensibilidade obrigatória na entrega.
  2. Alíquota do regime por cluster (real 34%, presumido ~x% da receita).
- **GATILHO SUDAM/SUDENE — duas fases (default: NÃO RENOVAR o laudo)**: se a entidade
  tem incentivo MATERIAL (efetiva muito abaixo de 34% por redução de 75% do IRPJ), o
  cluster incentivado sai da efetiva única e passa a DUAS FASES, com 3 inputs azuis
  (alíq. incentivada | alíq. pós-laudo | ano do laudo — a nota de IR da DF anual traz
  os vencimentos por entidade): `IR = −IF(ano <= laudo; aliq_inc; aliq_pos) × MAX(0;
  EBITDA − D&A fiscal)`. Pós-laudo: ~30% normalizado (conservador: 34%). Racional
  (jul/2026): prazo legal de aprovação de novos laudos vai só até 2028 + risco de a
  ANEEL capturar o benefício na tarifa das DisCos. Renovação dos laudos = só
  CENÁRIO/upside no LeiaMe. Precedente real: perpetuar vs extinguir = -19% de TP e
  -1,3 p.p. de TIR real.
- **Circuito de impostos no FCFE — caveats a declarar SEMPRE**:
  (a) QRR como proxy de D&A fiscal SUPERESTIMA o IR de DisCo em ciclo de capex pesado
  (a base fiscal real cresce com capex e juros capitalizados) — conservador;
  (b) sem consolidação fiscal, o escudo real do juro depende de ONDE está a dívida:
  na holding (lucro tributável ~zero, equivalência isenta) vira prejuízo fiscal com
  trava de 30% (escudo diferido); dentro da DisCo deduz a 34% (o financeiro fica FORA
  do lucro da exploração — o incentivo não corta o escudo). A efetiva consolidada é um
  meio-termo — declarar;
  (c) se o NPV do DTA entra no bridge do SOTP, o fluxo da TIR idealmente recebe a linha
  de realização do cronograma — senão a TIR fica conservadora vs o TP (assimetria a
  declarar).
- Prejuízo fiscal acumulado: ativo separado no SOTP — NPV do cronograma de realização
  divulgado nas DFs (trava de 30% embutida). Caveat obrigatório: não há consolidação
  fiscal no Brasil; companhias pagam IR mesmo com EBT consolidado negativo.
