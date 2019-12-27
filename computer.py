from enum import Enum

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

class IntCodeComputer():
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

    def __init__(self):
        self.memory = []

    # Intcode calculations
    def compute(self, intCode, a='12', b ='2'):
        # Set the input parameters
        # Defaults to the required parameters to set the 1202 program alarm state
        intCode[1] = a
        intCode[2] = b

        self.memory = intCode
        self.run()
        return self.memory[0]

    def run(self):
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