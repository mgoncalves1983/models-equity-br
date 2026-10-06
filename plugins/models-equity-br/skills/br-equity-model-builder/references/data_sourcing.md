# Fontes de dados e economia de contexto

## Hierarquia (parar na primeira que resolver)

1. **Planilha de fundamentos/histórico do usuário** — procurar primeiro em
   `pasta_fundamentos` (configuração); se não estiver lá, perguntar SEMPRE no início se
   existe e pedir o caminho do arquivo. Evita abrir release por release. Se existir, é a fonte
   primária do histórico (validar 2-3 âncoras contra um release antes de confiar).
2. **Pasta de RI do usuário** (`<pasta_ri>/<Empresa>`, da configuração) — inventariar
   ANTES de buscar na web. Pode ser uma pasta sincronizada (Google Drive, OneDrive,
   Dropbox): para a skill é uma pasta local. Convenção: subpastas por empresa com
   releases, ITR/DFPs, apresentações e transcrições por trimestre.
3. **Arquivos indicados pelo usuário** — PDFs fora da pasta de RI: pedir o caminho do
   arquivo e processar em disco (ver economia de contexto).
4. **Web/página de RI** — se o usuário não tiver repositório, PERGUNTAR: *"quer que eu
   acesse a página de RI da companhia para baixar os arquivos, ou você prefere fazer
   indicar os arquivos?"* Nunca sair varrendo a web sem essa permissão. O que for
   baixado vai para `<pasta_ri>/<Empresa>/`. Primeira modelagem: os PRESS
   RELEASES normalmente bastam (DRE gerencial, aberturas operacionais, endividamento,
   reconciliação de EBITDA). DFs completas entram para notas específicas (IR diferido,
   cronograma de dívida por indexador, societário, previdência, litígios).
5. **CVM/ENET e fontes públicas** — DFPs/ITRs oficiais, fatos relevantes, laudos de AGE;
   DFs de controladas não listadas saem em publicidade legal.
6. Cotações, NTN-B, dados de mercado: web search (sempre mais recente que qualquer
   repositório).

**CONTEXTO OBRIGATÓRIO — 4 documentos antes de modelar**: press release ANUAL do último
exercício (4Txx), DFP do último exercício, ÚLTIMO press release trimestral e última
APRESENTAÇÃO de resultados. Dão guidance, bridge de recorrência oficial, critério de
covenant e o tom da tese. Se não localizar, PEDIR; se o usuário não quiser fornecer,
declarar e seguir.

**Databook oficial** ("Base de Dados", planilha de fundamentos da própria companhia):
quando existir, é fonte primária de primeira linha — inventariar TODAS as abas antes de
fixar premissas (guidance de capex/"invest previsto", itens extraordinários, composição
acionária, aberturas por segmento). Atenção: abas de "extraordinários" costumam cobrir
só o trimestre corrente — o bridge ANUAL vem do release 4T.

**Aba Trimestral**: os operacionais e o EBITDA recorrente de cada tri saem do release
do PRÓPRIO trimestre — não há atalho; planejar a leitura dos 4-5 releases (subagentes
em paralelo economizam contexto). Linhas de caixa do DFC trimestral da CVM vêm
ACUMULADAS (YTD): tri = YTD(t) − YTD(t−1), sempre marcado como derivado.
PDF grande: nunca ler inteiro no contexto — `pdftotext -layout` e processar em disco
com regex/janelas.

## Economia de contexto (lição de guerra)

- **Arquivo em disco > arquivo em contexto.** PDF → `pdftotext -layout` (saída num
  arquivo temporário, nunca dentro da pasta de RI) → grep/sed cirúrgico. Um PDF de 140
  páginas lido inteiro inunda o contexto.
- Ler o PDF diretamente só para arquivos pequenos (releases ≤ ~35 págs). DFP/ITR
  completa: sempre via pdftotext + grep, ou subagente dedicado.
- Extração dirigida: localizar a tabela-alvo (grep pelo título: "Reconciliação do
  EBITDA", "Cronograma de amortização", "Composição acionária") e ler ±20 linhas,
  nunca o arquivo inteiro.
- Derivações economizam fonte: 2T = 9M − 1T − 3T; 4T = FY − 9M (sempre marcar como
  derivado e validar soma = FY).
- Se faltar um documento essencial e o contexto estiver pesado: DECLARAR a pendência na
  entrega (com o que ela afetaria) em vez de degradar a sessão inteira.

## Coletor automatizado (`scripts/ir_importer.py`)

**PRÉ-VOO OBRIGATÓRIO — nunca rodar o importador às cegas:**
1. Inventariar o repositório existente ANTES (`<pasta_ri>/<Empresa>/`) e montar
   o mapa de cobertura empresa × trimestre × tipo.
2. Rodar SÓ para os buracos (anos/períodos faltantes) — o dedupe interno é por nome de
   arquivo; rodar às cegas cria duplicatas em massa no repositório.
3. Manter a MESMA convenção de nomes do repositório existente.
4. Depois de baixar, informar ao usuário o que foi adicionado e onde (os arquivos já
   ficam em `<pasta_ri>/<Empresa>/`).

Portais MZiQ e similares: Selenium headless para colher links por ano (SPAs em JS),
download via requests, dedupe, filtro PT-only. NÃO interpreta dados — só baixa. Se o
usuário tiver um importador próprio, usar o dele.
