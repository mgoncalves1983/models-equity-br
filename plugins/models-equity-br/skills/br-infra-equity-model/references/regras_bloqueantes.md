# Regras bloqueantes — reler ANTES de cada módulo e ANTES de cada entrega

Uma tela. Se qualquer item aqui estiver violado, a entrega está errada — não é questão
de premissa. O material de contexto e as narrativas de caso estão em `casos.md`; leia
sob demanda, não no caminho crítico.

**Sessão longa decai.** Reler este arquivo (a) antes de escrever o primeiro código,
(b) antes de cada módulo novo, (c) antes de cada entrega e (d) depois de qualquer
compactação de contexto. Ler uma vez no início da sessão NÃO é suficiente — já falhou
em produção.

## Fontes

1. **Quatro documentos obrigatórios antes de modelar**: release anual do último
   exercício, DFP do último exercício, último release trimestral, última apresentação.
   Declarar no gate de premissas quais foram lidos e quais faltaram.
2. **Databook: inventariar TODAS as abas por nome antes de ir a PDF** — inclusive
   balanço, fluxo de caixa e apuração de IR, não só as operacionais. Um databook de 100+
   abas costuma conter o que se iria buscar na nota do DFP.
3. **Databook e release divergem por reapresentação.** Operação descontinuada faz a
   companhia reapresentar o release e não o databook. Cruzar TRIMESTRE A TRIMESTRE antes
   de confiar em qualquer série anual.

## Motor de distribuição

4. **Capex tem duas linhas: bruto e LÍQUIDO de obrigações especiais.** As OE são
   financiadas por consumidores e governo — não entram na BRR **nem na saída de caixa**.
   Extrair da aba de investimentos do databook, média de 3 anos.
5. **Reset de RTP ancorado na Parcela B VIGENTE, nunca remontado do zero.**
   `PB(t) = PB(t−1) × (1 + IPCA − X) + (BRR_atual − BRR_ref) × (WACC + QRR/BRR)
   + ganho de escala do CAOM`. A BRR de referência é a da última RTP indexada pelo
   **IPCA REALIZADO** (input próprio) e reseta a cada revisão.
6. **CAOM CRESCE com a rede — não leva haircut.** `CAOM_reset = CAOM_ref × (1+IPCA)^n ×
   (1 + β × g_mercado)^n`, β default **0,50**. Haircut de produtividade DUPLICA o Fator X
   e contraria o Submódulo 2.2, que manda ATUALIZAR o intervalo de custos operacionais
   pela variação de extensão de rede e número de consumidores.
7. **Driver de escala = Mercado Fio B** (energia faturada + GD compensada), nunca energia
   faturada. Cliente com geração própria fatura menos e continua usando a rede.
8. **Capex ancorado em múltiplo da QRR convergente**, nunca em nível real fixo. Nível
   fixo faz a base crescer sem limite e exigiria alta real insustentável da tarifa Fio B.

## Terminal e vencimento

9. **Perpetuidade SEMPRE sobre FCFF NORMALIZADO** (capex = QRR, crescimento real zero).
   Nunca sobre o FCFF do ano, que em fase de investimento é negativo.
10. **Coerência física do terminal**: mercado crescendo com base parada em termos reais é
    incoerente. **Default: crescimento de mercado converge a ZERO perto da perpetuidade e
    capex/QRR = 1,0x.** Avisar o usuário nos bullet points.
11. **Se modelar sem renovação, a entidade LIQUIDA no ano do vencimento**: dividendo sem
    piso em zero, dívida residual sai do bolso do acionista naquele ano, fluxo zero
    depois. Sem isso a dívida capitaliza juros contra EBITDA zero e o estrago só aparece
    décadas à frente.
12. **VNR ↔ indenização**: contar os dois é dupla contagem. Se renova, não há
    indenização; se não renova, modelar indenização e manter o VNR fora do EBITDA.
13. Verificar **aditivo de prorrogação assinado** (Decreto 12.068/2024) — renovação
    contratada é FATO, não premissa.

## Valuation

14. **Número principal = VPL(FCFE @ Ke).** SOTP (FCFF descontado a Ke com dívida deduzida
    a face) subestima o equity quando Kd < Ke — descarta o benefício do endividamento.
    Com alavancagem alta a diferença passa de 20% do equity. SOTP vira atribuição de
    valor por ativo.
15. **Não usar WACC** quando a alavancagem varia no horizonte: exige estrutura de capital
    constante. Se precisar de rigor formal, APV.
16. **Depreciação NUNCA como percentual do EBITDA.** Roll-forward de base BRUTA (a taxa
    incide sobre custo, não sobre líquido), com obra em andamento energizando e baixa no
    vencimento. **O ativo financeiro da concessão não deprecia.**

## Política de dividendos

17. `dividendo = MIN(teto × LL ; MAX(piso × LL ; sweep))` — três parâmetros azuis,
    editáveis por ano. **Sem teto, o sweep leva a companhia a se realavancar para
    distribuir** (payout de 148% em caso real).
18. **Piso default 25%** (art. 202) — mas VERIFICAR O ESTATUTO. A lei permite fixar
    abaixo desde que definido com precisão e sem sujeitar ao arbítrio dos
    administradores, e há companhia com 1%.

## Anti-padrão

19. **NÃO construir trava de alavancagem consolidada com conta de caixa paralela na
    holding.** Caixa que reduz a dívida líquida consolidada sem amortizar dívida nas
    entidades é aproximação aceitável enquanto é pequeno e se contradiz quando fica
    grande. Erros reais: duplo cômputo do caixa nos dois lados do teste, vaivém de
    dezenas de bilhões entre anos, aporte artificial de R$ 143 bn. Se precisar de
    restrição de financiamento: ou reescreve o roll-forward de dívida das entidades para
    receber amortização, ou deixa a alavancagem como LEITURA na aba dedicada sem
    realimentar o fluxo.
20. **Não empilhar remendo.** Se duas correções seguidas geraram efeito colateral novo,
    parar e reavaliar a arquitetura em vez de corrigir o sintoma.
