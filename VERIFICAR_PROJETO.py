#!/usr/bin/env python3
"""Verificacao offline da V62: hashes, sintaxe e estrutura PNG. Nao exige Pygame."""
from pathlib import Path
import hashlib
import struct
import sys

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'MANIFEST_SHA256.txt'
PNG_MAGIC = b'\x89PNG\r\n\x1a\n'


def check_png(path):
    with path.open('rb') as f:
        if f.read(8) != PNG_MAGIC:
            raise ValueError('assinatura PNG ausente')
        seen_header = False
        seen_image_data = False
        seen_end = False
        while True:
            size_bytes = f.read(4)
            if not size_bytes:
                break
            if len(size_bytes) != 4:
                raise ValueError('cabecalho incompleto')
            count = struct.unpack('>I', size_bytes)[0]
            if count > 100_000_000:
                raise ValueError('bloco PNG muito grande')
            kind = f.read(4)
            chunk = f.read(count)
            checksum = f.read(4)
            if len(kind) != 4 or len(chunk) != count or len(checksum) != 4:
                raise ValueError('bloco PNG truncado')
            import zlib
            if (zlib.crc32(kind + chunk) & 0xffffffff) != struct.unpack('>I', checksum)[0]:
                raise ValueError('CRC de PNG invalido')
            if kind == b'IHDR':
                if seen_header or count != 13:
                    raise ValueError('IHDR invalido')
                w, h = struct.unpack('>II', chunk[:8])
                if not (w and h):
                    raise ValueError('imagem sem tamanho')
                seen_header = True
            elif kind == b'IDAT':
                seen_image_data = True
            elif kind == b'IEND':
                seen_end = True
                break
        if not (seen_header and seen_image_data and seen_end):
            raise ValueError('PNG incompleto')


def main():
    fails = []
    tested_py = tested_png = tested_files = 0
    if not MANIFEST.is_file():
        print('ERRO: MANIFEST_SHA256.txt nao encontrado')
        return 1
    manifest = MANIFEST.read_text(encoding='utf-8').splitlines()
    expected = set()
    for line in manifest:
        if not line or line.startswith('#'):
            continue
        try:
            correct, rel = line.split('  ', 1)
        except ValueError:
            fails.append(f'Linha de manifesto invalida: {line[:70]}')
            continue
        rel = rel.strip()
        expected.add(rel)
        f = ROOT / rel
        if not f.is_file():
            fails.append(f'Ausente: {rel}')
            continue
        tested_files += 1
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        if got != correct:
            fails.append(f'Hash divergente: {rel}')
            continue
        try:
            if f.suffix == '.py':
                compile(f.read_bytes(), str(f), 'exec')
                tested_py += 1
            elif f.suffix.lower() == '.png':
                check_png(f)
                tested_png += 1
        except Exception as exc:
            fails.append(f'Erro em {rel}: {exc}')

    actual = {x.relative_to(ROOT).as_posix() for x in ROOT.rglob('*')
              if x.is_file() and '__pycache__' not in x.parts and '.git' not in x.parts}
    allowed_extra = {'MANIFEST_SHA256.txt'}
    extras = actual - expected - allowed_extra
    if extras:
        print('Aviso: arquivos adicionais nao constam do manifesto:')
        for name in sorted(extras):
            print(' -', name)
    print(f'Arquivos verificados: {tested_files} | Python compilados: {tested_py} | PNGs validados: {tested_png}')
    if fails:
        print(f'FALHAS: {len(fails)}')
        for err in fails[:40]:
            print(' -', err)
        return 1
    print('OK: pacote integro. Teste visual no Pygame ainda e necessario.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
