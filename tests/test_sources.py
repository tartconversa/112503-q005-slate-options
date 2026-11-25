"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'projects.csv': ['project', 'kind', 'market', 'delivery_due', 'option_until', 'plan'], 'stages.csv': ['stage', 'project', 'quarter', 'cost', 'condition', 'resource', 'first', 'last', 'max_delay_days'], 'reservations.csv': ['commitment', 'project', 'resource', 'start', 'stop', 'fee_paid', 'cancel_fee', 'settlement', 'state'], 'history.csv': ['comparable', 'kind', 'market', 'channel', 'settled_quarter', 'min_guarantee', 'total_received', 'days_late'], 'offers.csv': ['offer', 'package', 'project', 'market', 'minimum', 'receipt_quarter', 'expiry', 'rev'], 'scenarios.csv': ['scenario_id', 'market', 'quarter', 'receipt_factor', 'delay_days'], 'committee.csv': ['decision', 'project', 'reported', 'quarter', 'cash_cap', 'kind', 'signal'], 'committee_limits.csv': ['quarter', 'cash_available', 'min_regional_short', 'min_member_long', 'as_of']}
REFERENCES = [('stages.csv', 'project', 'projects.csv', 'project'), ('reservations.csv', 'project', 'projects.csv', 'project'), ('offers.csv', 'project', 'projects.csv', 'project'), ('committee.csv', 'project', 'projects.csv', 'project')]
OBSERVED_VALUES = [('offers.csv', 'package', 'G1', 2), ('offers.csv', 'offer', 'B4', 2), ('reservations.csv', 'resource', 'CastA', 2)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
