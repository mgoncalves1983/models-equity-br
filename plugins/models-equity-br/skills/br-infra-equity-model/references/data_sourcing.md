# Fontes de dados e economia de contexto

## Hierarquia (parar na primeira que resolver)

1. **Planilha do usuário com dados históricos** — procurar primeiro em
   `pasta_fundamentos` (configuração); se não estiver lá, perguntar SEMPRE no início se
   existe e pedir o caminho do arquivo. Evita abrir release por release. Se existir, é a fonte primária do
   histórico (validar 2-3 âncoras contra um release antes de confiar).
2. **Pasta de RI do usuário** (`<pasta_ri>/<Empresa>`, da configuração) — listar ANTES
   de buscar na web. Pode ser uma pasta sincronizada (Google Drive, OneDrive, Dropbox):
   para a skill é uma pasta local. Convenção: subpastas por empresa com releases,
   ITR/DFPs, apresentações e transcrições por trimestre.
3. **Arquivos indicados pelo usuário** — PDFs fora da pasta de RI: pedir o caminho do
   arquivo e processar em disco (ver economia de contexto).
4. **Web/página de RI** — se o usuário não tiver os documentos na pasta de RI,
   PERGUNTAR: *"quer que eu acesse a página de RI da companhia para baixar os arquivos,
   ou você prefere me indicar os arquivos?"* Nunca sair varrendo a web sem essa
   permissão. O que for baixado vai para `<pasta_ri>/<Empresa>/`.
   Primeira modelagem: os PRESS RELEASES normalmente bastam (têm DRE gerencial, balanço
   de energia, endividamento, reconciliação de EBITDA). DFs completas entram para notas
   específicas (IR diferido, cronograma de dívida por indexador, societário, previdência).
5. **CVM/ENET e fontes públicas** — DFPs/ITRs oficiais, fatos relevantes, laudos de AGE;
   DFs de SPEs não listadas saem em publicidade legal (Monitor Mercantil etc.).
6. **ANEEL (obrigatório se o perímetro tem DISTRIBUIÇÃO)** — NT da última RTP (traz
   composição da Parcela B, deduções, WACC, Fator X, CAOM/benchmarking) + REHs dos
   reajustes anuais (cedoc; dão a data do evento tarifário e a PB vigente por ciclo).
   Para TRANSMISSÃO: REH da RAP do ciclo. Para leilões de potência (LRCAP): resultados
   na CCEE/EPE/imprensa especializada. PDFs do cedoc às vezes bloqueiam fetch direto
   (403) — usar espelhos (atosoficiais, canalsolar) ou pedir o arquivo ao usuário.
7. Cotações, NTN-B, balanço de energia atualizado: web search (sempre mais recente que
   qualquer repositório).

**CONTEXTO OBRIGATÓRIO — 4 documentos antes de modelar**: press release ANUAL do último
exercício (4Txx), DFP do último exercício, ÚLTIMO press release trimestral e última
APRESENTAÇÃO de resultados. Dão guidance, bridge de recorrência oficial, critério de
covenant e o tom da tese. Se não localizar, PEDIR; se o usuário não quiser fornecer,
declarar e seguir.

**Databook oficial** ("Base de Dados" e similares): quando existir, é fonte primária de
primeira linha — **inventariar TODAS as abas POR NOME antes de ir a qualquer PDF**.
Databooks de 100+ abas costumam conter **balanço consolidado E por entidade, fluxo de
caixa consolidado E por entidade, e apuração de IR/CSLL** — não só as operacionais.
Falha real: buscar nota de imobilizado num DFP de 200 páginas quando o balanço
consolidado trimestral desde 2013 estava numa aba do próprio databook. Varrer por
`balan`, `BP `, `FC`, `fluxo`, `IR`, `imposto`, `dívida`, `investiment` antes de fixar
premissas (guidance de capex/
"invest previsto" por segmento, extraordinários, composição acionária, ativo a ativo,
RTP/RTA por concessionária). Atenção: abas de "extraordinários" costumam cobrir só o
trimestre corrente — o bridge ANUAL vem do release 4T (tabela de efeitos não caixa e
itens extraordinários com coluna FY).

**Aba Trimestral**: os operacionais (EBITDA recorrente, DL, capex, GSF, curtailment,
PLD) saem do release de CADA trimestre — não há atalho; planejar a leitura dos 4-5
releases (subagentes em paralelo economizam contexto). Linhas de caixa do DFC trimestral
da CVM vêm ACUMULADAS (YTD): tri = YTD(t) − YTD(t−1), sempre marcado como derivado.
PDF grande: nunca ler inteiro no contexto — `pdftotext -layout` e processar em disco
com regex/janelas.

**ARMADILHA DA REAPRESENTAÇÃO**: databook e release divergem quando há operação
descontinuada — a companhia reapresenta o release e não reapresenta o databook.
Caso real: EBITDA ajustado de R$ 13.122 mn no databook contra R$ 12.190 mn no release do
mesmo exercício, com o 4T batendo EXATAMENTE e a diferença toda em 1T-3T. **Cruzar
trimestre a trimestre antes de confiar em qualquer série anual.**

**CUSTO DE HOLDING — vem da NOTA DE SEGMENTOS da DFP**, coluna "Administração" (ou
equivalente), não da DRE da controladora isolada. A controladora isolada é a holding de
topo e pega só uma fração; o segmento administrativo abrange as holdings intermediárias e
os veículos de participações, que é onde ficam o compartilhamento de pessoal e a
infraestrutura. Diferença real: R$ 266 mn contra R$ 596 mn. A mesma nota traz as
**eliminações intercompany** — que costumam ser MUITO menores do que se estima por fora.

**ALÍQUOTA EFETIVA — três medidas, e elas divergem violentamente.** Da nota de
conciliação IRPJ/CSLL e da DFC: efetiva **contábil** (despesa/EBT), **corrente** (só o
imposto corrente) e **caixa** (imposto pago na DFC). Caso real: 17,2% / 31,5% / 22,9% num
ano e −5,7% / 6,0% / 8,7% no anterior. Usar a de **caixa** como âncora, em média de 2
anos, e identificar itens não recorrentes na conciliação (parcelamento de exercícios
anteriores é o mais comum).

## Economia de contexto (lição de guerra)

- **Arquivo em disco > arquivo em contexto.** PDF → `pdftotext -layout` (saída num
  arquivo temporário, nunca dentro da pasta de RI) → grep/sed cirúrgico. Um PDF de 140
  páginas lido inteiro inunda o contexto e pode truncar.
- Ler o PDF diretamente só para arquivos pequenos (releases ≤ ~35 págs). DFP/ITR
  completa: sempre via pdftotext + grep, ou sessão dedicada.
- Links do Drive de arquivos privados NÃO funcionam via curl (auth wall) — não insistir.
- Extração dirigida: localizar a tabela-alvo (grep pelo título: "Reconciliação do
  EBITDA", "Custos por natureza", "Cronograma de amortização") e ler ±20 linhas, nunca o
  arquivo inteiro.
- Derivações economizam fonte: 2T = 9M − 1T − 3T; 4T = FY − 9M (sempre marcar como
  derivado e validar soma = FY).
- Se faltar um documento essencial e o contexto estiver pesado: DECLARAR a pendência na
  entrega (com o que ela afetaria) em vez de degradar a sessão inteira.

## Coletor automatizado (`scripts/ir_importer.py`)

**PRÉ-VOO OBRIGATÓRIO — nunca rodar o importador às cegas:**
1. **Inventariar o repositório existente ANTES**: listar `<pasta_ri>/<Empresa>/`
   e montar o mapa de cobertura
   empresa × trimestre × tipo (release / ITR-DFP / apresentação / transcrição).
2. Rodar o importador **só para os buracos** (anos/períodos faltantes), passando apenas
   esses anos — o dedupe interno do script é por nome de arquivo; rodar às cegas
   re-baixa o que já existe com outro nome e cria duplicatas em massa.
3. Manter a MESMA convenção de nomes do repositório existente (senão o dedupe por nome
   nunca casa e as duplicatas se multiplicam a cada rodada).
4. Depois de baixar, informar ao usuário o que foi adicionado e onde (os arquivos já
   ficam em `<pasta_ri>/<Empresa>/`).

Coletor de DOCUMENTOS de portais de RI brasileiros (plataforma MZiQ e similares):
Selenium headless para colher os links por ano (páginas são SPA renderizadas em JS;
`requests` não enxerga), depois download via `requests` (rápido), com dedupe, filtro
PT-only, captura de links de YouTube das calls, e saída em
`<pasta_ri>/<Empresa>/`. Limitações conhecidas: Cloudflare Turnstile pode
bloquear renderizações repetidas (o script detecta e pula; não burla); rodar com pausas.
Ele NÃO interpreta dados — só baixa arquivos; a extração de números é feita depois,
via pdftotext/grep, pelos fluxos acima. Se o usuário tiver um importador próprio,
usar o dele.
