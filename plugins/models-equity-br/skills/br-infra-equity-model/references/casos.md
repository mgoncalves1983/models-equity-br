# Casos e evidências — ler sob demanda, não no caminho crítico

Material que justifica as regras bloqueantes. Consultar quando houver dúvida sobre o
PORQUÊ de uma regra, ou quando precisar convencer o usuário de que a regra importa.

## Obrigações especiais (regra 4)

Share médio 2023-25 do capex de distribuição, caso Equatorial:

| DisCo | OE / capex |
|---|---|
| Pará | 42,5% |
| CEA | 25,4% |
| Piauí | 14,2% |
| Maranhão | 5,3% |
| CEEE-D | 1,5% |
| Alagoas | 1,4% |
| Goiás | ~0% |

Tratar capex bruto como próprio inflava a BRR do Pará em ~R$ 1,4 bn/ano E afundava o
FCFF pelo mesmo valor — erro nos dois sentidos ao mesmo tempo. Consolidado: R$ 1.855 mn
de OE sobre R$ 10.639 mn de capex de distribuição em 2025.

## CAOM cresce com a rede (regra 6)

Onze revisões tarifárias das distribuidoras da Equatorial, 2013-2025, CAOM homologado vs
IPCA acumulado do ciclo:

| DisCo | Ciclo | CAOM real | Mercado | β implícito |
|---|---|---|---|---|
| Maranhão | 2013-17 | +14,8% | +20,8% | 0,71 |
| Maranhão | 2017-21 | +3,5% | +11,2% | 0,31 |
| Maranhão | 2021-25 | +11,3% | +24,0% | 0,47 |
| Pará | 2015-19 | +6,8% | +6,6% | 1,03 |
| Pará | 2019-23 | **+48,0%** | +17,1% | *2,81* |
| Piauí | 2013-23 | +16,5% | +39,7% | 0,42 |
| Alagoas | 2013-24 | +12,6% | +31,6% | 0,40 |
| **CEEE-D** | **2016-21** | **−8,9%** | **−5,5%** | 1,62 |
| CEA | 2017-23 | +3,3% | +4,0% | 0,83 |
| Goiás | 2013-18 | +5,0% | +15,4% | 0,32 |
| Goiás | 2018-23 | +15,5% | +10,5% | 1,48 |

**Subiu em termos reais em 10 de 11.** Mediana ex-outlier: β = 0,47. A única queda foi
CEEE-D, cujo mercado encolheu — a exceção confirma a regra de que o benchmark acompanha a
escala física nos dois sentidos.

O Pará de 2023 é o precedente de revisão pós-privatização com universalização amazônica:
+48% real, β de 2,81. Excluir da calibração, mas registrar como evidência de upside em
ativos de turnaround.

Nota de fase: o CAOM cresce em termos ABSOLUTOS mas cai por unidade de escala — Maranhão
2021-25 teve CAOM/MWh caindo 10% real. É assim que a eficiência volta para a tarifa, e é
por isso que β < 1.

## Mercado Fio B vs energia faturada (regra 7)

Equatorial, 1S26 vs 1S25:

| DisCo | Energia faturada | Mercado Fio B | GD compensada |
|---|---|---|---|
| Goiás | **−1,4%** | **+3,6%** | +126% |
| Maranhão | +4,7% | +6,4% | +60% |
| Pará | +4,7% | +6,6% | +48% |
| CEEE-D | +0,5% | +1,5% | +90% |

Usar energia faturada como driver de CAOM subestimaria o crescimento da rede em quase 5
p.p. só em Goiás. Fonte: databook, abas Mercado Distribuição Pré e Pós CP09 — sobrepõem
no 4T24 e permitem medir a quebra metodológica (diferença < 1% em energia faturada).

## Fator X — componente Pd em revisão (regra 6, contexto)

Última revisão aprovada em 17/03/2020: Pd baseado na produtividade média do setor e no
crescimento de mercado, base 2013-2018, **sem capex como insumo**.

Tomada de Subsídios 12/2025 (set/2025) e AIR publicada em 25/06/2026 abriram consulta
pública em julho/2026. Cinco propostas: duas mantêm o status quo (uma preserva a fórmula
de 2013-2018, outra atualiza a base para 2018-2024); três incorporam TOTEX ou
produtividade total dos fatores. A proposta indicada pela ANEEL combina 50% de PTF
setorial e 50% individual, com captura dinâmica de CAPEX e OPEX.

Mecanismo: com CAPEX como insumo, quem investe pesado tem PTF medida menor, logo **Pd
menor e menos redução tarifária**. Sell-side aponta distribuidoras de capex intensivo
como beneficiárias. Manter Fator X como input azul anual e não travar no default.

## Perpetuidade ancorada em fase de investimento (regra 9)

Primeira versão do modelo Equatorial perpetuou o FCFF de 2040, que era negativo em várias
distribuidoras por estarem construindo base. Resultado: **preço-alvo de −R$ 79/ação**.
Corrigido com FCFF normalizado (capex = QRR), foi para R$ 22,80.

## Dívida fantasma no vencimento (regra 11)

O sweep a 3,1x deixa `3,1 × EBITDA` de dívida no ano do vencimento. Como o EBITDA vai a
zero no ano seguinte, essa dívida capitaliza juros indefinidamente. No caso real, Goiás
chegava a 2060 com **R$ 86,7 bn de dívida fantasma** tendo encerrado em 2045, e CEEE-D
com R$ 35,5 bn. O sintoma só apareceu como um fluxo de −R$ 222 bn no último ano da grade,
e contaminou toda a máquina de caixa consolidado por várias rodadas de diagnóstico.

## SOTP vs FCFE (regra 14)

Caso Equatorial, alavancagem de 4,4x a 5,6x, Kd nominal de 10,2% a 12,8% contra Ke de
12%: SOTP dava R$ 29,14/ação e VPL(FCFE @ Ke) dava R$ 46,89. **Diferença de R$ 22,3 bn**,
ou R$ 17,75/ação — é o benefício do endividamento que o SOTP descarta ao deduzir dívida a
valor de face.

Atenção ao efeito cruzado: alíquota efetiva baixa (SUDAM/SUDENE) REDUZ o benefício da
alavancagem, porque encolhe o escudo fiscal. Os dois incentivos competem pela mesma base.

## Payout sem teto (regra 17)

Sem teto, o sweep de alavancagem-alvo distribui toda a capacidade de dívida criada pelo
crescimento do EBITDA. Payout implícito no caso real: 106% em 2032, 132% em 2034, **148%
em 2044** — a companhia tomando dívida nova todo ano só para pagar dividendo.

Teto ancorado no realizado da companhia (R$ 1.987 mn de JCP sobre R$ 2.646 mn de lucro
ajustado = 75%) elimina o artefato.

Nota contraintuitiva: teto BAIXO retém mais e desalavanca mais rápido. Teto de 75%
perpétuo faz a alavancagem furar PARA BAIXO do alvo. Subir o teto na maturidade (para
100%) deixa o sweep SEGURAR no alvo em vez de continuar caindo.

## Minoritários em duas camadas (protocolo de auditoria)

Cálculo por dentro no caso Equatorial: Σ (1 − %EQTL) × lucro de cada DisCo = R$ 396 mn em
2025, contra R$ 826 mn reportados. Gap de R$ 430 mn em 2025, R$ 537 mn em 2024, R$ 296 mn
em 2023 — sistemático.

Diagnóstico: **preferenciais resgatáveis do Itaú na holding intermediária**. Sem opção de
venda (só a companhia tem a call), ficam em participação de não controladores no PL, e a
remuneração desce pela MESMA linha de minoritários. São naturezas diferentes somadas numa
linha só: minoritário de DisCo é proporcional ao lucro, PN é encargo fixo a CDI.

Teste de sanidade: R$ 4,4 bn de capital preferencial × CDI de ~11% em 2024 = R$ 484 mn,
contra gap observado de R$ 537 mn.

## Alíquota efetiva — três medidas divergem violentamente

Caso Equatorial, nota de conciliação IRPJ/CSLL e DFC consolidada:

| | 2025 | 2024 | Média 2 anos |
|---|---|---|---|
| Efetiva contábil | 17,2% | **−5,7%** (crédito) | 5,1% |
| Imposto corrente | 31,5% | 6,0% | 18,1% |
| **Imposto pago em caixa** | 22,9% | 8,7% | **15,4%** |

Volatilidade explicada por dois itens da própria nota: subvenção governamental de IRPJ
(R$ 680,9 mn em 2025, R$ 825,8 mn em 2024) e parcelamento de anos anteriores (R$ 469,1 mn
em 2024, não recorrente). Usar a de caixa como âncora e identificar o não recorrente.

## Custo de holding — três ancoragens

| Base | Valor 2025 | Avaliação |
|---|---|---|
| Controladora isolada (G&A + outras despesas) | R$ 266 mn | Estreita demais |
| **Segmento "Administração" da nota de segmentos** | **R$ 596 mn** | **Correta** |
| Idem, ex-não recorrentes | ~R$ 450 mn | Alternativa |

A nota de segmentos define: serviços de administração central da operação de holding mais
compartilhamento de pessoal e infraestrutura — abrange a holding de topo, a holding
intermediária e os veículos de participações. A DRE da controladora isolada pega só o
topo.

Eliminações intercompany da mesma nota: R$ 28,3 mn. Estimativa prévia de R$ 300 mn estava
10x alta.

## Lição de processo

Nesta sessão, seis rodadas consecutivas foram correção de efeito colateral da rodada
anterior, com o preço-alvo oscilando entre R$ 44,60 e R$ 149 sem que a tese mudasse.
Causa: uma trava de alavancagem consolidada construída sobre conta de caixa paralela, que
se contradiz quando o caixa fica grande.

Sinal de alerta: se duas correções seguidas geraram problema novo, o defeito é de
arquitetura. Parar e reavaliar em vez de corrigir o sintoma.
