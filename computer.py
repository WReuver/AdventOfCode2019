import math
from enum import Enum

class Operation():
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
    def insert(a, index, memory=None):
        if memory is not None:
            memory[index] = a

    @staticmethod
    def extract(index, memory):
        if memory is not None:
            return memory[index]

    @staticmethod
    def stop(a, b):
        return


class ParameterMode(Enum):
    Position = 0,
    Immediate = 1


class Instruction:
    def __init__(self, operation: Operation, length):        
        self.operation = operation
        self.length = length


class IntCodeComputer():
    opcodes = {
        "01": Instruction(Operation.add, 4),
        "02": Instruction(Operation.multiply, 4),
        "03": Instruction(Operation.insert, 2),
        "04": Instruction(Operation.extract, 2),
        "99": Instruction(Operation.stop, 1)
    }

    def __init__(self):
        self.memory = []
        self.pointer = 0

    def diagnostics(self, id):
        pass

    def compute(self, intCode, a=None, b=None):
        # Set the input parameters
        # Defaults to the required parameters to set the 1202 program alarm state
        if a:
            intCode[1] = a
        if b:
            intCode[2] = b

        self.memory = intCode
        self.run()
        return self.memory

    def run(self):
        self.pointer = 0
        while self.pointer < len(self.memory) - 4:
            # Get the opcode from the current pointer position
            opcode = self.memory[self.pointer]

            # Decode the opcode
            opcode = self.splitOpcode(opcode)

            # Determine the operation
            op = opcode[0]

            # Get the first and second parameter
            a = self.memory[int(self.memory[self.pointer+1])]
            b = self.memory[int(self.memory[self.pointer+2])]
            # Get the target index

            # Determine the result of the operation
            result = self.opcodes[op].operation(a, b)

            # If the result equals the '99' opcode return value, halt the program
            if result is None:
                break

            # Assign the result to the target position and increment the loop counter
            targetPos = int(self.memory[self.pointer+3])
            self.memory[targetPos] = result

            # Increment the pointer position by the number of instruction parameters
            self.pointer += self.opcodes[op].length

    def splitOpcode(self, opcode):
        opcode = str(opcode)
        # print(f"Evaluating opcode '{opcode}'")

        params = len(opcode) - 2
        # print(f"Nr. of params: {params}")

        opcode = opcode.zfill(5)

        paramModes = list(opcode[:-2])

        arr = [opcode[-2:]]
        while paramModes:
            arr.append(paramModes.pop())

        # print(arr)
        # arr = [int(x) for x in arr]
        return arr


if __name__ == "__main__":
    comp = IntCodeComputer()

    # intcode = [1002, 4, 3, 4, 33]
    # print(comp.compute(intcode))
    comp.splitOpcode(2)
    