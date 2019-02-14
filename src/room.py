import textwrap
# Implement a class to hold room information. This should have name and
# description attributes.


class Room:
    def __init__(self, name, desc, contents=[], is_light=True):
        self.name = name
        self.desc = textwrap.TextWrapper().fill(desc)
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.contents = contents
        self.is_light = is_light
