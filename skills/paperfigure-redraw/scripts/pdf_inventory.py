#!/usr/bin/env python3
"""Render PDF pages and collect candidate captions for human review."""
import argparse
import json
import re
from pathlib import Path

try:
    import fitz
except ImportError as exc:
    raise SystemExit('Install PyMuPDF first: python -m pip install pymupdf') from exc

CAPTION = re.compile(r'(?im)^\s*((?:fig(?:ure)?\.?|table)\s*(?:s|S)?\d+[a-z]?(?:[.\s:—–-]|$).{0,240})')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--dpi', type=int, default=150)
    args = parser.parse_args()
    if args.dpi < 36 or args.dpi > 600:
        parser.error('--dpi must be between 36 and 600')
    args.out.mkdir(parents=True, exist_ok=True)
    pages = args.out / 'pages'
    pages.mkdir(exist_ok=True)
    records = []
    with fitz.open(args.pdf) as doc:
        if doc.needs_pass:
            raise SystemExit('Password-protected PDF: supply an unlocked copy.')
        page_count = len(doc)
        for index, page in enumerate(doc):
            number = index + 1
            stem = f'page-{number:04d}'
            page.get_pixmap(dpi=args.dpi, alpha=False).save(str(pages / f'{stem}.png'))
            content = page.get_text('text')
            (pages / f'{stem}.txt').write_text(content, encoding='utf-8')
            for match in CAPTION.finditer(content):
                records.append({'page': number, 'candidate': match.group(1).strip()})
    manifest = {'source': str(args.pdf), 'page_count': page_count,
                'dpi': args.dpi, 'candidates': records,
                'notice': 'Candidates only; visually review every page, including scanned pages.'}
    (args.out / 'candidates.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Rendered {manifest['page_count']} pages; {len(records)} candidate captions. Review every page.")


if __name__ == '__main__':
    main()

