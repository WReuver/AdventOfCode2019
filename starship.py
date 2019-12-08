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
              OpsDef.params: 4 },
        "2": { OpsDef.op: Ops.multiply,
               OpsDef.params: 4 },
        "3": { OpsDef.op: Ops.divide,
               OpsDef.params: 4 },
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
    def findIntcodeOutput(self, intcodeFile, a='12', b ='2'):
        intcodes = open(intcodeFile).readline()
        intcodes = intcodes.strip('\n').split(',')

        # Set the input parameters
        # Defaults to the required parameters to set the 1202 program alarm state
        intcodes[1] = a
        intcodes[2] = b

        self.memory = intcodes
        self.intCodeCalculator()
        return self.memory

    def intCodeCalculator(self):
        instrPointer = 0
        while instrPointer < len(self.memory)-4:
            # Determine the opcode and the a & b values
            opcode = self.memory[instrPointer]
            a = self.memory[int(self.memory[instrPointer+1])]
            b = self.memory[int(self.memory[instrPointer+2])]

            # Determine the result of the operation
            result = self.opcodes[str(opcode)][OpsDef.op](a, b)
            # Ensure 99 halts the program
            if result is None:
                break

            # Assign the result to the target position and increment the loop counter
            targetPos = int(self.memory[instrPointer+3])
            self.memory[targetPos] = result
            instrPointer += self.opcodes[str(opcode)][OpsDef.params]

if __name__ == '__main__':
    santaShip = Starship()

    # Day 1 
    santaShip.inputModules('input.txt')
    print(f"Required fuel: {santaShip.requiredFuel}")

    # Day 2
    print(f"1202 Program Alarm result: {santaShip.findIntcodeOutput('opcodeinput.txt')[0]}")

    # Day 3
    for a in range(100):
        for b in range(100):
            if santaShip.findIntcodeOutput('opcodeinput.txt', a=a, b=b)[0] == 19690720:
                print(f" {100*a+b}")
