from functools import partial
from action import Action
# Write a class to hold player information, e.g. what room they are in
# currently.


class Player:
    def __init__(self, name, loc):
        self.name = name
        self.loc = loc

    def move(self, dir):
        target = getattr(self.loc, dir)
        if target:
            self.loc = target
            return f'You moved into {self.loc.name}...'
        else:
            return False

    def situation(self):
        loc = self.loc
        (f'{loc.name}:')
        print(loc.desc)
        print('Choices:')
        choices = [('n', 'n_to'), ('e', 'e_to'), ('s', 's_to'), ('w', 'w_to')]
        choice_interface = {}
        for key, dir in choices:
            room = getattr(loc, dir)
            if room:
                desc = f'Move to {room.name}'
                act = partial(self.move, dir)
                choice_interface[key] = Action(key=key, act=act, desc=desc)
        return choice_interface
