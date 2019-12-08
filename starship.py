from enum import Enum
import os

class Ops():
    @staticmethod
    def add(a, b):
        return int(a) + int(b)

    @staticmethod
    def multiply(a, b):
        return int(a) * int(b)

    @staticmethod
    def divide(a, b):
        return int(a)/int(b)

    @staticmethod
    def stop(a, b):
        return

class OpsDef(Enum):
    op = 0
    params = 1

class Starship:
    opcodes = {
        "1": { OpsDef.op: Ops.add,
              OpsDef.params: 3 },
        "2": { OpsDef.op: Ops.multiply,
               OpsDef.params: 3 },
        "3": { OpsDef.op: Ops.divide,
               OpsDef.params: 3 },
        "99": { OpsDef.op: Ops.stop,
                OpsDef.params: 1 }
    }

    def __init__(self):
        self.requiredFuel = 0
        self.memory = []

    # Fuel calculation
    def inputModules(self, modulesData):
        contents = open(modulesData)
        for line in contents.readlines():
            self.fuelCounterUpper(int(line))

    def fuelCounterUpper(self, mass):
        # Calculate the fuel and add it to the total required fuel
        fuel = int(mass / 3) - 2
        self.requiredFuel += fuel
        # Calculate the extra fuel required for the fuel
        self.fuelFuelCounterUpper(fuel)

    def fuelFuelCounterUpper(self, fuelMass):
        # Calculate the fuel and add it to the total required fuel if > 0,
        # then call this function with the same amount until the fuel is 0 or negative
        fuelFuel = int(fuelMass/3) - 2
        if fuelFuel > 0: 
            self.requiredFuel += fuelFuel
            self.fuelFuelCounterUpper(fuelFuel)
        else: 
            return

    # Intcode calculations
    def intcodeInput(self, intcodeFile):
        intcodes = open(intcodeFile).readline()
        intcodes = intcodes.strip('\n').split(',')

        # Set the 1202 program alarm state requirements
        intcodes[1] = '12'
        intcodes[2] = '2'

        self.intCodeCalculator(intcodes)
        print("Hello " + str(intcodes[0]))

    def intCodeCalculator(self, intcode):
        address = 0
        while address < len(intcode)-4:
            # Determine the opcode and the a & b values
            opcode = intcode[address]
            a = intcode[int(intcode[address+1])]
            b = intcode[int(intcode[address+2])]

            # Determine the result of the operation
            result = self.opcodes[str(opcode)][OpsDef.op](a, b)
            # Ensure 99 halts the program
            if result is None:
                break

            # Assign the result to the target position and increment the loop counter
            targetPos = int(intcode[address+3])
            intcode[targetPos] = result
            address += 4

if __name__ == '__main__':
    santaShip = Starship()

    # Day 1 
    santaShip.inputModules('input.txt')
    print(santaShip.requiredFuel)

    # Actual input
    santaShip.intcodeInput('opcodeinput.txt')

