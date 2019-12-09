import unittest
from starship import Starship, OpsDef, Ops

class TestStarship(unittest.TestCase):
    def test_op_parameters(self):
        self.assertEqual(Starship.opcodes["1"][OpsDef.params], 4)
        self.assertEqual(Starship.opcodes["2"][OpsDef.params], 4)
        self.assertEqual(Starship.opcodes["3"][OpsDef.params], 4)
        self.assertEqual(Starship.opcodes["99"][OpsDef.params], 1)

    def test_intCodeCalculator(self):
        starship = Starship()

        starship.memory = [1, 0, 0, 0, 99]
        starship.intCodeCalculator()
        self.assertEqual(starship.memory, [2, 0, 0, 0, 99])

        starship.memory = [2, 3, 0, 3, 99]
        starship.intCodeCalculator()
        self.assertEqual(starship.memory, [2, 3, 0, 6, 99])

        starship.memory = [2, 4, 4, 5, 99, 0]
        starship.intCodeCalculator()
        self.assertEqual(starship.memory, [2, 4, 4, 5, 99, 9801])

        starship.memory = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        starship.intCodeCalculator()
        self.assertEqual(starship.memory, [30, 1, 1, 4, 2, 5, 6, 0, 99])

    def test_crossWiringAnalyzer(self):
        starship = Starship()

        starship.mapWires(['R8', 'U5', 'L5', 'D3'])
        starship.mapWires(['U7', 'R6', 'D4', 'L4'])
        print(f"{starship.wireMap[0]}")
        print(f"{starship.wireMap[1]}")

        print(starship.analyzeWires())

if __name__ == '__main__':
    unittest.main()