# Protocolo de auditoria (modo AUDITORIA)

Não fazer perguntas de premissas (IPCA, Ke etc. saem do próprio modelo). Perguntar
apenas: qual é a variável de OUTPUT principal (se não for óbvia).

## Protocolo

1. **Partir do output** (ex.: `tir_eq_real`): localizar a célula pelo nome definido e
   verificar ANTES DE TUDO se é fórmula viva ou valor digitado.
2. **Mapear o grafo de dependências de trás para frente**: output → fluxos → linhas de
   FCF → EBITDA/juros/imposto/capex → inputs. Anotar o mapa (aba!célula por conceito).
3. **Rodar o checklist de erros clássicos** (abaixo) contra o mapa.
4. **Quantificar CADA erro isoladamente**: replicar o cálculo em Python (ler valores
   cacheados com `data_only=True`) e recomputar a métrica corrigindo UM erro por vez —
   reportar em p.p. de TIR ou R$/ação.
5. **Reconciliar** com o modelo independente (se houver): decompor a diferença total em
   premissas (defensáveis, listar) vs erros mecânicos (corrigir), item a item.
6. **Entregar**: mapa do modelo; erros numerados e quantificados; convergências (o que o
   modelo acerta — sempre listar); sugestões em ordem de urgência; comparação final.
   Tom: direto e respeitoso; opiniões rotuladas.

## Checklist de erros clássicos (validados em auditorias reais)

1. Nome definido de dívida líquida apontando para trimestre/coluna velha (ou série de
   entidade antiga pré-reorganização).
2. Timing de IRR: ano-fantasma com fluxo zero (INDEX em célula vazia); primeiro fluxo
   ancorado em ano passado (relógio de valuation velho) contra preço de tela atual —
   usar XIRR com datas.
3. Subtração aritmética de inflação em vez de Fisher.
4. Tabelas de sensibilidade coladas como valores (mortas) contradizendo o modelo vivo.
5. Múltiplos históricos com share count atual × preços não ajustados por
   desdobramento/bonificação.
6. Rótulo "ajustado" dividindo pelo número cheio (ou recorrente consolidado tratado
   como atribuível ao controlador).
7. NPV de segmento datado em ano antigo (fluxos já passados, que já estão na DL).
8. Cauda perpétua sem racional: perpetuidade ancorada em ano distorcido (pico/vale de
   capex, transição), g real alto sem justificativa, ou concessão/contrato com termo
   atravessado como se fosse perpétuo sem custo de renovação.
9. **Output hardcoded**: a variável-fim é um número digitado, desconectado do modelo
   (checar TODA célula de conclusão com `data_only=False`).
10. **Dupla contagem de desalavancagem**: juros caindo (dívida amortizando) SEM linha de
    amortização deduzida do FCFE. Regimes consistentes: (a) dívida rolada = juros
    constantes, sem amortização no fluxo; ou (b) cronograma real = juros caindo E
    principal deduzido.
11. **Crédito de IR caixa sobre EBT negativo** sem trava de 30% e sem exigir lucro
    tributável (prejuízo virando receita de caixa no ano).
12. **Quebra de unidade/sinal no meio de uma linha** (série que muda de R$ mn para
    R$ mil ou troca sinal a partir de certa coluna). Detectar: varrer razão entre
    células consecutivas de séries longas (saltos >100x).
13. **Inputs mortos e blocos legados**: nomes definidos sem NENHUMA referência de
    fórmula; blocos de era societária anterior convivendo com o vivo.
14. Calibração de linha sazonal por trimestre anualizado (varejo/4T, agro/safra,
    dividendos de participações).
15. **Incoerência TIR ↔ bridge**: TIR implícita > Ke com upside negativo (ou
    vice-versa) — o fluxo da TIR não deduz obrigações que o bridge deduz do estoque
    (ver a tolerância para |upside| < 5% com alavancagem alta no build_playbook).
16. Passivos fora do bridge: previdência (CPC33), litígios prováveis, arrendamentos
    (IFRS16, se fora da DL divulgada), quasi-equity/minoritários.
17. **Itens não-caixa/não recorrentes dentro do EBITDA-base** (equivalência, MtM/valor
    justo, baixas, provisões extraordinárias) alimentando calibração, alavancagem ou
    dividendos — o recorrente deve expurgá-los quando identificáveis.

## Ferramentas

- Duas leituras do arquivo: `load_workbook(f)` (fórmulas) + `load_workbook(f,
  data_only=True)` (valores cacheados). Cache divergente de fórmula editada sem
  recálculo = sinal de erro, reportar.
- Réplica do fluxo do IRR em Python (bisseção) para recomputar cenários corrigidos.
- Nunca modificar o arquivo do usuário; trabalhar em cópia.
