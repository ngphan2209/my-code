"""Chuyen hai DOCX thanh JSON; anh duoc ghep theo khoi T, quan he va chu thich."""
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.knowledge import ROOT, group_of, validate_knowledge
from docx import Document


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def import_sources(rules_path, places_path, backgrounds=None):
    paragraphs = Document(rules_path).paragraphs
    events, rules = [], []
    pending = None
    for index, paragraph in enumerate(paragraphs):
        text = paragraph.text.strip()
        if text.startswith('2.2.'):
            break
        match = re.fullmatch(r'(.+?)\s*→\s*((?:DT|TG|R|K|N|V|L|T)\d+)', text)
        if match:
            label, code = match.groups()
            events.append({'code': code, 'label': label.strip(), 'group': group_of(code)})
    formula_count = 0
    for index, paragraph in enumerate(paragraphs):
        text = paragraph.text.strip()
        number = re.match(r'^(\d+)\.\s*Nếu\b', text)
        if number:
            if pending:
                raise ValueError(f'Luật {pending[0]} chưa có biểu thức trước đoạn {index}.')
            pending = (int(number[1]), text, index)
        if '∧' in text and '→' in text:
            formula_count += 1
            if pending is None:
                raise ValueError(f'Biểu thức không có lời văn/số luật ở đoạn {index}.')
            match = re.fullmatch(r'((?:(?:DT|TG|R|K|N|V|L)\d+\s*∧\s*){6}(?:DT|TG|R|K|N|V|L)\d+)\s*→\s*(T\d+)', text)
            if not match:
                raise ValueError(f'Không đọc được biểu thức đoạn {index}: {text}')
            conditions, result = match.groups()
            rules.append({'id': pending[0], 'conditions': [x.strip() for x in conditions.split('∧')],
                          'result': result, 'source_text': pending[1], 'source_formula': text,
                          'source_paragraph': pending[2], 'formula_paragraph': index})
            pending = None
    if pending or not rules or formula_count != len(rules):
        raise ValueError('Có luật chưa được nhập đầy đủ.')
    document = Document(places_path)
    blocks, current = [], None
    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        heading = re.fullmatch(r'(T\d+)\s+(.+)', text)
        if heading:
            current = {'code': heading[1], 'name': heading[2].strip(), 'text': [], 'images': [], 'captions': [], 'heading': index}
            blocks.append(current)
        if current is None:
            continue
        for rid in paragraph._p.xpath('.//a:blip/@r:embed'):
            part = document.part.related_parts[rid]
            current['images'].append((index, rid, part))
        if text.startswith('Hình '):
            current['captions'].append((index, text))
        elif text and not heading:
            current['text'].append(text)
    destinations, mappings = [], []
    for block in blocks:
        code = block['code']
        if len(block['images']) != 1 or len(block['captions']) != 1:
            raise ValueError(f'{code}: cần kiểm tra ảnh/chú thích thủ công, không tự ghép ảnh.')
        image_index, rid, part = block['images'][0]
        caption_index, caption = block['captions'][0]
        if not re.match(rf'Hình\s+{int(code[1:])}\.', caption) or not block['heading'] < image_index < caption_index:
            raise ValueError(f'{code}: thứ tự tiêu đề/ảnh/chú thích không rõ ràng.')
        relative = Path('assets/destinations') / (code + Path(str(part.partname)).suffix)
        (ROOT / relative).write_bytes(part.blob)
        destinations.append({'code': code, 'name': block['name'], 'description': '\n\n'.join(block['text']),
                             'image': relative.as_posix(), 'source_caption': caption})
        mappings.append(f'| {code} | {block["heading"]} | {image_index} | {rid} | {part.partname} | {caption} |')
    errors, warnings = validate_knowledge(events, destinations, rules)
    if errors:
        raise ValueError('\n'.join(errors))
    for name, value in [('events', events), ('destinations', destinations), ('rules', rules)]:
        write_json(ROOT / 'data' / f'{name}.json', value)
    if backgrounds:
        for pattern, output in [('nền sảnh*.png', 'home.png'), ('nền tư vấn*.png', 'consult.png')]:
            matches = list(backgrounds.glob(pattern))
            if len(matches) > 1:
                raise ValueError(f'Có nhiều nền {pattern}; hãy chỉ giữ bản muốn nhập trong thư mục nền.')
            if matches:
                shutil.copyfile(matches[0], ROOT / 'assets/backgrounds' / output)
    report = ['# Báo cáo nhập nguồn', '', 'Nguồn giữ nguyên; chỉ chuyển đổi sang JSON. Chỉ số đoạn DOCX bắt đầu từ 0.', '']
    for path in (rules_path, places_path):
        report.append(f'- {path.name}: SHA-256 `{hashlib.sha256(path.read_bytes()).hexdigest()}`')
    report.extend(['', f'Đã nhập {len(events)} sự kiện (gồm T1–T30), {len(destinations)} địa điểm, {len(rules)} luật.',
                   'Không nhập địa chỉ cụ thể vì tài liệu không có trường địa chỉ cụ thể.', '',
                   '## Quan hệ ảnh trong DOCX', '', '| Mã | Đoạn tiêu đề | Đoạn ảnh | Quan hệ | Tệp nhúng | Chú thích |',
                   '| --- | --- | --- | --- | --- | --- |', *mappings, '',
                   'Mỗi khối có đúng một ảnh và một chú thích cùng số T; ghép theo quan hệ DOCX, không theo tên imageN.',
                   'Chưa xác minh ảnh/chú thích và dữ liệu du lịch với nguồn thực địa.', '', '## Cảnh báo lúc nhập', '',
                   *['- ' + warning for warning in warnings]])
    (ROOT / 'reports/source_import.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    print(f'Nhập thành công: {len(destinations)} địa điểm, {len(rules)} luật; {len(warnings)} cảnh báo.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rules', type=Path, required=True)
    parser.add_argument('--places', type=Path, required=True)
    parser.add_argument('--backgrounds', type=Path)
    args = parser.parse_args()
    import_sources(args.rules, args.places, args.backgrounds)
