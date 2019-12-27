from enum import Enum
from util import determinant
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

    wiringDirs = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1)
    }

    def __init__(self):
        self.requiredFuel = 0
        self.memory = []
        self.wiring = []
        self.wireMap = []

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

    
    def loadWiringData(self, wiringDataFile):
        wiringDataRaw = open(wiringDataFile).readlines()

        for wireDataRaw in wiringDataRaw: 
            wireData = wireDataRaw.strip('\n').split(',')           
            # wiring.append(fixedWire)
            self.addWire(wireData)     


    def addWire(self, wire):
        # Newest index that isnt yet filled
        wireIndex = len(self.wireMap)
        # Set up the starting point
        self.wireMap.append([((0, 0), (0, 0))])
        # Get a reference to the newest wire
        newWireMap = self.wireMap[wireIndex]

        for seg in wire:
            # Determine segment direction (up, left, down, right) from the first character
            direction = self.wiringDirs[seg[0]]
            # Determine the length of the wire from the remaining characters
            length = int(seg[1:])            
            # Multiply the length by the direction value for the given plane [x, y]
            # [0, -1] * 800 = [0, -800]
            wireVector = tuple(i*length for i in direction)
            
            #[i*length for i in direction]

            # Determine the index of the wire segment
            wireSegIndex = len(self.wireMap[wireIndex])-1
            # print(f"wireVector: {wireVector}")
            # Calculate the coordinate results by adding the vector to the previous segment end point coordinates
            # previous = [50, 0], newest = [0, -50] results in [50, -50]
            # mult = ([x + y for x, y in zip(self.wireMap[wireIndex][wireSegIndex][1], wireVector)])

            zipper = tuple(x + y for x,y in zip(newWireMap[wireSegIndex][1], wireVector))
            # print(f"Seg: {self.wireMap[wireIndex][wireSegIndex][0]}")
            # print(f"Zipper: {zipper}")

            newWireMap.append((newWireMap[wireSegIndex][1], zipper))

    def analyzeWires(self):
        intersections = []
        for wire1 in self.wireMap[0]:
            for wire2 in self.wireMap[1]:
                result = self.compareWires(wire1, wire2)
                print(f"Result: {result}")
                if result is not None:
                    intersections.append(result)    

        
        return self.closestIntersection(intersections)

    def compareWires(self, wire1, wire2):
        dx = (wire1[0][0] - wire1[1][0], wire2[0][0] - wire2[1][0])
        dy = (wire1[0][1] - wire1[1][1], wire2[0][1] - wire2[1][1])

        div = determinant(dx, dy)

        if div == 0:
            return None
        else:        
            d = (determinant(*wire1), determinant(*wire2))
            x = determinant(d, dx) / div
            y = determinant(d, dy) / div

            x1 = wire1[0][0] if wire1[0][0] < wire1[0][1] else  wire1[0][1]
            x2 = wire1[0][0] if wire1[0][0] > wire1[0][1] else  wire1[0][1]

            y1 = wire1[1][0] if wire1[1][0] < wire1[1][1] else  wire1[1][1]
            y2 = wire1[1][0] if wire1[1][0] > wire1[1][1] else  wire1[1][1]

            if not (x == 0 and y == 0):
                if x1 <= x <= x2 and y1 <= y <= y2: 
                    return x, y

    def closestIntersection(self, intersections):
        closest = 99999999

        for sec in intersections:
            dist = abs(sec[0] + sec[1])
            if dist < closest:
                print(f"Closest is now: {sec} with a distance of {dist}")
                closest = dist
        
        return closest

if __name__ == '__main__':
    santaShip = Starship()

    # Day 1 
    santaShip.inputModules('modules.txt')
    print(f"Required fuel: {santaShip.requiredFuel}")

    # Day 2 Puzzle 1
    print(f"1202 Program Alarm result: {santaShip.findIntcodeOutput('opcodes.txt')[0]}")

    # Day 2 Puzzle 2
    for a in range(100):
        for b in range(100):
            if santaShip.findIntcodeOutput('opcodes.txt', a=a, b=b)[0] == 19690720:
                print(f"({a}, {b}) input combination results in a 19690720 output.")

    # Day 3
    santaShip.loadWiringData('wiring.txt')
