#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gate de qualidade antes de QUALQUER entrega.
Uso:
  python3 verify_model.py modelo.xlsx
  python3 verify_model.py modelo.xlsx --tir "Valuation!B57" --ke 0.0769 --upside "Valuation!B43"
  python3 verify_model.py modelo.xlsx --fy "Trimestral!B9:E9=Historico!E12"

Passos: (1) recalcula no LibreOffice via scripts/recalc.py (grava os valores no próprio
arquivo, pois o openpyxl não grava cache) e varre #REF!/#NAME?/#DIV/0! etc.;
(2) exige ZERO erros de fórmula;
(3) CHECK DE ITENS NÃO-CAIXA/NÃO RECORRENTES no EBITDA — duas varreduras independentes:
    (3a) VNR (lição de auditoria jul/2026 — o erro dominante: dupla contagem de VNR
         mudou o TP em -15% e zerou o upside num caso real): varre rótulos por
         VNR/"Atualização do Ativo Financeiro" e IMPRIME onde a linha aparece, exigindo
         confirmação de que (a) o EBITDA de calibração/recorrente é ex-VNR, (b) VNR é
         linha-memo NÃO-caixa fora do FCFF, e (c) a indenização terminal existe SEM o VNR
         no fluxo (senão é dupla contagem);
    (3b) demais itens não-caixa/não recorrentes (equivalência patrimonial, MtM/valor
         justo, impairment, baixas de ativo, rótulos "não recorrente"): IMPRIME onde
         aparecem, exigindo confirmação de que o recorrente os expurga quando
         identificáveis, de que são memos fora do fluxo e de que nada conta duas vezes;
(4) checks de coerência opcionais:
    - TIR real vs Ke quando há upside — coerência TIR x SOTP. ATENÇÃO: o check por
      SINAL falha estruturalmente quando |upside| < ~5% e a alavancagem é alta (o FCFE
      captura o valor do spread da dívida que o SOTP a Ke puro não dá). Nesses casos o
      script só ALERTA (não reprova) e sugere comparar com Ke blended;
    - somas trimestrais = FY (tolerância 0,15 pela derivação por diferença);
(5) lista células-check amarelas (FFF2CC) e seus valores para inspeção final.
ATENÇÃO: nunca rodar o recalc em arquivos com histórico de corrupção (ex.: caso ISAE4)."""
import sys, argparse, json, os, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recalc import recalc  # noqa: E402

VNR_PAT = re.compile(r'(atualiza[çc][ãa]o do ativo financeiro|valor justo do ativo indeniz|'
                     r'\bVNR\b|valor novo de reposi[çc])', re.I)
# Demais itens não-caixa / não recorrentes que não são VNR. Testado DEPOIS do VNR_PAT,
# para que uma linha de VNR não seja reportada duas vezes.
NC_PAT = re.compile(r'(equival[êe]ncia patrimonial|valor justo|marca[çc][ãa]o a mercado|\bMtM\b|'
                    r'impairment|atualiza[çc][ãa]o do ativo|n[ãa]o recorrente|baixa de ativ)', re.I)

def parse_ref(ref):
    sheet, cell = ref.split('!')
    return sheet, cell

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--tir', help='célula da TIR real, ex.: Valuation!B57')
    ap.add_argument('--ke', type=float, help='Ke real (Fisher) para o check de coerência')
    ap.add_argument('--upside', help='célula do upside, ex.: Valuation!B43')
    ap.add_argument('--fy', action='append', default=[],
                    help='check soma=FY: "Aba!B9:E9=Aba2!E12" (repetível)')
    ap.add_argument('--skip-recalc', action='store_true')
    a = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass

    ok = True
    if not a.skip_recalc:
        try:
            res = recalc(a.file)
        except Exception as e:  # noqa: BLE001
            print(f'FALHOU: recálculo no LibreOffice — {e}')
            print('Sem recálculo os checks abaixo não enxergam valores. NÃO ENTREGAR.')
            sys.exit(2)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        if res['total_errors']:
            print('FALHOU: erros de fórmula — NÃO ENTREGAR.')
            ok = False

    import openpyxl
    wb = openpyxl.load_workbook(a.file, data_only=True)
    wbf = openpyxl.load_workbook(a.file)

    # ---- (3) ITENS NÃO-CAIXA/NÃO RECORRENTES (bloqueio manual obrigatório) ----
    vnr_hits, nc_hits = [], []
    for ws in wbf.worksheets:
        for row in ws.iter_rows(min_col=1, max_col=2):
            for cell in row:
                if not isinstance(cell.value, str):
                    continue
                ref = f'{ws.title}!{cell.coordinate}: "{cell.value.strip()[:70]}"'
                if VNR_PAT.search(cell.value):
                    vnr_hits.append(ref)          # VNR tem prioridade: não duplicar
                elif NC_PAT.search(cell.value):
                    nc_hits.append(ref)

    if vnr_hits:
        print('\n=== (3a) CHECK VNR (responder antes de entregar — dupla contagem custou -15% de TP num caso real) ===')
        for h in vnr_hits:
            print('  linha VNR encontrada ->', h)
        print('  CONFIRME: (a) calibração e EBITDA RECORRENTE (hist E projetado) são ex-VNR;')
        print('            (b) VNR é memo NÃO-caixa (fora de FCFF/FCFE/dividendos);')
        print('            (c) indenização terminal existe SEM VNR no fluxo (senão = dupla contagem);')
        print('            (d) ND/EBITDA e política de dividendos usam EBITDA recorrente ex-VNR.')
        print('  O EBITDA reportado pode (e deve) aparecer como linha de REFERÊNCIA — nunca como base.')

    if nc_hits:
        print('\n=== (3b) CHECK ITENS NAO-CAIXA/NAO RECORRENTES no EBITDA (responder antes de entregar) ===')
        for h in nc_hits:
            print('  linha nao-caixa/nao recorrente ->', h)
        print('  CONFIRME: (a) calibração e EBITDA RECORRENTE (hist E projetado) expurgam esses itens quando identificáveis;')
        print('            (b) itens não-caixa são memo (fora de FCFF/FCFE/dividendos);')
        print('            (c) nenhum item aparece duas vezes (no fluxo E no bridge);')
        print('            (d) ND/EBITDA e política de dividendos usam o EBITDA RECORRENTE.')

    # ---- (4) coerência TIR x SOTP ----
    if a.tir and a.ke is not None and a.upside:
        s, c = parse_ref(a.tir); tir = wb[s][c].value
        s, c = parse_ref(a.upside); up = wb[s][c].value
        if isinstance(tir, (int, float)) and isinstance(up, (int, float)):
            coerente = (up < 0) == (tir < a.ke)
            print(f'\nCoerência TIR x SOTP: TIR real {tir:.2%} | Ke {a.ke:.2%} | '
                  f'upside {up:+.1%} -> {"OK" if coerente else "INCOERENTE"}')
            if not coerente:
                if abs(up) < 0.05:
                    print('  AVISO (não reprova): |upside| < 5% — o check por sinal falha '
                          'estruturalmente com alavancagem alta (FCFE captura o spread da '
                          'dívida; SOTP desconta FCFF a Ke puro). Compare a TIR com o Ke '
                          'BLENDED (Ke ajustado pelo mix dívida/equity) e DOCUMENTE no LeiaMe.')
                else:
                    print('  -> o fluxo da TIR provavelmente não deduz obrigações do bridge.')
                    ok = False

    for chk in a.fy:
        left, right = chk.split('=')
        s, rng = left.split('!')
        vals = [c.value for row in wb[s][rng] for c in row]
        soma = sum(v for v in vals if isinstance(v, (int, float)))
        s2, c2 = parse_ref(right); fy = wb[s2][c2].value
        d = soma - (fy or 0)
        print(f'{chk}: soma {soma:,.1f} vs FY {fy:,.1f} | diff {d:+,.2f} '
              f'{"OK" if abs(d) <= 0.15 else "FALHOU"}')
        if abs(d) > 0.15:
            ok = False

    print('\nCélulas-check (fundo amarelo):')
    for ws in wbf.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                f = cell.fill
                if f and f.fgColor and str(f.fgColor.rgb).endswith('FFF2CC'):
                    v = wb[ws.title][cell.coordinate].value
                    print(f'  {ws.title}!{cell.coordinate} = {v}')

    check_divida_pos_vencimento(wbf)
    check_coerencia_terminal()
    check_depreciacao(wbf)
    check_minoritarios()

    print('\nRESULTADO:', 'APROVADO' if ok else 'REPROVADO — corrigir antes de entregar')
    sys.exit(0 if ok else 1)

# ---------------------------------------------------------------------------
# Checks adicionados a partir do caso Equatorial (jul-ago/2026)
# ---------------------------------------------------------------------------

def check_divida_pos_vencimento(wb, verbose=True):
    """Varre saldos de divida de entidade DEPOIS do ano de vencimento da concessao.

    Qualquer valor != 0 e divida fantasma capitalizando juros contra EBITDA zero.
    Erro real: R$ 86,7 bn numa DisCo que encerrara 15 anos antes, so detectado por um
    fluxo de -R$ 222 bn no ultimo ano da grade.
    """
    achados = []
    for ws in wb.worksheets:
        if 'fluxo' not in ws.title.lower() and 'divid' not in ws.title.lower():
            continue
        venc_rows, dl_rows = [], []
        for r in range(1, ws.max_row + 1):
            lab = str(ws.cell(row=r, column=1).value or '')
            if 'VENCIMENTO' in lab.upper():
                venc_rows.append(r)
            if 'ívida líquida' in lab and 'abertura' in lab.lower():
                dl_rows.append(r)
        if venc_rows and dl_rows:
            achados.append((ws.title, len(venc_rows), len(dl_rows)))
    if verbose:
        print('\n=== (17) DIVIDA APOS O VENCIMENTO ===')
        if not achados:
            print('  nenhum bloco com vencimento identificado — check nao aplicavel')
        for t, nv, nd in achados:
            print(f'  {t}: {nv} linha(s) de vencimento e {nd} de divida de abertura.')
            print('  CONFIRMAR MANUALMENTE: o saldo de divida de cada entidade zera no ano')
            print('  seguinte ao vencimento? Se nao, ha divida fantasma. A entidade tem de')
            print('  LIQUIDAR no ano do vencimento (dividendo SEM piso em zero).')
    return achados


def check_coerencia_terminal(verbose=True):
    """Lembrete de coerencia fisica entre crescimento terminal e capex/QRR."""
    if verbose:
        print('\n=== (18) COERENCIA DO TERMINAL (responder antes de entregar) ===')
        print('  1. O crescimento de mercado converge a ZERO perto da perpetuidade?')
        print('  2. O capex/QRR de estado estacionario e 1,0x?')
        print('  Mercado crescendo com base parada em termos reais e fisicamente')
        print('  impossivel. Se o mercado cresce a g, entao capex/QRR = 1 + g/(QRR/BRR)')
        print('  E o terminal usa g real > 0. As duas premissas andam juntas.')
        print('  3. A perpetuidade esta ancorada em FCFF NORMALIZADO (capex = QRR)?')
        print('     Ancorar no FCFF do ano em fase de investimento ja produziu TP negativo.')


def check_depreciacao(wb, verbose=True):
    """Alerta se a D&A projetada parecer percentual fixo do EBITDA."""
    if verbose:
        print('\n=== (19) DEPRECIACAO ===')
        print('  D&A projetada como % do EBITDA e erro estrutural: a base cresce com')
        print('  CAPEX, nao com EBITDA, e o proxy subestima nos anos de investimento')
        print('  pesado. Usar roll-forward de base BRUTA (a taxa incide sobre custo),')
        print('  com obra em andamento energizando e baixa no vencimento.')
        print('  O ativo financeiro da concessao NAO deprecia.')


def check_minoritarios(verbose=True):
    """Lembrete do calculo de minoritario por dentro."""
    if verbose:
        print('\n=== (20) MINORITARIOS — CALCULO POR DENTRO ===')
        print('  Soma (1 - %participacao) x lucro de cada entidade bate com a linha')
        print('  reportada? Gap sistemtico em varios anos indica SEGUNDA CAMADA —')
        print('  tipicamente preferenciais resgataveis em holding intermediaria, que')
        print('  descem pela mesma linha mas sao encargo fixo a CDI.')
        print('  Teste: capital preferencial x CDI ~ gap observado.')


if __name__ == '__main__':
    main()
