import enum
from computer import IntCodeComputer
from itertools import permutations

class AmplifierPhaser:
    def __init__(self):
        self.comp = IntCodeComputer()
        A = Amplifier()
        B = Amplifier()
        C = Amplifier()
        D = Amplifier()
        E = Amplifier()
        self.amps = (A, B, C, D, E)

    def findMaxSignalSetting(self, program, minPhase, maxPhase):
        settings = self.phaseSettings(minPhase, maxPhase)
        maxOutput = 0

        for s in settings:
            output = self.run(program, s)
            if output > maxOutput:
                maxOutput = output

        return maxOutput

    def run(self, program, phaseSettings):
        phasePointer = 0

        for i, amp in enumerate(self.amps):
            amp.output =  self.comp.computeOut(program, input=[phaseSettings[phasePointer], amp.input])[0]

            if i + 1 < len(self.amps):
                self.amps[i+1].input = amp.output
                phasePointer += 1
            else:
                return amp.output

    def phaseSettings(self, start, end):
        r = range(start, end+1)
        return list(permutations(r, len(r)))

class Amplifier:
    def __init__(self):
        self.input = 0
        self.output = 0

if __name__ == "__main__":
    ap = AmplifierPhaser()
    setting = [0, 0, 0, 0, 0]
    print(ap.phaseSettings())
    # for i in range(10):
    #     setting = ap.nextPhaseSetting(setting)
    #     print(setting)