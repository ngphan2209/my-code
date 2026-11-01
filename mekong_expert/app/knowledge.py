"""Doc JSON va kiem tra co so tri thuc, khong phu thuoc Qt."""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {'R': 6, 'K': 4, 'N': 4, 'V': 20, 'L': 7, 'DT': 6, 'TG': 4}
GROUP_LABELS = {'R': 'Tỉnh/thành phố', 'K': 'Khoảng cách', 'N': 'Ngân sách',
                'V': 'Trải nghiệm', 'L': 'Loại hình', 'DT': 'Nhóm người cùng đi',
                'TG': 'Thời gian', 'T': 'Địa điểm'}


def group_of(code):
    match = re.fullmatch(r'(DT|TG|R|K|N|V|L|T)[1-9]\d*', str(code))
    return match.group(1) if match else None


def distance_in_text(text):
    # Chi doc phan khoang cach, khong nham voi ngan sach.
    match = re.search(r'cách trung tâm.*?(?=, có ngân sách)', text, re.I)
    if not match:
        return None
    distance = match.group().lower()
    patterns = {'K1': r'không quá 30\s*km', 'K2': r'trên 30\s*km đến 100\s*km',
                'K3': r'trên 100\s*km đến 200\s*km', 'K4': r'trên 200\s*km'}
    return next((code for code, pattern in patterns.items() if re.search(pattern, distance)), None)


def validate_knowledge(events, destinations, rules, root=ROOT):
    errors, warnings = [], []
    for name, value in [('events', events), ('destinations', destinations), ('rules', rules)]:
        if not isinstance(value, list):
            errors.append(f'{name}: phải là danh sách JSON.')
    if errors:
        return errors, warnings
    event_map, destination_map, ids = {}, {}, set()
    for index, event in enumerate(events):
        if not isinstance(event, dict) or any(not isinstance(event.get(k), str) or not event[k].strip()
                                              for k in ('code', 'label', 'group')):
            errors.append(f'events[{index}]: thiếu/sai code, label hoặc group.'); continue
        code = event['code']
        if code in event_map:
            errors.append(f'Mã sự kiện trùng: {code}.')
        event_map[code] = event
        if group_of(code) != event['group'] or event['group'] not in {*GROUPS, 'T'}:
            errors.append(f'{code}: nhóm sự kiện không hợp lệ.')
    expected = {f'{group}{i}' for group, count in {**GROUPS, 'T': 30}.items() for i in range(1, count + 1)}
    if set(event_map) != expected:
        errors.append(f'Danh mục mã khác quy định. Thiếu: {sorted(expected-set(event_map))}; thừa: {sorted(set(event_map)-expected)}')
    for index, destination in enumerate(destinations):
        if not isinstance(destination, dict) or any(not isinstance(destination.get(k), str) or not destination[k].strip()
                                                   for k in ('code', 'name', 'description', 'image')):
            errors.append(f'destinations[{index}]: thiếu/sai code, name, description hoặc image.'); continue
        code = destination['code']
        if code in destination_map:
            errors.append(f'Mã địa điểm trùng: {code}.')
        destination_map[code] = destination
        if code not in event_map or group_of(code) != 'T':
            errors.append(f'Địa điểm không tồn tại trong sự kiện: {code}.')
        image_path = Path(destination['image'])
        if image_path.is_absolute() or '..' in image_path.parts:
            errors.append(f'{code}: đường dẫn ảnh phải tương đối trong dự án.')
        elif not (root / image_path).is_file():
            warnings.append(f'Ảnh thiếu: {code}: {image_path}')
        if 'video' in destination:
            video_path = Path(str(destination['video']))
            if video_path.is_absolute() or '..' in video_path.parts:
                errors.append(f'{code}: đường dẫn video phải tương đối trong dự án.')
            elif not (root / video_path).is_file():
                warnings.append(f'Video thiếu: {code}: {video_path}')
        if 'address' in destination and not isinstance(destination['address'], str):
            errors.append(f'{code}: address phải là chuỗi.')
    if set(destination_map) != {f'T{i}' for i in range(1, 31)}:
        errors.append('Danh mục địa điểm phải có đúng T1–T30.')
    if not rules:
        errors.append("Tập luật rỗng, không thể tư vấn.")
    signatures, conditions_map, used = defaultdict(list), defaultdict(list), set()
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f'rules[{index}]: phải là đối tượng.'); continue
        rid = rule.get('id')
        if type(rid) is not int or rid <= 0:
            errors.append(f'rules[{index}]: id phải là số nguyên dương.')
        elif rid in ids:
            errors.append(f'ID luật trùng: {rid}.')
        else:
            ids.add(rid)
        prefix = f'Luật {rid}'
        for key in ('source_text', 'source_formula', 'result'):
            if not isinstance(rule.get(key), str) or not rule[key].strip():
                errors.append(f'{prefix}: thiếu/sai {key}.')
        result = rule.get('result')
        if not isinstance(result, str) or result not in destination_map:
            errors.append(f'{prefix}: mã địa điểm không tồn tại: {result}.')
        else:
            used.add(result)
        conditions = rule.get('conditions')
        if not isinstance(conditions, list) or not all(isinstance(c, str) for c in conditions):
            errors.append(f'{prefix}: conditions phải là danh sách mã.'); continue
        groups = [event_map.get(c, {}).get('group') for c in conditions]
        for code in conditions:
            if code not in event_map:
                errors.append(f'{prefix}: mã sự kiện không tồn tại: {code}.')
        if len(conditions) != 7 or set(groups) != set(GROUPS) or len(set(groups)) != len(groups):
            errors.append(f'{prefix}: thiếu hoặc lặp nhóm điều kiện; cần đúng bảy nhóm {list(GROUPS)}.')
        formula = rule.get('source_formula', '')
        if isinstance(formula, str):
            parts = formula.split('→')
            if len(parts) != 2 or [c.strip() for c in parts[0].split('∧')] != conditions or parts[-1].strip() != result:
                errors.append(f'{prefix}: conditions/result khác source_formula.')
        text = rule.get('source_text', '')
        if isinstance(text, str):
            text_k = distance_in_text(text)
            formula_k = next((c for c in conditions if group_of(c) == 'K'), None)
            if text_k and text_k != formula_k:
                warnings.append(f'Nguồn không khớp khoảng cách: luật {rid}: lời văn {text_k}, biểu thức {formula_k}.')
            elif text_k is None:
                warnings.append(f'Chưa nhận diện được khoảng cách lời văn: luật {rid}.')
        signature = tuple(sorted(conditions))
        if isinstance(result, str):
            signatures[(signature, result)].append(rid)
            conditions_map[signature].append((rid, result))
    for (_, result), rule_ids in signatures.items():
        if len(rule_ids) > 1:
            warnings.append(f'Luật trùng hoàn toàn: {rule_ids} → {result}.')
    for entries in conditions_map.values():
        if len({result for _, result in entries}) > 1:
            warnings.append(f'Cùng điều kiện, nhiều kết luận (hợp lệ): {entries}.')
    for code in sorted(set(destination_map) - used):
        warnings.append(f'Địa điểm không có luật: {code}.')
    return errors, warnings


def load_knowledge(root=ROOT):
    values = []
    for name in ('events', 'destinations', 'rules'):
        path = root / 'data' / f'{name}.json'
        try:
            values.append(json.loads(path.read_text(encoding='utf-8')))
        except (OSError, ValueError) as exc:
            raise ValueError(f'Không đọc được {path}: {exc}') from exc
    errors, warnings = validate_knowledge(*values, root=root)
    if errors:
        raise ValueError('Cơ sở tri thức không hợp lệ:\n' + '\n'.join(errors))
    return (*values, warnings)
