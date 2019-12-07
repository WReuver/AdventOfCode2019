from enum import Enum
import os

class Ops():
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        return a/b

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
        self.sum = 0

    def inputModules(self, input):
        contents = open('input.txt')
        for line in contents.readlines():
            self.fuelCounterUpper(int(line))

    def fuelCounterUpper(self, mass):
        fuel = int(mass / 3) - 2
        self.sum += fuel
        self.fuelFuelCounterUpper(fuel)

    def fuelFuelCounterUpper(self, fuelMass):
        fuelFuel = int(fuelMass/3) - 2
        if fuelFuel > 0: 
            self.sum += fuelFuel
            self.fuelFuelCounterUpper(fuelFuel)
        else: 
            return

    def intCodeCalculator(self, intcode):
        print(self.opcodes[0](1, 2))

santaShip = Starship()

# Day 1 
# santaShip.inputModules('input.txt')
# print(santaShip.sum)

# Day 2
santaShip.intCodeCalculator(1)
