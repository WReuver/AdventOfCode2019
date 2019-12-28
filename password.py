import re

class PasswordAnalyzer:
    def __init__(self):
        pass

    def validCombinations(self, startVal, endVal):
        # Initialize counter variable
        validPasswords = 0
        # Evaluate each sequence in the range
        for n in range(startVal, endVal):
            numStr = str(n)
            # If a sequence matches the two required patterns, increment the valid password counter
            if self.incrementsOrEqualsLeftToRight(numStr) and self.containsAdjacentDigits(numStr):
                validPasswords += 1

        return validPasswords

    def containsAdjacentDigits(self, password):
        series = [['0']]

        # Find all character series
        for c in password:        
            # Ongoing series
            if c == series[len(series)-1][0]:
                series[len(series)-1].append(c)
            # Start a new series
            else:
                series.append([c])

        # Evaluate if a valid series is present
        for s in series:
            if len(s) == 2:
                return True

        # Did not find any valid series
        return False

    def incrementsOrEqualsLeftToRight(self, numStr):
        # Initialize comparison variable
        prev = '0'
        # Compare each character to the previous one
        for c in numStr:
            if c < prev:
                return False
            prev = c
        # Passed
        return True

if __name__ == "__main__":
    pwAnalyzer = PasswordAnalyzer()
    print(pwAnalyzer.validCombinations(111122, 111123))
