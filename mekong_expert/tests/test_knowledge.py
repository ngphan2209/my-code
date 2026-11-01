import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from app.knowledge import load_knowledge, validate_knowledge


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.events, self.places, self.rules, self.warnings = load_knowledge()

    def errors(self, rules=None, events=None, places=None):
        return validate_knowledge(self.events if events is None else events,
                                  self.places if places is None else places,
                                  self.rules if rules is None else rules)[0]

    def test_full_data_and_audit_counts(self):
        self.assertEqual(len(self.events), 81)
        self.assertEqual(len(self.places), 30)
        self.assertEqual([r['id'] for r in self.rules], list(range(1, 436)))
        self.assertEqual(self.errors(), [])
        for prefix, count in [('Luật trùng hoàn toàn:', 13), ('Cùng điều kiện,', 2), ('Nguồn không khớp', 20)]:
            self.assertEqual(sum(w.startswith(prefix) for w in self.warnings), count)
        self.assertFalse(any(w.startswith('Ảnh thiếu') for w in self.warnings))

    def test_unknown_event(self):
        self.rules[0]['conditions'][0] = 'R99'
        self.assertTrue(any('mã sự kiện không tồn tại' in e for e in self.errors()))

    def test_unknown_destination(self):
        self.rules[0]['result'] = 'T99'
        self.assertTrue(any('mã địa điểm không tồn tại' in e for e in self.errors()))

    def test_missing_group(self):
        self.rules[0]['conditions'].pop()
        self.assertTrue(any('thiếu hoặc lặp nhóm' in e for e in self.errors()))

    def test_repeated_group(self):
        self.rules[0]['conditions'][-1] = 'R2'
        self.assertTrue(any('thiếu hoặc lặp nhóm' in e for e in self.errors()))

    def test_duplicate_id(self):
        self.rules[1]['id'] = self.rules[0]['id']
        self.assertTrue(any('ID luật trùng' in e for e in self.errors()))

    def test_wrong_structure_and_missing_fields(self):
        self.assertTrue(self.errors(events={}))
        self.assertTrue(self.errors(places=[{}]))
        self.assertTrue(self.errors(rules=[{}]))
        self.assertTrue(self.errors(rules=[None]))
        del self.rules[0]['source_text']
        self.assertTrue(any('source_text' in e for e in self.errors()))

    def test_invalid_json_and_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            with self.assertRaisesRegex(ValueError, 'Không đọc được'):
                load_knowledge(root)
            (root / 'data/events.json').write_text('{invalid', encoding='utf8')
            with self.assertRaisesRegex(ValueError, 'events.json'):
                load_knowledge(root)

    def test_missing_photo_and_no_rules_are_warnings(self):
        self.places[0]['image'] = 'assets/destinations/absent.jpg'
        rules = [r for r in self.rules if r['result'] != 'T1']
        errors, warnings = validate_knowledge(self.events, self.places, rules)
        self.assertEqual(errors, [])
        self.assertTrue(any('Ảnh thiếu: T1' in w for w in warnings))
        self.assertIn('Địa điểm không có luật: T1.', warnings)

    def test_source_formula_divergence(self):
        self.rules[0]['conditions'][0] = 'R2'
        self.assertTrue(any('khác source_formula' in e for e in self.errors()))

    def test_bad_image_path_and_duplicate_event(self):
        self.places[0]['image'] = '../outside.png'
        self.events.append(deepcopy(self.events[0]))
        self.assertTrue(any('đường dẫn ảnh' in e for e in self.errors()))
        self.assertTrue(any('Mã sự kiện trùng' in e for e in self.errors()))


if __name__ == '__main__':
    unittest.main()
