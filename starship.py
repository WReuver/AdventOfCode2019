from enum import Enum
from util import determinant
from fuel import FuelSystem
from computer import IntCodeComputer
from wiring import Wiring
from password import PasswordAnalyzer
from navigation import OrbitMapper
from decoding import SpaceImageFormatDecoder
import os

class Starship:   
    def __init__(self):

        self.fuelSystem = FuelSystem()
        self.intCodeComputer = IntCodeComputer()
        self.wiring = Wiring()
        self.pwAnalyzer = PasswordAnalyzer()
        self.orbitMapper = OrbitMapper()
        
    def computeRequiredFuel(self, modulesMassData):
        """
        Computes and returns the required amount of fuel for the modules 
        """

        return self.fuelSystem.computeRequiredFuel(modulesMassData)

    def computeIntCodeResults(self, intCodeFile, a='12', b='2'):
        intCode = open(intCodeFile).readline()
        intCode = intCode.strip('\n').split(',')

        return self.intCodeComputer.compute(intCode, a , b)

    def runIntCodeDiagnostics(self, intCodeFile, id):
        intCode = open(intCodeFile).readline()
        intCode = intCode.strip('\n').split(',')

        return self.intCodeComputer.diagnostics(intCode, id)

    def findClosestWiringIntersection(self, wiringData):
        self.wiring.loadWiringData(wiringData)

        return self.wiring.analyzeWires()

    def validPasswordCombinations(self, start, end):
        """
        Returns the number of valid password combinations within the given start to end range
        """        
        return self.pwAnalyzer.validCombinations(start, end)

    def downloadOrbitMap(self, mapFile):
        mapData = open(mapFile).readlines()
        mapData = [p.strip('\n') for p in mapData]

        self.orbitMapper.loadMap(mapData)
        return self.orbitMapper.orbitCountChecksum()

    def findJumpDistance(self, start, end):
        return self.orbitMapper.jumpDistance(start, end)

    def imageChecksum(self, imageFile, width, height):
        decoder = SpaceImageFormatDecoder(imageFile)
        return decoder.checksum(width, height)

    def decodeBiosPassword(self, imageFile, width, height):
        decoder = SpaceImageFormatDecoder(imageFile)
        return decoder.decode(width, height)

if __name__ == '__main__':
    santaShip = Starship()

    # Day 1 
    print(f"== Day 1 - Star One and Two ==\n\tRequired fuel: {santaShip.computeRequiredFuel('modules.txt')}")

    # Day 2 Puzzle 1
    print(f"== Day 2 - Star One ==\n\t1202 Program Alarm result: {santaShip.computeIntCodeResults('opcodes.txt')[0]}")

    # Day 2 Puzzle 2
    for a in range(100):
        for b in range(100):
            if santaShip.computeIntCodeResults('opcodes.txt', a=a, b=b)[0] == 19690720:
                print(f"-- Day 2 - Star Two --\n\tInput combination a = {a}, b = {b} results in a 19690720 output.")

    # Day 3
    # santaShip.findClosestWiringIntersection('wiring.txt')

    # Day 4 
    print(f"== Day 4 - Star One and Two ==\n\tValid passwords: {santaShip.validPasswordCombinations(271973, 785961)}")

    # Day 5
    print(f"== Day 5 - Star One ==\n\tDiagnostic Result: {santaShip.runIntCodeDiagnostics('diagnostics.txt', 1)}")

    print(f"-- Day 5 - Star Two --\n\tDiagnostic Result: {santaShip.runIntCodeDiagnostics('diagnostics.txt', 5)}")

    # Day 6 
    print(f"== Day 6 - Star One ==\n\tOrbit Count Checksum: {santaShip.downloadOrbitMap('orbitmap.txt')}")
    print(f"-- Day 6 - Star Two --\n\tYOU to SAN jump distance: {santaShip.findJumpDistance('YOU', 'SAN')}")

    # Day 8
    print(f"== Day 8 - Star one ==\n\tImage checksum result: {santaShip.imageChecksum('biosimage.sif', 25, 6)}")
    print(f"-- Day 8 - Star Two --\n\tDecoded Bios Password Image: \n")
    santaShip.decodeBiosPassword('biosimage.sif', 25, 6)
