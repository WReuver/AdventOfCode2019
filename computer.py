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
    def stop(a, b):
        return


class Instruction:
    def __init__(self, operation: Operation, params):        
        self.operation = operation
        self.params = params

class IntCodeComputer():
    opcodes = {
        "1": Instruction(Operation.add, 4),
        "2": Instruction(Operation.multiply, 4),
        "3": Instruction(Operation.divide, 4),
        "99": Instruction(Operation.stop, 1)
    }

    def __init__(self):
        self.memory = []

    # Intcode calculations
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
        instrPointer = 0
        while instrPointer < len(self.memory)-4:
            # Determine the opcode and the a & b values
            opcode = self.memory[instrPointer]
            a = self.memory[int(self.memory[instrPointer+1])]
            b = self.memory[int(self.memory[instrPointer+2])]

            # Determine the result of the operation
            result = self.opcodes[str(opcode)].operation(a, b)
            # Ensure 99 halts the program
            if result is None:
                break

            # Assign the result to the target position and increment the loop counter
            targetPos = int(self.memory[instrPointer+3])
            self.memory[targetPos] = result
            instrPointer += self.opcodes[str(opcode)].params