# models-equity-br

**Claude Code** skills to build and audit equity models, in Excel with live formulas,
for Brazilian listed companies.

| Skill | Use it for |
|---|---|
| `br-equity-model-builder` | Any Brazilian listed company (except infrastructure/utilities). |
| `br-infra-equity-model` | Infrastructure and utilities: generation, transmission, distribution, energy trading. |

Claude Code picks the right skill from the request ("build the model for TAEE11",
"audit this model: <file path>"). Both follow the same method: a source hierarchy for
data collection, assumption questions with a suggested default for each, explicit
approval before any code is written, driver-based projections, real IRR (Fisher)
against the long NTN-B, and a verification gate (LibreOffice recalculation with zero
formula errors) before anything is delivered.

The skills' instructions are written in Portuguese, and Claude answers in Portuguese by
default.

## Requirements

- [Claude Code](https://code.claude.com). The skills are not designed for the claude.ai chat.
- Python 3.8+ with `openpyxl` (`pip install openpyxl`).
- [LibreOffice](https://www.libreoffice.org/download/), to recalculate and verify models.
- `pdftotext` (Poppler package), to read earnings releases and financial statements in PDF.
- Optional, only to download investor-relations documents automatically:
  `pip install selenium requests` and Google Chrome.

On the first run the skill checks all of this and lists what is missing.

## Installation

1. Get read access to this repository on GitHub and make sure git is authenticated on
   your machine (for example, `gh auth login`).
2. In Claude Code:

   ```
   /plugin marketplace add <owner>/models-equity-br
   /plugin install models-equity-br@models-equity-br
   ```

   Replace `<owner>` with the GitHub account or organization that hosts the repository.

3. To get updates: `/plugin marketplace update models-equity-br`.

## First run

The first time either skill runs, it says it was built for Claude Code and creates a
configuration file with three folders:

| Field | What it is |
|---|---|
| `pasta_ri` | Investor-relations documents, one subfolder per company (releases, ITR/DFP, presentations). The IR importer saves here. |
| `pasta_fundamentos` | Fundamentals / historical data spreadsheets (optional). |
| `pasta_saida` | Where models are saved. |

The file lives at `~/.claude/models-equity-br/config.json` and is shared by both skills.
Synced folders (Google Drive, OneDrive, Dropbox) work like any local folder. To change it
later, run `/models-equity-br:configurar` or edit the file. To use a different file, set
the `MODELS_EQUITY_BR_CONFIG` environment variable.

## Testing

For maintainers, after cloning:

```bash
# 1. scripts: configuration, recalculation and verify_model (never touches your real configuration)
python3 tools/smoke_test.py

# 2. no names, paths or metadata that would prevent sharing
python3 tools/check_sanitized.py

# 3. plugin manifests
claude plugin validate .
```

To try the skills for real without installing the plugin and without touching your
configuration:

```bash
# macOS / Linux
MODELS_EQUITY_BR_CONFIG=/tmp/test/config.json claude --plugin-dir ./plugins/models-equity-br
```

```powershell
# Windows (PowerShell)
$env:MODELS_EQUITY_BR_CONFIG="$env:TEMP\test\config.json"; claude --plugin-dir .\plugins\models-equity-br
```

Suggested script inside that session:

1. **First run:** ask "build the model for TAEE11". Expected: the notice that the skill
   is built for Claude Code, the three folder questions, the file being created and the
   dependency list. No questions about the company before that.
2. **Second run:** exit, start again with the same command and repeat the request.
   Expected: it does not ask for the folders again.
3. **Skill choice:** ask for a non-infrastructure company (e.g. "model for LREN3").
   Expected: `br-equity-model-builder`.
4. **Audit:** "audit this model: <path to one of your models>". Expected: audit mode,
   with no assumption questions.
5. **Verification:** run `verify_model.py` on a finished model:
   `python3 plugins/models-equity-br/skills/br-infra-equity-model/scripts/verify_model.py <model.xlsx>`.
   It recalculates the file in LibreOffice and writes the values back into it, so use a
   copy.
6. **Configuration command:** `/models-equity-br:configurar` shows the folders and lets
   you change them.

The strongest test is to rebuild a model you already know and compare the numbers.

## Sanitization check

`tools/check_sanitized.py` runs on GitHub on every push and fails if it finds:

- absolute machine or network paths;
- email addresses;
- external links and author metadata inside Office files;
- diverging copies of the scripts shared between the skills;
- **blocked terms** (company names, people, etc.).

The list of blocked terms is not stored in the code. It comes from the repository
secret `SANITIZE_BLOCKLIST` (Settings → Secrets and variables → Actions), one regular
expression per line. Locally, use a `.sanitize-blocklist` file at the repository root,
which git ignores.

## Layout

```
.claude-plugin/marketplace.json        plugin catalog
plugins/models-equity-br/
  .claude-plugin/plugin.json           manifest
  commands/configurar.md               /models-equity-br:configurar
  skills/br-equity-model-builder/      SKILL.md, references/, scripts/, assets/
  skills/br-infra-equity-model/        same structure
tools/                                 tests and sanitization check
```

The scripts `config.py`, `recalc.py`, `ir_importer.py` and `helpers_template.py` exist as
identical copies in both skills, so each skill works on its own. When you change one,
copy it to the other (the sanitization check flags any difference).

## Rights

All rights reserved. Use by permission only.
