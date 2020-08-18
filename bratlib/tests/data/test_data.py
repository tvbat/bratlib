import tempfile
import unittest
from shutil import rmtree

from bratlib.data import *

sample_doc = """T1\tA 1 2\tlorem
T2\tB 3 5;5 6\tipsum
E1\tD:T1 Org1:T1 Org2:T2
R1\tC Arg1:T1 Arg2:T2
*\tEquiv T1 T2
A1\tF E1
N1\tReference T1 C:1\tlorem
"""


class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.brat_dir = tempfile.mkdtemp()
        cls.brat_file = os.path.join(cls.brat_dir, 'file.ann')
        with open(cls.brat_file, 'w') as f:
            f.write(sample_doc)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.brat_dir)

    def test_from_file(self):

        ents_expected = [
            Entity('A', [(1, 2)], 'lorem'),
            Entity('B', [(3, 5), (5, 6)], 'ipsum'),
        ]

        event_expected = []

        rel_expected = [
            Relation('C', ents_expected[0], ents_expected[1])
        ]

        equiv_expected = [
            Equivalence(ents_expected[0:2])
        ]

        attribute_expected = [
            Attribute('F', event_expected[0])
        ]

        norm_expected = [
            Normalization(ents_expected[0], 'C', '1')
        ]

        ann = BratFile.from_ann_path(self.brat_file)

        self.assertListEqual(ann.entities, ents_expected)
        self.assertListEqual([ent.mention for ent in ann.entities], [ent.mention for ent in ents_expected])
        self.assertListEqual(ann.relations, rel_expected)
        self.assertIs(ann.relations[0].arg1, ann.entities[0])
        self.assertListEqual(ann.equivalences, equiv_expected)
        self.assertListEqual(ann.attributes, attribute_expected)
        self.assertListEqual(ann.normalizations, norm_expected)
