import math
from enum import Enum


class ParameterMode():
    Position = 0
    Immediate = 1
    

class Parameter():
    One = 1
    Two = 2
    Three = 3


class Instruction:
    def __init__(self, operation, length):        
        self.operation = operation
        self.length = length


class IntCodeComputer():

    def __init__(self):
        self.memory = []
        self.pointer = 0
        self.didPointerMove = False
        self.opcodes = {
            "01": Instruction(self.add, 4),
            "02": Instruction(self.multiply, 4),
            "03": Instruction(self.insert, 2),
            "04": Instruction(self.extract, 2),
            "05": Instruction(self.jumpIfTrue, 3),
            "06": Instruction(self.jumpIfFalse, 3),
            "07": Instruction(self.lessThan, 4),
            "08": Instruction(self.equals, 4),
            "99": Instruction(self.stop, 1)
        }
        self.output = []

    def diagnostics(self, program, id):
        # Load the program into memory
        self.memory = [int(i) for i in program]
        # Empty the diagnostic results buffer
        self.output = []
        # Run the program with the provided id value and report the diagnostic results
        self.run([id])
        return self.output

    def computeOut(self, program, input=None):
        self.memory = [int(i) for i in program]
        self.output = []
        # Run the program and return the memory as the result
        self.run(input)
        return self.output

    def compute(self, program, a=None, b=None, input=None):
        # Load the program into memory
        self.memory = [int(i) for i in program]

        # Set the input parameters
        # Defaults to the required parameters to set the 1202 program alarm state
        if a:
            self.memory[1] = a
        if b:
            self.memory[2] = b
            
        # Run the program and return the memory as the result
        self.run(input)
        return self.memory

    def run(self, input=None):
        self.pointer = 0
        self.didPointerMove = False
        self.inputPointer = 0

        while self.pointer < len(self.memory) - 1:
            # Get the opcode from the current pointer position
            opcode = self.memory[self.pointer]

            # Decode the opcode
            opcode = self.splitOpcode(opcode)

            # Determine the operation
            op = opcode[0]

            # 
            if op == "99":
                break
            elif op == "03" and input is not None:
                self.opcodes[op].operation(opcode, input[self.inputPointer])
                self.inputPointer += 1
            else:
                self.opcodes[op].operation(opcode)            

            # Increment the pointer position by the number of instruction parameters
            if not self.didPointerMove:
                self.pointer += self.opcodes[op].length
            else:
                self.didPointerMove = False

    def splitOpcode(self, opcode):
        # Convert opcode to string so it can be easily manipulated
        opcode = str(opcode)
        # Pad the opcode with zeroes so it is five characters long
        opcode = opcode.zfill(5)

        # The parameter mode portion of the opcode includes all but the last two characters
        paramModes = list(opcode[:-2])

        # Start the opcode list with the operation (last 2 characters)
        opcodeList = [opcode[-2:]]

        # Fill the opcode list with the remaining parameter modes and return it
        #   Parameter modes are stored right to left, so popping the parameter modes and appending
        #    them results in a left to right order
        while paramModes:
            opcodeList.append(paramModes.pop())

        return opcodeList

    def movePointer(self, val):
        self.pointer = val
        self.didPointerMove = True

    def add(self, code):
        a, b = self.getParameters(code, 2)

        # Determine the target (write) position
        targetPos = int(self.memory[self.pointer + 3])

        # Execute the instruction if the values are valid
        if a is not None and b is not None and targetPos is not None:
            self.memory[targetPos] = int(a) + int(b)
            return self.memory[targetPos]
        else:
            print(f"Addition Instruction Error: Value {a}, {b} or {targetPos} is not a number or a string")

    def multiply(self, code):
        a, b = self.getParameters(code, 2)

        # Determine the target (write) position
        targetPos = int(self.memory[self.pointer + 3])

        # Execute the instruction if the values are valid
        if a is not None and b is not None and targetPos is not None:
            self.memory[targetPos] = int(a) * int(b)
            return self.memory[targetPos]
        else:
            print(f"Multiplication Instruction Error: Value {a}, {b} or {targetPos} is not a number or a string")

    def insert(self, code, val):
        a = self.memory[self.pointer+1]
        if a is not None:
            self.memory[a] = val
        else:
            print(f"Insertion Error: Value {a} is not a number or a string")

    def extract(self, code):
        a = self.memory[self.pointer + 1]
        # If the parameter is in position mode, append the value at the position
        if int(code[Parameter.One]) == ParameterMode.Position:
            self.output.append(self.memory[a])
        # Else append the value
        else:
            self.output.append(a)

    def jumpIfTrue(self, code):
        a, b = self.getParameters(code, 2)

        # Do nothing if the first parameter is a zero
        if a == 0:
            return
        else:
            self.movePointer(b)    

    def jumpIfFalse(self, code):
        a, b = self.getParameters(code, 2)

        # Do nothing if the first parameter is a zero
        if a != 0:
            return
        else:
            self.movePointer(b)

    def lessThan(self, code):
        a, b = self.getParameters(code, 2)
        targetPos = self.memory[self.pointer+3]

        if a < b:
            self.memory[targetPos] = 1
        else:
            self.memory[targetPos] = 0 

    def equals(self, code):
        a, b = self.getParameters(code, 2)
        targetPos = self.memory[self.pointer+3]

        if a == b:
            self.memory[targetPos] = 1
        else:
            self.memory[targetPos] = 0        

    def stop(self):
        return None

    def getParameters(self, opcodeList, length):
        # Determine the parameter mode for the first parameter, and return its value
        if int(opcodeList[Parameter.One]) == ParameterMode.Position:
            a = self.memory[self.memory[self.pointer+1]]
        else:
            a = self.memory[self.pointer+1]

        if length < 2:
            return a,

        if int(opcodeList[Parameter.Two]) == ParameterMode.Position:
            b = self.memory[self.memory[self.pointer+2]]
        else:
            b = self.memory[self.pointer+2]

        if length < 3:
            return a, b

        