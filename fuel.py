class FuelSystem:
    def __init__(self):
        self.requiredFuel = 0

    def computeRequiredFuel(self, modulesMassData):
        contents = open(modulesMassData)
        for line in contents.readlines():
            self.fuelCounterUpper(int(line))       

        return self.requiredFuel

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
