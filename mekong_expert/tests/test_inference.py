import unittest
from copy import deepcopy
from app.knowledge import load_knowledge
from app.inference import infer


class InferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events, cls.places, cls.rules, _ = load_knowledge()

    def run_infer(self, facts, rules=None):
        return infer(facts.split(), self.rules if rules is None else rules, self.events)

    def test_my_khanh(self):
        result = self.run_infer('R1 K1 N1 V1 L3 DT1 TG2')
        self.assertIn('T1', [r['code'] for r in result])
        self.assertEqual(next(p['name'] for p in self.places if p['code'] == 'T1'), 'Làng du lịch Mỹ Khánh')

    def test_both_t5_t6(self):
        result = self.run_infer('R3 K2 N2 V5 L7 DT5 TG2')
        self.assertEqual([r['code'] for r in result], ['T5', 'T6'])
        self.assertIn(75, result[0]['rule_ids'])
        self.assertIn(87, result[1]['rule_ids'])

    def test_both_t8_t9(self):
        self.assertEqual([r['code'] for r in self.run_infer('R3 K3 N2 V9 L5 DT3 TG2')], ['T8', 'T9'])

    def test_no_match(self):
        self.assertEqual(self.run_infer('R6 K4 N4 V20 L1 DT6 TG4'), [])

    def test_six_conditions_do_not_match(self):
        rule = self.rules[0]
        self.assertEqual(self.run_infer('R1 K1 N1 V1 L3 DT1 TG1', [rule]), [])
        with self.assertRaises(ValueError):
            self.run_infer('R1 K1 N1 V1 L3 DT1', [rule])

    def test_duplicate_rule_no_duplicate_destination(self):
        rule = self.rules[0]
        duplicate = deepcopy(rule)
        duplicate['id'] = 999
        result = infer(rule['conditions'], [rule, duplicate], self.events)
        self.assertEqual(result, [{'code': 'T1', 'rule_ids': [1, 999]}])

    def test_original_duplicates_keep_all_ids(self):
        rule = next(r for r in self.rules if r['id'] == 37)
        result = infer(rule['conditions'], self.rules, self.events)
        place = next(r for r in result if r['code'] == 'T3')
        self.assertEqual(place['rule_ids'], [37, 40])
        self.assertEqual(len([r for r in result if r['code'] == 'T3']), 1)

    def test_all_source_rules(self):
        self.assertEqual(len(self.rules), 435)
        for rule in self.rules:
            with self.subTest(rule=rule['id']):
                self.assertIn(rule['result'], [r['code'] for r in infer(rule['conditions'], self.rules, self.events)])

    def test_budget_not_inherited(self):
        self.assertEqual(self.run_infer('R1 K1 N4 V1 L3 DT1 TG2', [self.rules[0]]), [])

    def test_invalid_input(self):
        for facts in ('R99 K1 N1 V1 L3 DT1 TG2', 'R1 R2 N1 V1 L3 DT1 TG2'):
            with self.subTest(facts=facts), self.assertRaises(ValueError):
                self.run_infer(facts)


if __name__ == '__main__':
    unittest.main()
