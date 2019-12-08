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

class Starship:
    opcodes = {
        "1": Ops.add,
        "2": Ops.multiply,
        "3": Ops.divide,
        "99": Ops.stop
    }

    def __init__(self):
        self.requiredFuel = 0

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
        print(intcodes[0])

    def intCodeCalculator(self, intcode):
        i = 0
        while i < len(intcode)-4:
            # Determine the opcode and the a & b values
            opcode = intcode[i]
            a = intcode[int(intcode[i+1])]
            b = intcode[int(intcode[i+2])]

            # Determine the result of the operation
            result = self.opcodes[str(opcode)](a, b)
            # Ensure 99 halts the program
            if result is None:
                break

            # Assign the result to the target position and increment the loop counter
            targetPos = int(intcode[i+3])
            intcode[targetPos] = result
            i += 4

santaShip = Starship()

# Day 1 
santaShip.inputModules('input.txt')
print(santaShip.requiredFuel)

# Day 2
# Test input
testInput1 = [1, 0, 0, 0, 99]
testInput2 = [2, 3, 0, 3, 99]
testInput3 = [2, 4, 4, 5, 99, 0]
testInput4 = [1, 1, 1, 4, 99, 5, 6, 0, 99]

santaShip.intCodeCalculator(testInput1)
print(testInput1[0])

santaShip.intCodeCalculator(testInput2)
print(testInput2[3])

santaShip.intCodeCalculator(testInput3)
print(testInput3[5])

santaShip.intCodeCalculator(testInput4)
print(testInput4[0])
print(testInput4[4])

# Actual input
santaShip.intcodeInput('opcodeinput.txt')

