"""Extract page text/geometry and render selected physical pages. Requires PyMuPDF."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--pages', help='1-based pages, e.g. 2,4-6; default all')
    args = parser.parse_args()
    try:
        import fitz
    except ImportError:
        parser.error('Install dependency: python -m pip install pymupdf')
    with fitz.open(args.pdf) as doc:
        if doc.needs_pass:
            parser.error('PDF is encrypted; provide an unlocked copy')
        selected = set(range(1, len(doc) + 1))
        if args.pages:
            selected = set()
            try:
                for part in args.pages.split(','):
                    bounds = list(map(int, part.split('-')))
                    if len(bounds) == 1:
                        bounds *= 2
                    if len(bounds) != 2 or not 1 <= bounds[0] <= bounds[1] <= len(doc):
                        raise ValueError()
                    selected.update(range(bounds[0], bounds[1] + 1))
            except ValueError:
                parser.error('Invalid physical page selection')
        args.out.mkdir(parents=True, exist_ok=True)
        records = []
        for index, page in enumerate(doc, 1):
            record = {'pdf_page': index, 'width': page.rect.width, 'height': page.rect.height}
            try:
                text = page.get_text('text', sort=True)
                (args.out / f'page-{index:03}.txt').write_text(text, encoding='utf-8')
                record['blocks'] = page.get_text('blocks', sort=True)
                record['low_text_warning'] = len(text.strip()) < 80
                record['section_candidates'] = [line for line in text.splitlines() if any(
                    word in line.lower() for word in ('abstract', 'introduction', 'design',
                    'evaluation', 'implementation', 'conclusion', 'discussion', 'motivation'))]
            except Exception as exc:
                record['text_error'] = str(exc)
            if index in selected:
                try:
                    page.get_pixmap(matrix=fitz.Matrix(2, 2)).save(args.out / f'page-{index:03}.png')
                except Exception as exc:
                    record['render_error'] = str(exc)
            records.append(record)
        (args.out / 'pages.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Processed {len(doc)} pages. Reading order and visual evidence require review.')


if __name__ == '__main__':
    main()
