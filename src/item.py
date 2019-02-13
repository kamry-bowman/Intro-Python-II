class Item:
    def __init__(self, name, desc=None):
        self.name = name
        self.desc = desc or 'a ' + name
