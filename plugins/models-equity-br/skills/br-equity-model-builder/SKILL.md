---
name: br-equity-model-builder
description: Build audit-ready Excel equity models (openpyxl, live formulas) or audit existing models for ANY BRAZILIAN listed company, from the user's fundamentals spreadsheet ("planilha de fundamentos"), the user's local folder of investor-relations PDFs (releases, ITR/DFP, presentations) and CVM filings. Use whenever the user gives a B3 ticker or asks to build/model/value a Brazilian company, mentions modelo, valuation, TIR real vs NTN-B, DFP/ITR, press release de resultados, planilha de fundamentos, or points to their own Brazilian company model for review/audit. NOT for power/utilities/electric infrastructure names (generation, transmission, distribution — use br-infra-equity-model) and NOT for US-listed companies.
---

# Modelos de equity — empresas brasileiras listadas (genérico)

Skill para (A) **construir do zero** ou (B) **auditar** modelos de valuation de QUALQUER
empresa brasileira listada. Destilado do método do autor (PM buy-side): mesmas
boas práticas da skill de infra (br-infra-equity-model), sem os módulos setoriais.
Empresas de energia elétrica/utilities → usar a br-infra-equity-model.

## Primeira rodada e configuração — SEMPRE antes do Passo 0

Esta skill foi feita para o **Claude Code**: precisa de terminal e de arquivos locais.
Caminhos `scripts/`, `references/` e `assets/` citados aqui são relativos a
`${CLAUDE_PLUGIN_ROOT}/skills/br-equity-model-builder/`. As pastas de trabalho ficam num arquivo de
configuração compartilhado pelas skills do pacote `models-equity-br`. Antes de
qualquer outra coisa, rodar (no Windows, `python` ou `py` no lugar de `python3`):

    python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-equity-model-builder/scripts/config.py" status

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
  `python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-equity-model-builder/scripts/config.py" set --pasta-ri "..." --pasta-fundamentos "..." --pasta-saida "..."`
  (`--criar` só se o usuário pediu para criar pastas novas; `--pasta-fundamentos ""`
  se não houver). Depois rodar `python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-equity-model-builder/scripts/config.py" deps` e informar ao usuário:
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
   SEMPRE, logo no início: *"você tem uma planilha de fundamentos/dados históricos da
   companhia? Me passe o caminho do arquivo."* Se tiver, ela é a fonte primária do
   histórico. Inventariar `<pasta_ri>/<Empresa>` ANTES de buscar na web. Para a aba Trimestral: o release de CADA trimestre (não há atalho).
   **CONTEXTO OBRIGATÓRIO — ler 4 documentos ANTES de modelar** (dão guidance, o bridge
   de recorrência oficial, o critério de covenant e o tom da tese):
   (1) press release ANUAL do último exercício (4Txx); (2) DFP do último exercício;
   (3) ÚLTIMO press release trimestral; (4) última APRESENTAÇÃO de resultados.
   Se não localizar algum, PEDIR ao usuário; se ele não quiser fornecer, declarar a
   lacuna e seguir. Se a companhia publica DATABOOK oficial ("Base de Dados"/planilha
   de fundamentos própria), inventariar TODAS as abas (guidance, extraordinários,
   composição acionária, aberturas operacionais) ANTES de fixar premissas — guidance
   da companhia > estimativa própria.
2. **Perguntas iniciais** (uma mensagem só; **TODA pergunta vem com default sugerido** —
   ajuda o usuário a pensar nas possibilidades; NUNCA assumir sem perguntar):
   (a) IPCA de longo prazo (default 4,0%);
   (b) Ke nominal (default 12%);
   (c) perímetro/segmentos: quais linhas de negócio existem? **Mapear TODOS os
       segmentos, mesmo os pequenos**, e definir com o usuário o DRIVER de projeção de
       cada um (volume x preço x margem; lojas x vendas/loja; carteira x spread; etc.);
   (d) anos de histórico (default: 3 últimos anos anuais; mínimo 2) — e se houve
       **M&A no período** (se sim, coluna proforma);
   (e) horizonte explícito (default 10 anos) e perpetuidade **going concern**:
       g nominal da perpetuidade (default = IPCA; g real > 0 só com justificativa);
   (f) impostos — default sugerido: alíquota **EFETIVA** (IR/EBT do último ano cheio,
       consolidada ou por segmento se divulgado; embute JCP e presumido); alternativa:
       34% estatutária;
   (g) dividendos — **arquitetura: o DIVIDENDO é a política; a dívida líquida é a
       RESULTANTE** (roll-forward). payout mínimo = política divulgada da companhia;
       **default sem política: 25% (mínimo legal, art. 202 da Lei 6.404; JCP conta;
       base = LL ajustado)** + sweep ao alvo de alavancagem (divulgado pela companhia;
       senão ND/EBITDA atual se ≤ 3,5x, ou 3,5x com convergência em 3 anos). Fórmulas
       no build_playbook.
3. **Arquitetura** — propor abas, blocos por segmento, fontes por linha, e ESPERAR o ok
   explícito antes de escrever qualquer código.
4. **Construção** — ler `references/build_playbook.md` (padrões técnicos, calibração,
   bridges, dívida/dividendos, bridge do valuation, Multiplos, Trimestral enriquecida,
   armadilhas de execução).
5. **Verificação** — `scripts/verify_model.py`: recálculo LibreOffice com gate de ZERO
   erros de fórmula + checks de coerência. Nunca entregar sem passar.
6. **Entrega** — Excel com fórmulas vivas, salvo em `pasta_saida` (informar o caminho
   completo) + resumo com conclusões na régua **TIR real
   (Fisher) vs NTN-B longa** e reconciliação quantificada (R$/ação e p.p. de TIR)
   contra as premissas do usuário, item a item. Declarar TODO atalho de projeção usado
   e toda pendência de dado.

## Regras de ouro (resumo — detalhes nos references)

- Fisher SEMPRE (nunca subtração aritmética de inflação). XNPV/XIRR com datas reais;
  ano corrente fracionado; demais fluxos em meio de ano. Data de valuation em célula própria.
- **Projetar por DRIVER, não por inflação**: cada segmento tem seu decompositor (volume
  x preço x margem etc.). Se para algum segmento não houver dado que sustente a
  decomposição, crescer por inflação É aceitável — mas AVISAR explicitamente no output
  da entrega e no LeiaMe (qual segmento, por quê).
- **EBITDA recorrente = base de trabalho**: expurgar itens NÃO RECORRENTES e NÃO-CAIXA
  do EBITDA (equivalência patrimonial, marcação a mercado/valor justo, baixas,
  provisões extraordinárias, atualizações contábeis de ativos), QUANDO POSSÍVEL
  identificá-los (bridge oficial do release é a fonte). O EBITDA reportado aparece
  sempre como linha de REFERÊNCIA — nunca como base de calibração, alavancagem,
  dividendos ou múltiplos.
- Cores: azul = input; preto = fórmula; verde = link entre abas. Nomes definidos para
  premissas. Comentário com FONTE e derivação em toda célula de input. R$ mn, anual.
- Histórico lado a lado com a projeção, nas MESMAS linhas. DOIS bridges obrigatórios
  (Historico anual E Trimestral): (i) soma dos segmentos → consolidado (plug de
  holding/eliminações documentado); (ii) reportado → RECORRENTE (EBITDA e lucro
  líquido, com IR sobre os ajustes) — verificando se o recorrente divulgado parte do
  CONSOLIDADO ou do atribuível aos controladores (reportar sempre o atribuível).
- NUNCA anualizar um trimestre para calibrar linha sazonal (varejo/4T, agro/safra,
  educação/captação). Calibrar no ano cheio mais recente; trimestre é só check.
- Minoritários: deduzir a **book value** (não capitalizar lucros; anotar o viés);
  quasi-equity (PNs bancárias em holdings intermediárias): ver build_playbook.
- Coerência TIR ↔ valuation: se upside < 0, a TIR implícita TEM de ser < Ke (tolerância
  quando |upside| < ~5% com alavancagem alta — ver playbook). Se não fechar, LISTAR o
  porquê na entrega.
- **Perpetuidade going concern**: NUNCA ancorar em ano distorcido (pico/vale de capex,
  ano de transição) — usar ano normalizado DECLARADO; g default = IPCA.
- Aba Trimestral (versão enriquecida) e aba **Multiplos** são entregáveis padrão —
  specs no build_playbook; template em `assets/example_multiples.xlsx`.
- Alavancagem SEMPRE sobre EBITDA recorrente; distinguir covenant oficial do critério
  analítico, rotulando qual está no alvo da política de dividendos.
- Upside não modelado e atalhos de projeção usados: listados no LeiaMe — nunca
  silenciosamente no fluxo.

## Scripts

- `scripts/helpers_template.py` — col(), w(), sec(), estilos e formatos padronizados.
- `scripts/verify_model.py` — recalc + gate zero erros + checks de coerência e de
  itens não-caixa/não recorrentes no EBITDA.
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
