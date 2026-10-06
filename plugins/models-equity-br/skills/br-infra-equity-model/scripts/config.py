#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuração local das skills de modelos de equity (compartilhada entre as skills).

Na primeira rodada a skill pergunta ao usuário onde ficam os arquivos e grava as
respostas num JSON. As rodadas seguintes só leem esse arquivo.

Arquivo: ~/.claude/models-equity-br/config.json
         (ou o caminho na variável de ambiente MODELS_EQUITY_BR_CONFIG)

Uso:
  python3 config.py status                      # mostra a configuração; código 3 = não configurado
  python3 config.py set --pasta-ri DIR --pasta-saida DIR [--pasta-fundamentos DIR] [--criar]
  python3 config.py get pasta_ri                # imprime só o valor (para outros scripts)
  python3 config.py deps                        # checa as dependências da skill

Campos:
  pasta_ri           pasta com os documentos de RI, uma subpasta por empresa
                     (releases, ITR/DFP, apresentações). O importador de RI salva aqui.
  pasta_fundamentos  pasta com as planilhas de fundamentos / dados históricos (opcional).
  pasta_saida        pasta onde os modelos (.xlsx) são salvos.
"""
import argparse
import datetime
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

CAMPOS = ('pasta_ri', 'pasta_fundamentos', 'pasta_saida')
NAO_CONFIGURADO = 3


def _utf8_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass


def config_path():
    env = os.environ.get('MODELS_EQUITY_BR_CONFIG')
    if env:
        return Path(env).expanduser()
    return Path.home() / '.claude' / 'models-equity-br' / 'config.json'


def load():
    """Devolve o dict da configuração, ou None se ainda não existe."""
    p = config_path()
    if not p.exists():
        return None
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def get(campo, default=None):
    cfg = load() or {}
    return cfg.get(campo) or default


def _norm(pasta):
    return str(Path(pasta).expanduser().resolve())


def cmd_status(_args):
    p = config_path()
    cfg = load()
    out = {'configurado': cfg is not None, 'arquivo': str(p)}
    if cfg is not None:
        out['config'] = cfg
        out['pastas_inexistentes'] = [c for c in CAMPOS
                                      if cfg.get(c) and not Path(cfg[c]).is_dir()]
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if cfg is not None else NAO_CONFIGURADO


def cmd_set(args):
    cfg = load() or {}
    novos = {'pasta_ri': args.pasta_ri, 'pasta_fundamentos': args.pasta_fundamentos,
             'pasta_saida': args.pasta_saida}
    erros = []
    for campo, valor in novos.items():
        if valor is None:
            continue
        if valor == '':
            cfg[campo] = None
            continue
        pasta = Path(_norm(valor))
        if not pasta.is_dir():
            if args.criar or campo == 'pasta_saida':
                pasta.mkdir(parents=True, exist_ok=True)
                print(f'pasta criada: {pasta}')
            else:
                erros.append(f'{campo}: a pasta não existe: {pasta} '
                             '(confira o caminho ou rode de novo com --criar)')
                continue
        cfg[campo] = str(pasta)
    if erros:
        print('\n'.join(erros), file=sys.stderr)
        return 1
    for campo in ('pasta_ri', 'pasta_saida'):
        if not cfg.get(campo):
            print(f'{campo} é obrigatório.', file=sys.stderr)
            return 1
    cfg.setdefault('pasta_fundamentos', None)
    cfg['atualizado_em'] = datetime.date.today().isoformat()
    p = config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f'configuração gravada em {p}')
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
    return 0


def cmd_get(args):
    valor = get(args.campo)
    if valor is None:
        return NAO_CONFIGURADO
    print(valor)
    return 0


def find_soffice():
    """Localiza o executável do LibreOffice (Linux, macOS e Windows)."""
    for nome in ('soffice', 'libreoffice'):
        achado = shutil.which(nome)
        if achado:
            return achado
    candidatos = [
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',
        r'C:\Program Files\LibreOffice\program\soffice.exe',
        r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
    ]
    for c in candidatos:
        if Path(c).exists():
            return c
    return None


def cmd_deps(_args):
    linhas, faltando_obrigatorio = [], False

    def item(nome, ok, obrigatorio, como_instalar):
        nonlocal faltando_obrigatorio
        status = 'ok' if ok else ('FALTANDO' if obrigatorio else 'faltando (opcional)')
        if not ok and obrigatorio:
            faltando_obrigatorio = True
        linhas.append((nome, status, '' if ok else como_instalar))

    item(f'Python {sys.version_info.major}.{sys.version_info.minor}',
         sys.version_info >= (3, 8), True, 'instalar Python 3.8 ou mais novo')
    item('openpyxl', importlib.util.find_spec('openpyxl') is not None, True,
         'pip install openpyxl')
    item('LibreOffice (recálculo do modelo)', find_soffice() is not None, True,
         'instalar em https://www.libreoffice.org/download/')
    item('pdftotext (leitura de PDFs)', shutil.which('pdftotext') is not None, True,
         'Poppler: macOS "brew install poppler"; Linux "apt install poppler-utils"; '
         'Windows: baixar o Poppler e pôr a pasta bin no PATH')
    item('selenium (importador de RI)', importlib.util.find_spec('selenium') is not None,
         False, 'pip install selenium requests (e Google Chrome instalado)')
    item('requests (importador de RI)', importlib.util.find_spec('requests') is not None,
         False, 'pip install requests')

    largura = max(len(n) for n, _, _ in linhas)
    for nome, status, dica in linhas:
        print(f'{nome.ljust(largura)}  {status}' + (f'  -> {dica}' if dica else ''))
    return 1 if faltando_obrigatorio else 0


def main():
    _utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('status')
    s = sub.add_parser('set')
    s.add_argument('--pasta-ri')
    s.add_argument('--pasta-fundamentos', help='passe "" para deixar em branco')
    s.add_argument('--pasta-saida')
    s.add_argument('--criar', action='store_true', help='cria as pastas que não existirem')
    g = sub.add_parser('get')
    g.add_argument('campo', choices=CAMPOS)
    sub.add_parser('deps')
    args = ap.parse_args()
    return {'status': cmd_status, 'set': cmd_set, 'get': cmd_get, 'deps': cmd_deps}[args.cmd](args)


if __name__ == '__main__':
    sys.exit(main())
