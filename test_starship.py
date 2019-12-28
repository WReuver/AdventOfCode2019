import unittest
from starship import Starship
from computer import IntCodeComputer, Operation

class TestStarship(unittest.TestCase):
    def test_instruction_parameter_length(self):
        self.assertEqual(IntCodeComputer.opcodes["1"].params, 4)
        self.assertEqual(IntCodeComputer.opcodes["2"].params, 4)
        self.assertEqual(IntCodeComputer.opcodes["3"].params, 4)
        self.assertEqual(IntCodeComputer.opcodes["99"].params, 1)

    def test_instruction_operation(self):
        self.assertEqual(IntCodeComputer.opcodes["1"].operation, Operation.add)
        self.assertEqual(IntCodeComputer.opcodes["2"].operation, Operation.multiply)
        self.assertEqual(IntCodeComputer.opcodes["3"].operation, Operation.divide)
        self.assertEqual(IntCodeComputer.opcodes["99"].operation, Operation.stop)

    def test_intCodeCalculator(self):
        # Initialize an intcode computer instance
        intCodeComp = IntCodeComputer()

        # Test the example int codes and verify the results
        intcode = [1, 0, 0, 0, 99]
        self.assertEqual(intCodeComp.compute(intcode), [2, 0, 0, 0, 99])

        intcode = [2, 3, 0, 3, 99]
        self.assertEqual(intCodeComp.compute(intcode), [2, 3, 0, 6, 99])

        intcode = [2, 4, 4, 5, 99, 0]
        self.assertEqual(intCodeComp.compute(intcode), [2, 4, 4, 5, 99, 9801])

        intcode = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        self.assertEqual(intCodeComp.compute(intcode), [30, 1, 1, 4, 2, 5, 6, 0, 99])

    def test_crossWiringAnalyzer(self):
        starship = Starship()

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

    def test_passwordAnalyzer(self):
        starship = Starship()

        passwordRange = 112233, 112234
        self.assertEqual(starship.validPasswordCombinations(*passwordRange), 1)
        passwordRange = 123444, 123445
        self.assertEqual(starship.validPasswordCombinations(*passwordRange), 0)
        passwordRange = 111122, 111123
        self.assertEqual(starship.validPasswordCombinations(*passwordRange), 1)

if __name__ == '__main__':
    unittest.main()