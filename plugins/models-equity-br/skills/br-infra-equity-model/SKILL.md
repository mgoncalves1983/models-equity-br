---
name: br-infra-equity-model
description: Build audit-ready Excel equity models (openpyxl, live formulas) or audit existing models for BRAZILIAN listed infrastructure and utility companies — power generation (hydro, wind, solar), transmission, distribution, energy trading. Use this skill whenever the user mentions a B3 utilities/infra ticker (e.g. AURE3, EGIE3, CPLE6, ISAE4, TAEE11, EQTL3, ENGI11, NEOE3, SBSP3, ORVR3), asks to build/model/value a Brazilian utility, mentions SOTP, real IRR vs NTN-B, concessões, runoff, régua de outorga, GSF, curtailment, RAP, RAB, or points to their own Brazilian utility model for review/audit. Also use it when asked to update or extend a model previously built with it. NOT for US-listed companies.
---

# Modelos de equity — infraestrutura listada no Brasil

Skill para (A) **construir do zero** ou (B) **auditar** modelos de valuation de empresas
brasileiras listadas de infraestrutura/utilities. Método consolidado a partir dos modelos
ENGIE (EGIE3), Auren (AURE3), ISA Energia (ISAE4) e **Copel (CPLE3 — regulado completo
D+G+T, jul/2026)** do autor (PM buy-side).

## Como ler esta skill (instrução de processo — leia primeiro)

`references/regras_bloqueantes.md` é **uma tela** e concentra tudo que invalida a
entrega. **Reler: (a) antes do primeiro código, (b) antes de cada módulo novo, (c) antes
de cada entrega, (d) depois de qualquer compactação de contexto.** Ler uma vez no início
da sessão NÃO funciona — instrução decai em sessão longa, e isso já falhou em produção:
a regra estava lida e mesmo assim o modelo foi construído sem um dos documentos
obrigatórios.

Os demais references são material de apoio, lidos **no ponto de uso**:
`data_sourcing.md` na coleta, `segment_modules.md` imediatamente antes de escrever cada
módulo, `build_playbook.md` na construção, `audit_protocol.md` antes de cada entrega e no
modo auditoria. `casos.md` só sob demanda — traz a evidência por trás das regras, útil
para convencer o usuário, inútil no caminho crítico.

## Primeira rodada e configuração — SEMPRE antes do Passo 0

Esta skill foi feita para o **Claude Code**: precisa de terminal e de arquivos locais.
Caminhos `scripts/`, `references/` e `assets/` citados aqui são relativos a
`${CLAUDE_PLUGIN_ROOT}/skills/br-infra-equity-model/`. As pastas de trabalho ficam num arquivo de
configuração compartilhado pelas skills do pacote `models-equity-br`. Antes de
qualquer outra coisa, rodar (no Windows, `python` ou `py` no lugar de `python3`):

    python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-infra-equity-model/scripts/config.py" status

- **Configurado** (código 0) → usar `pasta_ri`, `pasta_fundamentos` e `pasta_saida` em
  todo o fluxo, sem perguntar de novo. Se `pastas_inexistentes` vier preenchido, avisar
  o usuário e oferecer corrigir (comando `/models-equity-br:configurar`).
- **Não configurado** (código 3) → **PRIMEIRA RODADA.** A primeira mensagem ao usuário
  é SÓ este aviso, com as três perguntas das pastas (trocando `<arquivo>` pelo caminho
  que o `status` imprimiu). Nenhuma pergunta sobre a empresa nessa mensagem — elas vêm
  depois de a configuração estar gravada:

  > Esta skill foi feita para o **Claude Code**. Como é a primeira vez, vou criar um
  > arquivo de configuração em `<arquivo>` com três informações, que ficam valendo para
  > as próximas vezes:
  > 1. **Pasta dos documentos de RI** — uma subpasta por empresa, com releases, ITR/DFP e
  >    apresentações. Se ainda não tiver, diga onde quer que eu crie.
  > 2. **Pasta das planilhas de fundamentos** (opcional) — dados históricos das empresas.
  > 3. **Pasta onde salvar os modelos.**
  >
  > Você pode mudar depois com `/models-equity-br:configurar` ou editando o arquivo.

  Gravar as respostas com
  `python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-infra-equity-model/scripts/config.py" set --pasta-ri "..." --pasta-fundamentos "..." --pasta-saida "..."`
  (`--criar` só se o usuário pediu para criar pastas novas; `--pasta-fundamentos ""`
  se não houver). Depois rodar `python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-infra-equity-model/scripts/config.py" deps` e informar ao usuário:
  onde o arquivo foi criado, o que ele contém e as dependências faltantes com o comando
  de instalação. Só então seguir para o Passo 0.
- **Fora do Claude Code** (sem terminal ou sem acesso a arquivos locais) → avisar que a
  skill foi feita para o Claude Code, pedir as pastas/arquivos só para esta conversa e
  seguir; nada é gravado.

Nunca usar caminhos fixos: toda pasta vem da configuração ou do usuário.

## Passo 0 — Identificar o modo (inferir, confirmar em uma linha)

- Usuário indicou um .xlsx próprio e pede crítica/revisão/mapeamento → **modo AUDITORIA**
  (ler `references/audit_protocol.md`; NÃO fazer as perguntas de premissas — elas saem do
  próprio modelo auditado).
- Pede modelo/valuation/TIR de uma empresa → **modo CONSTRUÇÃO** (seguir abaixo).
- Ambíguo → perguntar: "construir do zero ou auditar um modelo existente?"

## Modo CONSTRUÇÃO — fluxo obrigatório

1. **Coleta** — ler `references/data_sourcing.md` e seguir a hierarquia de fontes.
   Procurar a planilha da companhia em `pasta_fundamentos`; se não achar, perguntar
   SEMPRE, logo no início: *"você tem uma planilha com dados históricos da companhia?
   Me passe o caminho do arquivo — isso evita abrir release por release."* Se tiver, ela
   é a fonte primária do histórico. Inventariar `<pasta_ri>/<Empresa>` ANTES de buscar
   na web. Se o perímetro tiver DISTRIBUIÇÃO: coletar também a
   NT da última RTP e as REHs dos reajustes anuais (ANEEL/cedoc). Para a aba Trimestral:
   o release de CADA trimestre (não há atalho).
   **CONTEXTO OBRIGATÓRIO — ler 4 documentos ANTES de modelar** (dão guidance, o bridge
   de recorrência oficial, o critério de covenant e o tom da tese):
   (1) press release ANUAL do último exercício (4Txx); (2) DFP do último exercício;
   (3) ÚLTIMO press release trimestral; (4) última APRESENTAÇÃO de resultados.
   Se não localizar algum, PEDIR ao usuário; se ele não quiser fornecer, declarar a
   lacuna e seguir. Se a companhia publica DATABOOK oficial ("Base de Dados"), ele é
   fonte primária: inventariar TODAS as abas (guidance de capex/"invest previsto",
   extraordinários, composição acionária, ativo a ativo) ANTES de fixar premissas —
   guidance da companhia > estimativa própria.
2. **Perguntas iniciais** (uma mensagem só; **TODA pergunta vem com default sugerido** —
   isso ajuda o usuário a pensar nas possibilidades; NUNCA assumir sem perguntar):
   (a) IPCA de longo prazo (default 4,0%);
   (b) Ke nominal (default 12%);
   (c) perímetro / CHAVEAMENTO DE MÓDULOS: quais segmentos existem — distribuição,
       geração, transmissão, comercialização, outros? **Mapear TODOS os segmentos,
       mesmo os pequenos** — a maioria das empresas tem segmentos secundários e vale
       modelar cada um com o módulo próprio (`references/segment_modules.md`) para o
       resultado sair correto; participações societárias;
   (d) tratamento de terminal — default: **runoff + indenização de ativos não
       amortizados como BASE, para distribuição E geração, SEM renovação** (o mercado
       majoritariamente olha assim); renovação com régua de outorga só como cenário.
       VERIFICAR antes se há **aditivo de prorrogação assinado** (Decreto 12.068/2024):
       renovação contratada é FATO, não premissa. Se houver runoff, a grade explícita vai
       até o ÚLTIMO vencimento e cada entidade LIQUIDA no próprio ano de vencimento;
   (e) granularidade (default: cluster por usina/complexo com mesmo vencimento);
   (f) anos de histórico (default: 3 últimos anos anuais; mínimo 2 para distribuição) —
       e se houve **M&A no período** (se sim, coluna proforma);
   (g) **GSF de longo prazo** (default 0,85) — se houver hidro;
   (h) **curtailment eólico e solar de longo prazo** (defaults 14% / 20%) — se houver
       renováveis; solar é estruturalmente pior;
   (i) preço de energia LP (default R$ 200/MWh nominal-2026, líquido, indexado a IPCA);
   (j) SE TEM DISTRIBUIÇÃO: **data do evento tarifário anual** da concessionária (REH do
       último reajuste — define os pesos de calendarização do módulo), ano da próxima
       RTP e duração do ciclo, trajetória do WACC regulatório (input ANUAL; default =
       implícito da última RTP constante), **β de elasticidade do CAOM ao Mercado Fio B
       (default 0,50 — o CAOM CRESCE com a rede; NÃO usar haircut de produtividade, que
       duplica o Fator X)** e crescimento projetado do Mercado Fio B por concessão;
   (k) impostos — default sugerido: alíquota **EFETIVA por entidade** do último ano
       cheio (IR/EBT do reportado; embute JCP e presumido); alternativa: 34% estatutária
       por cluster. **GATILHO SUDAM/SUDENE**: se a entidade tem incentivo MATERIAL
       (efetiva muito abaixo de 34% por redução de IRPJ), o cluster incentivado passa a
       DUAS FASES — alíquota incentivada até o ano do laudo (nota de IR da DF anual traz
       os vencimentos) e nível normalizado (~30%; conservador 34%) depois. Default =
       NÃO RENOVAR o laudo (prazo legal de novos laudos vai só até 2028 + risco de a
       ANEEL capturar o benefício na tarifa); renovação = cenário/upside no LeiaMe.
       Precedente real: perpetuar vs extinguir valia -19% de TP e -1,3 p.p. de TIR real;
   (l) dividendos — **arquitetura: o DIVIDENDO é a política; a dívida líquida é a
       RESULTANTE** (roll-forward), nunca o contrário. Parâmetros (defaults sugeridos):
       **TRÊS parâmetros — piso, TETO e sweep**: piso = política divulgada (default
       25%, art. 202, JCP conta — mas VERIFICAR O ESTATUTO: a lei permite abaixo de 25%
       desde que definido com precisão, e há companhia com 1%); **teto = payout máximo
       sobre o lucro, ancorado no histórico da companhia — sem ele o sweep leva a
       companhia a se realavancar para distribuir (payout de 148% em caso real)**;
       alvo de alavancagem do sweep = divulgado pela companhia;
       senão ND/EBITDA atual se ≤ 3,5x, ou 3,5x com convergência em 3 anos. Fórmulas e
       regras no build_playbook. SEMPRE reconciliar o payout implícito vs o histórico.
       Alavancagem SEMPRE sobre EBITDA recorrente — distinguir covenant oficial (ex.:
       pro forma proporcional com JVs) do critério analítico, rotulando qual está no alvo.
3. **GATE DE PREMISSAS — obrigatório, antes de QUALQUER código.** Apresentar em bullet
   points, no máximo 15, o que vai ser feito. O usuário tem de dizer **go** explícito.
   Sem isso, não escrever uma linha. Conteúdo mínimo:
   - **Fontes lidas**: quais dos 4 documentos obrigatórios foram lidos e quais faltaram
     (declarar a lacuna, não omitir); se o databook foi inventariado aba a aba.
   - Taxas: IPCA, Ke nominal, Ke real por Fisher, NTN-B de referência — e **alertar se o
     Ke real ficar abaixo da NTN-B**, o que torna o preço-alvo generoso por construção.
   - Horizonte e terminal: até quando vai a grade explícita; se há renovação ou
     indenização; **avisar que o default é crescimento de mercado convergindo a ZERO
     perto da perpetuidade com capex/QRR = 1,0x**, porque as duas premissas têm de ser
     coerentes entre si.
   - Capex: múltiplo da QRR de partida e de estado estacionário; se há guidance oficial.
   - CAOM: β de elasticidade ao Mercado Fio B (default 0,50) e que NÃO há haircut.
   - Fator X: nível e que está como input azul anual (metodologia do Pd em revisão).
   - Crescimento de mercado projetado por concessão, com o realizado ao lado.
   - Impostos: alíquotas por entidade, laudos SUDAM/SUDENE e ano de vencimento.
   - Política de dividendos: **piso (default 25%, MAS verificar o estatuto), teto e alvo
     do sweep** — os três com valor explícito.
   - Alavancagem: alvo, e que o modelo não impõe restrição de financiamento no fluxo.
   - Minoritários: percentuais e se há segunda camada (preferenciais).
   - Atalhos declarados e pendências de dado.
4. **Arquitetura** — propor abas, clusters e fontes por linha; ESPERAR o ok explícito.
5. **Construção** — **RELER `references/regras_bloqueantes.md` antes de cada módulo** e
   ler `references/build_playbook.md` (padrões técnicos, calibração,
   bridge, valuation, Multiplos, Trimestral enriquecida) e
   `references/segment_modules.md` (regras por segmento: hidro, eólica/solar, receita de
   potência/LRCAP, comercialização, transmissão, distribuição, participações).
6. **Verificação** — **RELER `references/regras_bloqueantes.md`** e rodar
   `scripts/verify_model.py`: recálculo LibreOffice com gate de ZERO
   erros de fórmula + checks de coerência. Nunca entregar sem passar.
7. **Entrega** — Excel com fórmulas vivas, salvo em `pasta_saida` (informar o caminho
   completo) + resumo com conclusões na régua **TIR real
   (Fisher) vs NTN-B longa** e reconciliação quantificada (R$/ação e p.p. de TIR) contra
   as premissas do usuário, item a item. DECLARAR no output todo atalho de projeção
   usado (regra anti-atalho abaixo) e toda pendência de dado.

## Regras de ouro (resumo — detalhes nos references)

- Fisher SEMPRE (nunca subtração aritmética de inflação). XNPV/XIRR com datas reais;
  ano corrente fracionado; demais fluxos em meio de ano. Data de valuation em célula própria.
- **PROIBIDO o atalho "EBITDA subindo IPCA até a perpetuidade"**: projetar SEMPRE
  decomposto por driver (distribuição ← motor de Parcela B por ciclo; transmissão ← RAP
  por contrato; geração ← volume x preço x GSF/curtailment; comercialização ← book).
  Se para algum segmento pequeno o atalho for inevitável (sem dado), DIZER no output da
  entrega que foi usado e explicar por quê.
- Cores: azul = input; preto = fórmula; verde = link entre abas. Nomes definidos para
  premissas. Comentário com FONTE e derivação em toda célula de input. R$ mn, anual.
- Histórico lado a lado com a projeção, nas MESMAS linhas. DOIS bridges obrigatórios
  (Historico anual E Trimestral): (i) soma dos segmentos → consolidado (plug de
  holding/eliminações documentado); (ii) reportado → RECORRENTE (EBITDA e lucro líquido,
  com IR sobre os ajustes no LL) — cada ajuste explicado quando possível.
- **VNR NUNCA é caixa e NUNCA entra no EBITDA recorrente — histórico NEM projetado.**
  Mostrar o EBITDA reportado como linha de REFERÊNCIA, mas TODO o trabalho (calibração,
  alavancagem, política de dividendos, múltiplos, projeção) é ex-VNR. A contrapartida
  econômica do VNR é a indenização terminal da RAB: VNR no fluxo + indenização = DUPLA
  CONTAGEM (num caso real auditado: -R$ 8,5/ação, -15% de TP — mudava a conclusão).
  Em DisCos com VNR relevante, fazer também o bridge LL → "lucro caixa" (base do payout).
- Contratos existentes a preço implícito CALCULADO das DFs (receita/volume); descontratado
  a energ_lp. Cotas/RAG fora da base de GSF (risco hidrológico é do cotista).
- Impostos: se usar alíquotas EFETIVAS por entidade, o ESCUDO DE JUROS do FCFE usa a
  MESMA efetiva consolidada (nunca 34% — dobraria o benefício do JCP), e a combinação
  "WACC regulatório pré-imposto (gross-up a 34%) + efetiva baixa" é generosa →
  sensibilidade obrigatória na entrega. Trava de 30% no prejuízo fiscal. Caveat sempre:
  não há consolidação fiscal no Brasil.
- Minoritários: deduzir a **book value** por default (decisão do autor), OU **no fluxo**
  de cada entidade quando houver participação relevante (>20% numa controlada material).
  Checar SEMPRE por dentro — Σ (1 − %) × lucro de cada entidade — contra o reportado:
  gap sistemático indica segunda camada, tipicamente preferenciais resgatáveis em holding
  intermediária, que são encargo fixo a CDI e não participação proporcional.
- NUNCA anualizar um trimestre para calibrar linha sazonal (eólica é o pior caso; hidro
  via GSF/PLD também). Calibrar no ano cheio mais recente; trimestre é só check.
- Coerência TIR ↔ SOTP: se upside < 0, a TIR implícita TEM de ser < Ke. Se o bridge deduz
  um estoque, o fluxo da TIR deduz os desembolsos correspondentes. Se não conseguir
  fechar a coerência, LISTAR o porquê na entrega.
- Transmissão: se RAP > ~15-20% do EBITDA consolidado (ou a pedido), módulo completo
  (DRE regulatória); senão, mini-cluster. Ver `references/segment_modules.md`.
- Distribuição: motor COMPLETO por ciclo tarifário, calendarizado pela DATA do evento
  tarifário da empresa, com calibração obrigatória contra o reportado — ver o módulo em
  `references/segment_modules.md` (nunca proxy de EBITDA indexado).
- Aba Trimestral é entregável padrão (versão enriquecida — ver build_playbook): dado do
  PRÓPRIO release de cada trimestre; derivação por diferença (2T = 9M − 1T − 3T) só como
  fallback marcado; soma dos tris = FY exato (inclusive do EBITDA recorrente).
- Aba **Multiplos** é entregável padrão (substituiu a antiga aba Sensibilidade) — spec
  no build_playbook; template em `assets/example_multiples.xlsx`.
- **Número principal = VPL(FCFE @ Ke)**; o SOTP (FCFF a Ke, dívida a face) é atribuição
  de valor por ativo e SUBESTIMA o equity quando Kd < Ke. Reportar os dois com a
  diferença rotulada. Não usar WACC com alavancagem variável.
- **FCFE yield** é linha padrão da aba Valuation: `(dividendos pagos − Δ dívida líquida)
  / market cap`, sobre a dívida analítica, com aporte de capital como fluxo negativo.
- **Alavancagem em TRÊS visões**: analítica (todas as dívidas, inclusive quase-dívida em
  patrimônio e passivos negociados), visão da companhia, e visão covenant com o limite
  contratual das escrituras. Bridge quantificado entre elas.
- Valuation reporta as linhas de TIR FCFE e TIR DDM — na arquitetura padrão (dividendo
  = política, DL = resultante) FCFE ≡ dividendo por construção e as duas COLAPSAM numa
  só (manter as duas linhas com a nota explicando).
- Upside não modelado (compensações regulatórias, ecossistemas, preços acima do LP) vai
  listado no LeiaMe — nunca silenciosamente no fluxo.

## Scripts

- `scripts/helpers_template.py` — col(), w(), sec(), estilos e formatos padronizados.
- `scripts/verify_model.py` — recalc + gate zero erros + checks de coerência + varredura
  de dívida de entidade não zerada pós-vencimento + coerência entre crescimento terminal
  de mercado e múltiplo capex/QRR + varredura
  de itens não-caixa/não recorrentes no EBITDA (3a VNR; 3b equivalência patrimonial,
  MtM/valor justo, impairment, baixas, "não recorrente").
- `scripts/config.py` — configuração local (`status`, `set`, `get`, `deps`); ver
  "Primeira rodada" acima.
- `scripts/recalc.py` — recalcula o .xlsx no LibreOffice e conta erros de fórmula
  (usado pelo `verify_model.py`; também roda sozinho).
- `scripts/ir_importer.py` — coletor de documentos de RI. **Dependências:
  `pip install selenium requests` + Google Chrome** (portais MZiQ; Selenium para colher
  links, requests para baixar). Uso: `python3 scripts/ir_importer.py <Empresa> <anos...>
  [--portal URL]`; salva em `<pasta_ri>/<Empresa>/`. ANTES de rodar: inventariar
  `<pasta_ri>/<Empresa>/` e coletar SÓ os períodos faltantes (pré-voo em
  `references/data_sourcing.md` — senão cria duplicatas em massa). Implementação de
  referência — se o usuário tiver um importador próprio, usar o dele.
