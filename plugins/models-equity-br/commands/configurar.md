---
description: Mostra ou altera as pastas usadas pelas skills de modelos de equity (documentos de RI, planilhas de fundamentos e saída dos modelos).
---

O usuário quer ver ou alterar a configuração das skills de modelos de equity
(`br-equity-model-builder` e `br-infra-equity-model`). As duas usam o mesmo arquivo.
No Windows, usar `python` ou `py` no lugar de `python3`.

1. Rodar:

       python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-equity-model-builder/scripts/config.py" status

2. Mostrar ao usuário, em linguagem simples, onde está o arquivo de configuração e o
   valor atual de cada pasta:
   - **Pasta dos documentos de RI** (`pasta_ri`) — uma subpasta por empresa, com
     releases, ITR/DFP e apresentações; o importador de RI também salva aqui.
   - **Pasta das planilhas de fundamentos** (`pasta_fundamentos`, opcional).
   - **Pasta onde salvar os modelos** (`pasta_saida`).
   Se ainda não houver configuração, dizer que este é o primeiro uso e que o arquivo
   será criado agora.

3. Perguntar numa mensagem só o que mudar, com o valor atual como sugestão. Se o
   usuário disse em $ARGUMENTS o que quer mudar, usar isso e não perguntar de novo.

4. Gravar só o que mudou:

       python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-equity-model-builder/scripts/config.py" set --pasta-ri "..." --pasta-fundamentos "..." --pasta-saida "..."

   (`--criar` apenas se o usuário pediu para criar pastas novas; `--pasta-fundamentos ""`
   para deixar em branco.) Se o comando recusar uma pasta inexistente, mostrar o erro e
   perguntar se é para corrigir o caminho ou criar a pasta.

5. Rodar `python3 "${CLAUDE_PLUGIN_ROOT}/skills/br-equity-model-builder/scripts/config.py" deps`
   e terminar com: caminho do arquivo, valores gravados e dependências faltantes com o
   comando de instalação.
