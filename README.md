# models-equity-br

Skills do **Claude Code** para construir e auditar modelos de equity, em Excel com
fórmulas vivas, de empresas brasileiras listadas.

| Skill | Para quê |
|---|---|
| `br-equity-model-builder` | Qualquer empresa brasileira listada (exceto infraestrutura/utilities). |
| `br-infra-equity-model` | Infraestrutura e utilities: geração, transmissão, distribuição, comercialização. |

O Claude Code escolhe a skill sozinho pelo pedido ("monta o modelo da TAEE11",
"audita este modelo: <caminho do arquivo>"). As duas seguem o mesmo método: coleta de
fontes com hierarquia, perguntas de premissas com default sugerido, aprovação explícita
antes de escrever código, projeção por driver, TIR real (Fisher) contra NTN-B longa e um
gate de verificação (recálculo no LibreOffice com zero erros de fórmula) antes de
qualquer entrega.

## Requisitos

- [Claude Code](https://code.claude.com) (as skills não foram feitas para o chat do claude.ai).
- Python 3.8+ com `openpyxl` (`pip install openpyxl`).
- [LibreOffice](https://www.libreoffice.org/download/), para recalcular e verificar os modelos.
- `pdftotext` (pacote Poppler), para ler releases e DFs em PDF.
- Opcional, só para baixar documentos de RI automaticamente:
  `pip install selenium requests` e o Google Chrome.

Na primeira rodada a skill confere tudo isso e diz o que falta.

## Instalação

1. Tenha acesso de leitura a este repositório no GitHub e o git autenticado na máquina
   (por exemplo, `gh auth login`).
2. No Claude Code:

   ```
   /plugin marketplace add <dono>/models-equity-br
   /plugin install models-equity-br@models-equity-br
   ```

   Troque `<dono>` pela conta ou organização do GitHub onde o repositório está.

3. Para receber atualizações: `/plugin marketplace update models-equity-br`.

## Primeira rodada

Na primeira vez que uma das skills roda, ela avisa que foi feita para o Claude Code e
cria um arquivo de configuração com três pastas:

| Campo | O que é |
|---|---|
| `pasta_ri` | Documentos de RI, uma subpasta por empresa (releases, ITR/DFP, apresentações). O importador de RI salva aqui. |
| `pasta_fundamentos` | Planilhas de fundamentos / dados históricos (opcional). |
| `pasta_saida` | Onde os modelos são salvos. |

O arquivo fica em `~/.claude/models-equity-br/config.json` e vale para as duas skills.
Pastas sincronizadas (Google Drive, OneDrive, Dropbox) funcionam como qualquer pasta
local. Para mudar depois: `/models-equity-br:configurar`, ou edite o arquivo. Para usar
outro arquivo, defina a variável de ambiente `MODELS_EQUITY_BR_CONFIG`.

## Como testar

Para quem mantém o repositório, depois de clonar:

```bash
# 1. scripts: configuração, recálculo e verify_model (não mexe na sua configuração real)
python3 tools/smoke_test.py

# 2. nada de nomes, caminhos ou metadados que impeçam compartilhar
python3 tools/check_sanitized.py

# 3. manifests do plugin
claude plugin validate .
```

Para testar as skills de verdade sem instalar o plugin e sem tocar na sua configuração:

```bash
# macOS / Linux
MODELS_EQUITY_BR_CONFIG=/tmp/teste/config.json claude --plugin-dir ./plugins/models-equity-br
```

```powershell
# Windows (PowerShell)
$env:MODELS_EQUITY_BR_CONFIG="$env:TEMP\teste\config.json"; claude --plugin-dir .\plugins\models-equity-br
```

Roteiro sugerido dentro dessa sessão:

1. **Primeira rodada:** peça "quero montar o modelo da TAEE11". Esperado: o aviso de que a
   skill é para o Claude Code, as três perguntas de pasta, o arquivo criado e a lista de
   dependências. Nenhuma pergunta sobre a empresa antes disso.
2. **Segunda rodada:** feche, abra de novo com o mesmo comando e repita o pedido.
   Esperado: não pergunta as pastas de novo.
3. **Escolha da skill:** peça uma empresa não-infra (ex.: "modelo da LREN3"). Esperado:
   `br-equity-model-builder`.
4. **Auditoria:** "audita este modelo: <caminho de um modelo seu>". Esperado: modo
   auditoria, sem perguntas de premissas.
5. **Verificação:** rode `verify_model.py` num modelo já pronto:
   `python3 plugins/models-equity-br/skills/br-infra-equity-model/scripts/verify_model.py <modelo.xlsx>`.
   Ele recalcula o arquivo no LibreOffice e grava os valores nele, então use uma cópia.
6. **Comando de configuração:** `/models-equity-br:configurar` mostra as pastas e deixa
   trocar.

O teste mais forte é refazer um modelo que você já conhece e comparar os números.

## Trava de sanitização

`tools/check_sanitized.py` roda no GitHub a cada push e falha se encontrar:

- caminhos absolutos de máquina ou de rede;
- e-mails;
- links externos e metadados de autor dentro de arquivos do Office;
- cópias divergentes dos scripts compartilhados entre as skills;
- os **termos proibidos** (nomes de empresa, pessoas etc.).

A lista de termos não fica no código. Ela vem do segredo `SANITIZE_BLOCKLIST` do
repositório (Settings → Secrets and variables → Actions), uma expressão regular por
linha. Localmente, use um arquivo `.sanitize-blocklist` na raiz, que o git ignora.

## Estrutura

```
.claude-plugin/marketplace.json        catálogo do plugin
plugins/models-equity-br/
  .claude-plugin/plugin.json           manifesto
  commands/configurar.md               /models-equity-br:configurar
  skills/br-equity-model-builder/      SKILL.md, references/, scripts/, assets/
  skills/br-infra-equity-model/        idem
tools/                                 testes e trava de sanitização
```

Os scripts `config.py`, `recalc.py`, `ir_importer.py` e `helpers_template.py` existem
em cópias idênticas nas duas skills, para cada uma funcionar sozinha. Ao alterar um,
copie para a outra (a trava acusa divergência).

## Direitos

Todos os direitos reservados. Uso mediante autorização.
