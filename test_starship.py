import unittest
from starship import Starship
from computer import IntCodeComputer
from navigation import OrbitMapper

class TestStarship(unittest.TestCase):
    # def test_instruction_parameter_length(self):
    #     self.assertEqual(IntCodeComputer.opcodes["01"].length, 4)
    #     self.assertEqual(IntCodeComputer.opcodes["02"].length, 4)
    #     self.assertEqual(IntCodeComputer.opcodes["03"].length, 2)
    #     self.assertEqual(IntCodeComputer.opcodes["04"].length, 2)
    #     self.assertEqual(IntCodeComputer.opcodes["99"].length, 1)

    # def test_instruction_operation(self):
    #     self.assertEqual(IntCodeComputer.opcodes["01"].operation, IntCodeComputer.add)
    #     self.assertEqual(IntCodeComputer.opcodes["02"].operation, IntCodeComputer.multiply)
    #     self.assertEqual(IntCodeComputer.opcodes["03"].operation, IntCodeComputer.insert)
    #     self.assertEqual(IntCodeComputer.opcodes["04"].operation, IntCodeComputer.extract)
    #     self.assertEqual(IntCodeComputer.opcodes["99"].operation, IntCodeComputer.stop)

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

    # def test_crossWiringAnalyzer(self):
    #     starship = Starship()

    #     wire1 = ([6, 3], [2, 3])
    #     wire2 = ([3, 5], [3, 2])
    #     self.assertEqual(starship.compareWires(wire1, wire2), (3.0, 3.0))

    #     wire1 = ([6, 7], [6, 3])
    #     wire2 = ([8, 5], [3, 5])
    #     self.assertEqual(starship.compareWires(wire1, wire2), (6.0, 5.0))

    #     starship = Starship()
    #     starship.addWire(['R8', 'U5', 'L5', 'D3'])
    #     starship.addWire(['U7', 'R6', 'D4', 'L4'])
    #     print(f"{starship.wireMap[0]}")
    #     print(f"{starship.wireMap[1]}")
    #     print(starship.analyzeWires())

    #     starship = Starship()
    #     starship.addWire(['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']) 
    #     starship.addWire(['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'])
    #     print(f"{starship.wireMap[0]}")
    #     print(f"{starship.wireMap[1]}")
    #     print(starship.analyzeWires())
    #     # starship.addWire(['R98', 'U47', 'R26', 'D63', 'R33', 'U'])

    def test_passwordAnalyzer(self):
        starship = Starship()

        passwordRange = 112233, 112234
        self.assertEqual(starship.validPasswordCombinations(*passwordRange), 1)
        passwordRange = 123444, 123445
        self.assertEqual(starship.validPasswordCombinations(*passwordRange), 0)
        passwordRange = 111122, 111123
        self.assertEqual(starship.validPasswordCombinations(*passwordRange), 1)

    def test_diagnostics(self):
        intCodeComp = IntCodeComputer()

        # Position mode - Input equal to 8 outputs 1, else 0        
        program = [3,9,8,9,10,9,4,9,99,-1,8]
        self.assertEqual(intCodeComp.diagnostics(program, 8), [1])
        self.assertEqual(intCodeComp.diagnostics(program, 0), [0])

        # Position mode - Input less than 8 outputs 1, else 0
        program = [3,9,7,9,10,9,4,9,99,-1,8]
        self.assertEqual(intCodeComp.diagnostics(program, 2), [1])
        self.assertEqual(intCodeComp.diagnostics(program, 8), [0])

        # Immediate mode - Input equal to 8 outputs 1, else 0
        program = [3,3,1108,-1,8,3,4,3,99]
        self.assertEqual(intCodeComp.diagnostics(program, 8), [1])
        self.assertEqual(intCodeComp.diagnostics(program, 0), [0])

        # Immediate mode - Input less than 8 outputs 1, else 0
        program = [3,3,1107,-1,8,3,4,3,99]
        self.assertEqual(intCodeComp.diagnostics(program, 6), [1])
        self.assertEqual(intCodeComp.diagnostics(program, 9), [0])

        # Jump tests, position mode
        program = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
        self.assertEqual(intCodeComp.diagnostics(program, 0), [0])
        self.assertEqual(intCodeComp.diagnostics(program, 5), [1])
        self.assertEqual(intCodeComp.diagnostics(program, -1), [1])

        # Jump tests, immediate mode
        program = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
        self.assertEqual(intCodeComp.diagnostics(program, 0), [0])
        self.assertEqual(intCodeComp.diagnostics(program, 5), [1])
        self.assertEqual(intCodeComp.diagnostics(program, -1), [1])

        program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

        # ID < 8
        self.assertEqual(intCodeComp.diagnostics(program, 0), [999])
        self.assertEqual(intCodeComp.diagnostics(program, 7), [999])

        # ID == 8
        self.assertEqual(intCodeComp.diagnostics(program, 8), [1000])

        # ID > 8
        self.assertEqual(intCodeComp.diagnostics(program, 9), [1001])
        self.assertEqual(intCodeComp.diagnostics(program, 10), [1001])

    def test_orbitChecksum(self):
        # Orbit count checksum test
        orbitMapper = OrbitMapper()
        testOrbitMap = ["COM)B",
                        "B)C",
                        "C)D",
                        "D)E",
                        "E)F",
                        "B)G",
                        "G)H",
                        "D)I",
                        "E)J",
                        "J)K",
                        "K)L"]

        orbitMapper.loadMap(testOrbitMap)
        self.assertEqual(orbitMapper.orbitCountChecksum(), 42)

        # Jump distance from planet 'YOU' to planet 'SAN' test
        orbitMapper = OrbitMapper()
        testOrbitMap = ["COM)B",
                        "B)C",
                        "C)D",
                        "D)E",
                        "E)F",
                        "B)G",
                        "G)H",
                        "D)I",
                        "E)J",
                        "J)K",
                        "K)L",
                        "K)YOU",
                        "I)SAN"]

        orbitMapper.loadMap(testOrbitMap)
        self.assertEqual(orbitMapper.jumpDistance("YOU", "SAN"), 4)

if __name__ == '__main__':
    unittest.main()
