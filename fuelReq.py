import os

class Starship:
    def __init__(self):
        self.sum = 0

    def inputModules(self, input):
        contents = open('input.txt')
        for line in contents.readlines():
            self.fuelCounterUpper(int(line))

    def fuelCounterUpper(self, mass):
        fuel = int(mass / 3) - 2
        self.sum += fuel
        self.fuelFuelCounterUpper(fuel)

    def fuelFuelCounterUpper(self, fuelMass):
        fuelFuel = int(fuelMass/3) - 2
        if fuelFuel > 0: 
            self.sum += fuelFuel
            self.fuelFuelCounterUpper(fuelFuel)
        else: 
            return

santaShip = Starship()
santaShip.inputModules('input.txt')
print(santaShip.sum)
