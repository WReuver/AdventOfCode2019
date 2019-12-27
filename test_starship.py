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


        # print(starship.analyzeWires2())
        wire1 = ([6, 3], [2, 3])
        wire2 = ([3, 5], [3, 2])
        self.assertEqual(starship.compareWires(wire1, wire2), (3.0, 3.0))

        wire1 = ([6, 7], [6, 3])
        wire2 = ([8, 5], [3, 5])
        self.assertEqual(starship.compareWires(wire1, wire2), (6.0, 5.0))

        starship = Starship()
        starship.addWire(['R8', 'U5', 'L5', 'D3'])
        starship.addWire(['U7', 'R6', 'D4', 'L4'])
        print(f"{starship.wireMap[0]}")
        print(f"{starship.wireMap[1]}")
        print(starship.analyzeWires())

        starship = Starship()
        starship.addWire(['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']) 
        starship.addWire(['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'])
        print(f"{starship.wireMap[0]}")
        print(f"{starship.wireMap[1]}")
        print(starship.analyzeWires())
        # starship.addWire(['R98', 'U47', 'R26', 'D63', 'R33', 'U'])

if __name__ == '__main__':
    unittest.main()