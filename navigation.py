
class OrbitMapper:
    def __init__(self):
        self.map = []
        self.keyMap = {}

    def loadMap(self, data):
        # Map all the orbits, each planet only has one key
        for orbit in data:
            # Split each orbit into a list containing the orbited and orbitee items
            p = orbit.split(')')
            
            # If the orbited item is not in the keyMap, add it with the orbitee as the value
            if p[0] not in self.keyMap:
                self.keyMap[p[0]] = [p[1]]
            # Else append it to the list of orbitees
            else:
                self.keyMap[p[0]].append(p[1])

            # If the orbitee item is not in the keyMap, add it
            if p[1] not in self.keyMap:
                self.keyMap[p[1]] = []

        # Replace each orbitee with an Orbit object, so that parent/child references are available
        for p in self.keyMap:
            self.keyMap[p] = Orbit(p, None, self.keyMap[p])

        # Finish loading the map by creating a nested list from the parent/child relationships
        self.mapChildren()

    def mapChildren(self):
        """
        Starting from the Center of Mass (COM) object, each child string is replaced with
        the corresponding Orbit object from the keyMap. In addition, each orbit object is 
        assigned a parent reference so that the orbit count can be calculated by navigating
        upwards through the parent references until the COM object (with parent 'None')
        is reached.
        """
        # Initiate the mapping with the Center of Mass (COM) object
        center = self.keyMap['COM']
        self.map = [center]

        # Initialize a queue with the COM object as the starting item
        queue = [self.map[0]]
        while len(queue) > 0:
            # Get the last item from the queue
            item = queue.pop()

            # Initialize a temporary list
            orbitObjects = []
            for child in item.children:
                if child in self.keyMap:
                    # Get the Orbit object from the keyMap
                    x = self.keyMap[child]
                    # Assign the parent reference
                    x.parent = item
                    # Add the item to the temporary list
                    orbitObjects.append(x)
                else:
                    print(f"No key for {child}")
            # Reassign the children variable to the list of Orbit objects
            item.children = orbitObjects
            # print(f"Name: {item.name}, Parent: {item.parent}, Children: {[i.name for i in item.children]}")

            # If the item has children, add each child to the queue
            if item.children:
                [queue.append(child) for child in item.children]

    def orbitCountChecksum(self):
        # Initialize a queue with the COM object as the starting item
        queue = [self.map[0]]
        # Direct and indirect orbit count variable
        orbitCountChecksum = 0

        while len(queue) > 0:
            # Get the last item from the queue
            item = queue.pop()

            parent = item.parent
            # Navigate up until the COM object (with parent 'None') is reached, incrementing the counter for each jump
            while parent is not None:
                orbitCountChecksum += 1
                parent = parent.parent

            # If the item has children, add each child to the queue
            if item.children:
                [queue.append(c) for c in item.children]

        return orbitCountChecksum

    def jumpDistance(self, start, end):
        if start in self.keyMap and end in self.keyMap:
            # Get the Orbit objects from the keyMap
            start = self.keyMap[start]
            end = self.keyMap[end]
            # Jump distance variable
            jumpCount = 0

            # Compute the path to the COM object for both start and end objects
            path1 = self.pathToCenter(start)
            path2 = self.pathToCenter(end)

            # Find the closest common parent
            commonParent = None
            for p in path1:
                if p in path2:
                    commonParent = p
                    break

            # Jumpcount is the sum of the indices of the commonParent item in both lists 
            #  plus 2 to offset the counting from zero
            if commonParent is not None:
                jumpCount = path1.index(commonParent) + path2.index(commonParent) + 2
                return jumpCount
            else:
                print("Failed to find common parent")
        elif start in self.keyMap:
            print(f"No entry found for object '{end}'")
        elif end in self.keyMap:
            print(f"No entry found for object '{start}'")
        else:
            print(f"No entries found for objects '{start}' and '{end}'")

    def pathToCenter(self, planet):
        orbits = planet.parent
        path = []
        while orbits is not None:
            orbits = orbits.parent
            path.append(orbits)

        return path

class Orbit:
    def __init__(self, name, parent=None, children=[]):
        self.name = name
        self.parent = parent
        self.children = children
