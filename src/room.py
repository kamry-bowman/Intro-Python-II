# Implement a class to hold room information. This should have name and
# description attributes.


class Room:
    def __init__(self, name, desc, contents=[]):
        self.name = name
        self.desc = desc
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.contents = contents
