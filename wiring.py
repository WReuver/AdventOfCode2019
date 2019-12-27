class Wiring:
    def __init__(self):
        pass    

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Segment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end