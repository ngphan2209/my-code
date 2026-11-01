"""Kiem tra chung du lieu va tao bao cao co the doi chieu voi nguon."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.knowledge import ROOT, validate_knowledge
from app.inference import infer


def check(root=ROOT):
    values = []
    try:
        for name in ('events', 'destinations', 'rules'):
            values.append(json.loads((root / 'data' / f'{name}.json').read_text(encoding='utf-8')))
    except (OSError, ValueError) as exc:
        return [f'Không đọc được JSON: {exc}'], [], []
    errors, warnings = validate_knowledge(*values, root=root)
    coverage = []
    if not errors:
        events, destinations, rules = values
        for rule in rules:
            codes = {r['code'] for r in infer(rule['conditions'], rules, events)}
            if rule['result'] not in codes:
                errors.append(f'Luật {rule["id"]} không suy ra {rule["result"]}.')
            else:
                coverage.append(rule['id'])
    return errors, warnings, coverage


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', action='store_true', help='Cập nhật reports/knowledge_audit.md')
    args = parser.parse_args()
    errors, warnings, coverage = check()
    summary = f'{len(errors)} lỗi chặn chạy; {len(warnings)} cảnh báo; {len(coverage)} luật qua kiểm tra suy ra kết luận.'
    print(summary)
    for item in errors + warnings:
        print(item)
    if args.report:
        lines = ['# Kiểm tra cơ sở tri thức', '', summary, '',
                 'Quy ước kỹ thuật: suy luận theo biểu thức mã hóa. Giữ nguyên lời văn và số luật; giải thích giao diện sinh từ danh mục mã.',
                 'Đây chưa phải xác minh dữ liệu du lịch thực tế. Không sửa khoảng cách, tỉnh, giá hoặc sinh thêm luật.',
                 'Cùng điều kiện dẫn đến nhiều kết luận là tình huống hợp lệ, không chặn chạy.', '',
                 '## Lỗi chặn chạy', '', *(['- ' + e for e in errors] or ['Không có.']), '',
                 '## Cảnh báo', '', *['- ' + w for w in warnings], '',
                 '## Đối chiếu nguồn', '',
                 'Xem source_import.md để biết SHA-256 nguồn, vị trí đoạn và cách ghép ảnh.',
                 'Xem source_inventory.md để biết mã nguồn cũ đã đọc và phạm vi tham khảo.']
        (ROOT / 'reports/knowledge_audit.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    sys.exit(1 if errors else 0)
