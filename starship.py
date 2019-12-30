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
    print(f"== Day 1 - Star One and Two ==\nRequired fuel: {santaShip.computeRequiredFuel('modules.txt')}")

    # Day 2 Puzzle 1
    print(f"== Day 2 - Star One ==\n1202 Program Alarm result: {santaShip.computeIntCodeResults('opcodes.txt')[0]}")

    # Day 2 Puzzle 2
    for a in range(100):
        for b in range(100):
            if santaShip.computeIntCodeResults('opcodes.txt', a=a, b=b)[0] == 19690720:
                print(f"-- Day 2 - Star Two --\nInput combination a = {a}, b = {b} results in a 19690720 output.")

    # Day 3
    # santaShip.findClosestWiringIntersection('wiring.txt')

    # Day 4 
    print(f"== Day 4 - Star One and Two ==\nValid passwords: {santaShip.validPasswordCombinations(271973, 785961)}")
