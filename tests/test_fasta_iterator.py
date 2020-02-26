import os, sys, unittest

import pythomics.parsers.fasta as parser


class Test_Fasta_Iterator(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.split(__file__)[0]
        data_dir = os.path.join(base_dir, "fixtures")
        self.handle = os.path.join(data_dir, "test_fasta_iterator.fasta")
        self.index = "{}.{}".format(self.handle, "fai")

    def test_fasta_iterator(self):
        f = parser.FastaIterator(self.handle, delimiter=">")
        assert isinstance(f, parser.FastaIterator)
        headers = []
        sequences = []
        for header, sequence in f:
            headers.append(header)
            sequences.append(sequence)
        self.assertEqual(headers, ["c1", "c2", "c3"])
        self.assertEqual(
            sequences[1],
            "MSCRQFSSSYLSRSGGGGGGGLGSGGSIRSSYSRFSSSGGRGGGGRFSSSSGYGGGSSRVCGRGGGGSFGYSYGGGSGGGFSASSLGGGFGGGSRGFGGASGGGYSSSGGFGGGFGGGSGGGFGGGYGSGFGGLGGFGGGAGGGDGGILTANEKSTMQELNSRLASYLDKVQALEEANNDLENKIQDWYDKKGPAAIQKNYSPYYNTIDDLKDQIVDLTVGNNKTLLDIDNTRMTLDDFRIKFEMEQNLRQGVDADINGLRQVLDNLTMEKSDLEMQYETLQEELMALKKNHKEEMSQLTGQNSGDVNVEINVAPGKDLTKTLNDMRQEYEQLIAKNRKDIENQYETQITQIEHEVSSSGQEVQSSAKEVTQLRHGVQELEIELQSQLSKKAALEKSLEDTKNRYCGQLQMIQEQISNLEAQITDVRQEIECQNQEYSLLLSIKMRLEKEIETYHNLLEGGQEDFESSGAGKIGLGGRGGSGGSYGRGSRGGSGGSYGGGGSGGGYGGGSGSRGGSGGSYGGGSGSGGGSGGGYGGGSGGGHSGGSGGGHSGGSGGNYGGGSGSGGGSGGGYGGGSGSRGGSGGSHGGGSGFGGESGGSYGGGEEASGSGGGYGGGSGKSSHS",
        )

    def test_fasta_get_sequence(self):
        f = parser.FastaIterator(self.handle, index=self.index)
        out = f.get_sequence("c1", 5, 30)
        self.assertEqual(
            "DDDKIVGGYTCAANSIPYQVSLNSGS", out, "Fasta get_sequence #1 Failure"
        )
        f.fasta_file.close()

    def test_fasta_index_build(self):
        f = parser.FastaIterator(self.handle)
        f.build_fasta_index()
        index = open(self.index, "r").read()
        self.assertEqual(
            index, "c1	231	4	231	232\nc2	623	240	70	71\nc3	645	878	70	71\n"
        )


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Fasta_Iterator)
    unittest.TextTestRunner(verbosity=2).run(suite)
