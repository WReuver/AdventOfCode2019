import unittest
from starship import Starship, OpsDef, Ops

class TestStarship(unittest.TestCase):
    def test_op_parameters(self):
        self.assertEqual(Starship.opcodes["1"][OpsDef.params], 3)
        self.assertEqual(Starship.opcodes["2"][OpsDef.params], 3)
        self.assertEqual(Starship.opcodes["3"][OpsDef.params], 3)
        self.assertEqual(Starship.opcodes["99"][OpsDef.params], 1)

    def test_intCodeCalculator(self):
        starship = Starship()

        testInput1 = [1, 0, 0, 0, 99]
        testInput2 = [2, 3, 0, 3, 99]
        testInput3 = [2, 4, 4, 5, 99, 0]
        testInput4 = [1, 1, 1, 4, 99, 5, 6, 0, 99]

        starship.intCodeCalculator(testInput1)
        self.assertEqual(testInput1[0], 2)

        starship.intCodeCalculator(testInput2)
        self.assertEqual(testInput2[3], 6)

        starship.intCodeCalculator(testInput3)
        self.assertEqual(testInput3[5], 9801)

        starship.intCodeCalculator(testInput4)
        self.assertEqual(testInput4[0], 30)
        self.assertEqual(testInput4[4], 2)

if __name__ == '__main__':
    unittest.main()