import math
from enum import Enum

class Operation():
    pass
    # @staticmethod
    # def add(code, memory, pointer):
    #     if int(code[Parameter.One]) == ParameterMode.Position:
    #         a = memory[int(memory[pointer+1])]
    #     else:
    #         a = memory[pointer+1]

    #     if int(code[Parameter.Two]) == ParameterMode.Position:
    #         b = memory[int(memory[pointer+2])]
    #     else:
    #         b = memory[pointer+2]

    #     if int(code[Parameter.Three]) == ParameterMode.Position:
    #         targetPos = memory[int(memory[pointer+3])]
    #     else: 
    #         pass

    #     if a is not None and b is not None:
    #         return int(a) + int(b)
    #     else:
    #         return None

    #     # return int(a) + int(b)

    # @staticmethod
    # def multiply(a, b):
    #     return int(a) * int(b)

    # @staticmethod
    # def divide(a, b):
    #     return int(a)/int(b)

    # @staticmethod
    # def insert(a, index, memory=None):
    #     if memory is not None:
    #         memory[index] = a

    # @staticmethod
    # def extract(index, memory):
    #     if memory is not None:
    #         return memory[index]

    # @staticmethod
    # def stop(a, b):
    #     return


class ParameterMode():
    Position = 0
    Immediate = 1

class Parameter():
    One = 1
    Two = 2
    Three = 3


class Instruction:
    def __init__(self, operation: Operation, length):        
        self.operation = operation
        self.length = length


class IntCodeComputer():

    def __init__(self):
        self.memory = []
        self.pointer = 0
        self.opcodes = {
            "01": Instruction(self.add, 4),
            "02": Instruction(self.multiply, 4),
            "03": Instruction(self.insert, 2),
            "04": Instruction(self.extract, 2),
            "99": Instruction(self.stop, 1)
        }

    def diagnostics(self, program, id):
        self.memory = program
        self.run(id)
        return self.memory

    def compute(self, program, a=None, b=None):
        # Set the input parameters
        # Defaults to the required parameters to set the 1202 program alarm state
        if a:
            program[1] = a
        if b:
            program[2] = b

        self.memory = program
        self.run()
        return self.memory

    def run(self, testInput=None):
        self.pointer = 0
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
            elif op == "03" and testInput:
                self.opcodes[op].operation(opcode, testInput)
            else:
                self.opcodes[op].operation(opcode)            

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

    def add(self, code):
        # a = None
        # b = None

        if int(code[Parameter.One]) == ParameterMode.Position:
            a = self.memory[int(self.memory[self.pointer+1])]
        else:
            a = self.memory[self.pointer+1]

        if int(code[Parameter.Two]) == ParameterMode.Position:
            b = self.memory[int(self.memory[self.pointer+2])]
        else:
            b = self.memory[self.pointer+2]

        # if int(code[Parameter.Three]) == ParameterMode.Position:
        targetPos = int(self.memory[self.pointer + 3])
        # else: 
        #     targetPos = int(self.memory[self.pointer + 3])

        if a is not None and b is not None and targetPos is not None:
            self.memory[targetPos] = int(a) + int(b)
            return self.memory[targetPos]
        else:
            # TODO Error
            return None

    def multiply(self, code):
        a = None
        b = None

        if int(code[Parameter.One]) == int(ParameterMode.Position):
            a = self.memory[int(self.memory[self.pointer+1])]
        else:
            a = self.memory[self.pointer+1]

        if int(code[Parameter.Two]) == ParameterMode.Position:
            b = self.memory[int(self.memory[self.pointer+2])]
        else:
            b = self.memory[self.pointer+2]

        if int(code[Parameter.Three]) == ParameterMode.Position:
            targetPos = int(self.memory[self.pointer + 3])
            # self.memory[int(self.memory[self.pointer+3])]
        else: 
            targetPos = int(self.memory[self.pointer + 3])

        if a is not None and b is not None:
            self.memory[targetPos] = int(a) * int(b)
            return self.memory[targetPos]
        else:
            # TODO Error
            return None

    def insert(self, code, val):
        a = code[1]
        self.memory[a] = val

    def extract(self, code):
        a = code[1]
        return self.memory[a]

    def stop(self):
        return None

if __name__ == "__main__":
    comp = IntCodeComputer()

    intcode = [1002, 4, 3, 4, 33]
    # comp.memory = intcode
    print(comp.compute(intcode))
    # a = "3"
    # print(f"{comp.splitOpcode(a)}")
    # print(f"{comp.add([0, 1, 2, 0])}")
    # print(f"{comp.splitOpcode(1002)}")

