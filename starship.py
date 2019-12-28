from enum import Enum
from util import determinant
from fuel import FuelSystem
from computer import IntCodeComputer
from wiring import Wiring
from password import PasswordAnalyzer
import os

class Starship:   
    def __init__(self):

        self.fuelSystem = FuelSystem()
        self.intCodeComputer = IntCodeComputer()
        self.wiring = Wiring()
        self.pwAnalyzer = PasswordAnalyzer()
        
    def computeRequiredFuel(self, modulesMassData):
        """
        Computes and returns the required amount of fuel for the modules 
        """

        return self.fuelSystem.computeRequiredFuel(modulesMassData)

    def computeIntCodeResults(self, intCodeFile, a='12', b='2'):
        # Read the input file
        intCode = open(intCodeFile).readline()
        # Process the input data to 
        intCode = intCode.strip('\n').split(',')

        # 
        return self.intCodeComputer.compute(intCode, a , b)

    def findClosestWiringIntersection(self, wiringData):
        self.wiring.loadWiringData(wiringData)

        return self.wiring.analyzeWires()

    def validPasswordCombinations(self, start, end):
        """
        Returns the number of valid password combinations within the given start to end range
        """
        
        return self.pwAnalyzer.validCombinations(start, end)
        

if __name__ == '__main__':
    santaShip = Starship()

    # Day 1 
    print(f"Required fuel: {santaShip.computeRequiredFuel('modules.txt')}")

    # Day 2 Puzzle 1
    print(f"1202 Program Alarm result: {santaShip.computeIntCodeResults('opcodes.txt')}")

    # Day 2 Puzzle 2
    for a in range(100):
        for b in range(100):
            if santaShip.computeIntCodeResults('opcodes.txt', a=a, b=b) == 19690720:
                print(f"({a}, {b}) input combination results in a 19690720 output.")

    # Day 3
    santaShip.findClosestWiringIntersection('wiring.txt')

    # Day 4 
    print(f"Valid passwords: {santaShip.validPasswordCombinations(271973, 785961)}")
