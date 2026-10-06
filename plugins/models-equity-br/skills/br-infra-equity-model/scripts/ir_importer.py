#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coletor de documentos de RI (implementação de referência).
Se o usuário tiver um importador próprio, USAR O DELE (costuma ser mais testado nos
portais reais).

O que faz: para portais de resultados em plataforma MZiQ (SPAs renderizadas em JS),
colhe os links de documentos por ano via Selenium headless (fase 1, leve) e depois
baixa via requests (fase 2, rápida), com dedupe, filtro de idioma PT e captura de
links de YouTube das teleconferências. NÃO interpreta os dados — apenas baixa arquivos.

Saída: <pasta_ri>/<Empresa>/, onde pasta_ri vem da configuração da skill
(scripts/config.py) — ou de --saida.
PRÉ-VOO: inventariar <pasta_ri>/<Empresa>/ e rodar SÓ para os períodos faltantes.

Uso:
  python3 ir_importer.py <Empresa> <ano> [<ano> ...] [--portal URL] [--saida DIR]
  ex.: python3 ir_importer.py Copel 2025 2026
       python3 ir_importer.py MinhaEmpresa 2026 --portal https://ri.exemplo.com.br/central-de-resultados/

Limitações: Cloudflare Turnstile pode bloquear renderizações repetidas (detecta e
pula; não burla). Usar pausas entre anos/empresas; em bloqueio persistente, rodar de
IP residencial. Cuidado com pkill -f chrome em shells cuja linha contenha 'chrome'
(mata o próprio shell — lição de guerra)."""
import argparse, json, os, re, sys, time, random
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config  # noqa: E402

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/125 Safari/537.36')
IR_PORTALS = {
    'Copel': 'https://ri.copel.com/informacoes-financeiras/central-de-resultados/',
    # adicionar: 'Empresa': 'url da central de resultados'
}
EN_KEYWORDS = ('english', 'earnings release', '_en', '-en.', 'ingles')
HARVEST_JS = """
const out=[]; document.querySelectorAll('a[href]').forEach(a=>{
  const h=a.href||'', t=(a.innerText||'').trim();
  if(/\\.(pdf|xlsx|zip|mp3)(\\?|$)/i.test(h) || h.includes('youtube')||h.includes('youtu.be'))
    out.push({href:h, text:t});
}); return out;"""


def _new_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    o = Options()
    for f in ('--headless=new', '--no-sandbox', '--disable-dev-shm-usage',
              f'--user-agent={UA}'):
        o.add_argument(f)
    return webdriver.Chrome(options=o)


def _select_year(driver, year):
    """Troca o ano no widget de resultados; nunca levanta exceção."""
    try:
        from selenium.webdriver.support.ui import Select
        from selenium.webdriver.common.by import By
        sels = driver.find_elements(By.TAG_NAME, 'select')
        for s in sels:
            try:
                Select(s).select_by_visible_text(str(year))
                return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def _harvest_year(driver, year, settle=6):
    """Colhe links do ano; devolve lista de {href, text}."""
    _select_year(driver, year)
    time.sleep(settle)
    items = driver.execute_script(HARVEST_JS) or []
    seen, out = set(), []
    for it in items:
        if it['href'] in seen:
            continue
        seen.add(it['href'])
        if any(k in (it['href'] + ' ' + it['text']).lower() for k in EN_KEYWORDS):
            continue
        out.append(it)
    return out


def _download_result_item(item, year, folder, yt_file, headers):
    href, text = item['href'], item['text']
    os.makedirs(folder, exist_ok=True)
    if 'youtube' in href or 'youtu.be' in href:
        with open(yt_file, 'a') as f:
            f.write(f'{year}\t{text}\t{href}\n')
        return ('yt', href)
    name = re.sub(r'[^\w\-. ]', '_', (text or href.split('/')[-1]))[:110]
    if not re.search(r'\.(pdf|xlsx|zip|mp3)$', name, re.I):
        name += os.path.splitext(href.split('?')[0])[1] or '.pdf'
    path = os.path.join(folder, f'{year}_{name}')
    if os.path.exists(path):
        return ('dup', path)
    try:
        r = requests.get(href, headers=headers, timeout=60)
        if r.status_code == 200 and len(r.content) > 5000:
            open(path, 'wb').write(r.content)
            return ('file', path)
    except Exception:
        pass
    return None


def run(company, years, out_root=None, portal=None):
    """Fase 1 (Selenium): colher links -> JSON. Fase 2 (requests): baixar."""
    out_root = out_root or config.get('pasta_ri')
    if not out_root:
        sys.exit('pasta_ri não configurada: rode config.py set (ou passe --saida).')
    portal = portal or IR_PORTALS.get(company)
    if not portal:
        sys.exit(f'Portal de RI de {company} desconhecido: passe --portal URL.')
    folder = os.path.join(out_root, company)
    os.makedirs(folder, exist_ok=True)
    yt = os.path.join(folder, f'{company}_YouTube_Links.txt')
    d = _new_driver()
    links = {}
    try:
        d.get(portal); time.sleep(6)
        for y in years:
            try:
                links[str(y)] = _harvest_year(d, y)
                print(y, '->', len(links[str(y)]), 'links')
            except Exception as e:
                print(y, 'ERR', str(e)[:80]); links[str(y)] = []
            time.sleep(random.uniform(4, 8))
    finally:
        d.quit()
    with open(os.path.join(folder, f'{company}_links.json'), 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False)
    hdr = {'User-Agent': UA}
    for y, items in links.items():
        stats = {'file': 0, 'dup': 0, 'yt': 0}
        for it in items:
            r = _download_result_item(it, y, folder, yt, hdr)
            if r:
                stats[r[0]] += 1
        print(f'== {y}: {stats} ==')
    print(f'Arquivos em {folder}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Coletor de documentos de RI (portais MZiQ).')
    ap.add_argument('empresa', help='nome da subpasta da empresa, ex.: Copel')
    ap.add_argument('anos', nargs='+', type=int, help='anos a coletar (só os faltantes)')
    ap.add_argument('--portal', help='URL da central de resultados (se não estiver em IR_PORTALS)')
    ap.add_argument('--saida', help='pasta raiz de saída (default: pasta_ri da configuração)')
    a = ap.parse_args()
    run(a.empresa, a.anos, out_root=a.saida, portal=a.portal)
