#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trava de sanitização: garante que o repositório não carregue nomes, caminhos ou
metadados que impeçam compartilhar as skills fora da empresa.

Dois tipos de verificação:
1. Termos proibidos (nomes de empresa, pessoas etc.). A lista NÃO fica no código —
   senão a própria trava citaria os termos. Fontes, uma expressão regular por linha
   (sem diferenciar maiúsculas/minúsculas; linhas com # são comentário):
     - variável de ambiente SANITIZE_BLOCKLIST (no GitHub: segredo do repositório);
     - arquivo .sanitize-blocklist na raiz (fora do git, ver .gitignore).
2. Checks estruturais, sempre ativos: caminhos absolutos de máquina, e-mails,
   ambientes do claude.ai (/mnt/...), links externos e metadados de autor dentro de
   arquivos do Office, e cópias divergentes dos scripts compartilhados entre skills.

Uso: python3 tools/check_sanitized.py      (código 1 se encontrar algo)
"""
import hashlib
import os
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
IGNORAR_DIRS = {'.git', '__pycache__', 'node_modules'}
IGNORAR_ARQS = {'.sanitize-blocklist'}
OFFICE = {'.xlsx', '.xlsm', '.docx', '.pptx'}
BINARIOS = {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.bin'}
COMPARTILHADOS = ('config.py', 'recalc.py', 'ir_importer.py', 'helpers_template.py')

ESTRUTURAIS = [
    (r'[A-Za-z]:\\(?!Program Files)', 'caminho absoluto do Windows'),
    (r'(?<![\w.])/Users/[^/\s"\'`]+/', 'caminho absoluto do macOS'),
    (r'(?<![\w.])/home/[^/\s"\'`]+/', 'caminho absoluto do Linux'),
    (r'/mnt/(user-data|skills)', 'caminho do ambiente claude.ai'),
    (r'\\\\[A-Za-z0-9_.-]+\\', 'caminho de rede (UNC)'),
    (r'file:///', 'link para arquivo local'),
    (r'[\w.+-]+@[\w-]+\.[\w.-]*[a-z]{2,}', 'endereço de e-mail'),
]


def carregar_blocklist():
    linhas = []
    env = os.environ.get('SANITIZE_BLOCKLIST', '')
    linhas += env.replace('\r', '').split('\n')
    arq = RAIZ / '.sanitize-blocklist'
    if arq.exists():
        linhas += arq.read_text(encoding='utf-8').splitlines()
    pats = []
    for l in linhas:
        l = l.strip()
        if l and not l.startswith('#'):
            pats.append((re.compile(l, re.I), 'termo proibido'))
    return pats


def textos_office(path):
    """Devolve [(parte, texto)] de um arquivo do Office e os problemas estruturais."""
    partes, problemas = [], []
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.startswith(('xl/externalLinks/', 'word/externalLinks/')):
                problemas.append(f'{n}: link para pasta de trabalho externa')
            if 'printerSettings' in n:
                problemas.append(f'{n}: configuração de impressora embutida')
            if n.endswith(('.xml', '.rels')):
                t = z.read(n).decode('utf-8', 'replace')
                partes.append((n, t))
                if n == 'docProps/core.xml':
                    for tag in ('dc:creator', 'cp:lastModifiedBy'):
                        m = re.search(rf'<{tag}>([^<]+)</{tag}>', t)
                        if m:
                            problemas.append(f'{n}: metadado {tag} preenchido')
    return partes, problemas


def varrer(texto, pats):
    for i, linha in enumerate(texto.splitlines(), 1):
        for rx, motivo in pats:
            m = rx.search(linha)
            if m:
                yield i, motivo, m.group(0)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass
    bloq = carregar_blocklist()
    estr = [(re.compile(p), m) for p, m in ESTRUTURAIS]
    if not bloq:
        print('AVISO: lista de termos proibidos vazia (segredo SANITIZE_BLOCKLIST ou '
              'arquivo .sanitize-blocklist) — rodando só os checks estruturais.')
    achados = []
    for path in sorted(RAIZ.rglob('*')):
        rel = path.relative_to(RAIZ)
        if path.is_dir() or set(rel.parts) & IGNORAR_DIRS or path.name in IGNORAR_ARQS:
            continue
        if rel == Path('tools/check_sanitized.py'):
            pats = bloq            # este arquivo descreve os padrões estruturais
        else:
            pats = bloq + estr
        suf = path.suffix.lower()
        if suf in OFFICE:
            partes, probs = textos_office(path)
            achados += [f'{rel}: {p}' for p in probs]
            for parte, t in partes:
                for _, motivo, trecho in varrer(t, pats):
                    achados.append(f'{rel} [{parte}]: {motivo}: {trecho!r}')
            continue
        if suf in BINARIOS:
            continue
        try:
            t = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            achados.append(f'{rel}: arquivo binário não reconhecido — revisar à mão')
            continue
        for n, motivo, trecho in varrer(t, pats):
            achados.append(f'{rel}:{n}: {motivo}: {trecho!r}')

    # scripts compartilhados: as cópias de cada skill têm de ser idênticas
    skills = sorted(p for p in (RAIZ / 'plugins').glob('*/skills/*') if p.is_dir())
    for nome in COMPARTILHADOS:
        hashes = {}
        for s in skills:
            f = s / 'scripts' / nome
            if f.exists():
                hashes[str(f.relative_to(RAIZ))] = hashlib.sha256(f.read_bytes()).hexdigest()
        if len(set(hashes.values())) > 1:
            achados.append(f'cópias divergentes de {nome}: ' + ', '.join(hashes))

    if achados:
        print(f'{len(achados)} problema(s) encontrado(s):')
        for a in achados:
            print('  ' + a)
        return 1
    print('OK: nenhum problema encontrado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
