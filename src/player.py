from functools import partial
from collections import OrderedDict
from action import Action

from item import Item
# Write a class to hold player information, e.g. what room they are in
# currently.


class Player:
    def __init__(self, name, loc):
        self.name = name
        self.loc = loc
        self.current_situation = None
        self.inventory = []

    def move(self, dir):
        target = getattr(self.loc, dir)
        if target:
            self.loc = target
            return f'You moved into {self.loc.name}...'
        else:
            return False

    def take(self, item):
        if not isinstance(item, Item):
            raise Exception('Can only take items')
        self.inventory.append(item)
        self.loc.contents.remove(item)
        return f'Picked up {item.name}'

    def look(self):
        contents = self.loc.contents
        if not contents:
            string = "You don't see anything of interest."
            self.clear_situation()
            return string
        else:
            def pickup(item):
                result = self.take(item) + '\n'
                result += self.look() or ''
                return result

            string = 'Looking around, you notice the following: \n'
            choices = OrderedDict()
            for index, item in enumerate(contents):
                num = str(index + 1)
                string += ' ' * 10
                string += f'{num}. {item.desc}\n'
                choices[num] = Action(
                    key=num,
                    desc=f'pick up {item.name}',
                    act=partial(pickup, item=item)
                )

            self.current_situation = Situation(desc=string, choices=choices)
            cancel = Action(key='c', desc="Don't touch anything.",
                            act=self.clear_situation)
            self.current_situation.add_choice(cancel)

    def clear_situation(self):
        self.current_situation = None

    def situation(self):
        if not self.current_situation:
            loc = self.loc
            desc = f'Location: {loc.name}\n{loc.desc}'

            situation = Situation(desc=desc)

            choices = [('n', 'north'), ('e', 'east'),
                       ('s', 'south'), ('w', 'west')]

            for key, dir in choices:
                room = getattr(loc, dir)
                if room:
                    desc = f'Move {dir} to {room.name}'
                    act = partial(self.move, dir)
                    situation.add_choice(Action(key=key, act=act, desc=desc))

            look = Action(key='l', desc='Look around', act=self.look)
            situation.add_choice(look)
            return situation
        else:
            return self.current_situation


class Situation:
    def __init__(self, desc='', choices={}):
        self.desc = desc
        self.choices = OrderedDict(choices)

    def add_choice(self, choice):
        if not isinstance(choice, Action):
            raise Exception('That is not an Action')
        else:
            self.choices[choice.key] = choice

    def announce(self):
        str = ''
        str += self.desc + '\n'
        str += 'Choices:\n'

        for key, choice in self.choices.items():
            str += (f'{key}: {choice.desc}\n')

        return str
