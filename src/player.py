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

    def use_up(self, item):
        self.inventory.remove(item)
        if item.original_life != 1:
            return f'You used up {item.name}'

    def look(self):
        contents = self.loc.contents
        if not contents:
            string = "You don't see anything of interest."
            self.clear_situation()
            return string
        else:
            # generates specific pickup actions for different items, gets
            # bound in loop below
            def pickup(item):
                result = self.take(item) + '\n'
                result += self.look() or ''
                return result

            string = 'Looking around, you notice the following: \n'
            choices = OrderedDict()
            # loop creates a Action for each item around, adds these items
            # to a Situation, and sets Players current state to that situation
            for index, item in enumerate(contents):
                num = str(index + 1)
                string += ' ' * 10
                string += f'{num}. {item.desc}\n'
                choices[num] = Action(
                    key=num,
                    desc=f'pick up {item.name}',
                    act=partial(pickup, item=item)
                )

            # Adds cancellation of 'look' situation to return to generic staet
            self.current_situation = Situation(desc=string, choices=choices)
            cancel = Action(key='c', desc="Don't touch anything.",
                            act=self.clear_situation)
            self.current_situation.add_choice(cancel)

    def check_inventory(self):
        inventory = self.inventory
        if not inventory:
            string = "Your pack is empty."
            self.clear_situation()
            return string
        else:
            # generates specific use actions for different items, gets
            # bound in loop below
            def use(item):
                result = item.use(self) + '\n'
                result += self.check_inventory() or ''
                return result

            string = 'Checking your pack, you find: \n'
            choices = OrderedDict()
            # loop creates a Action for each item around, adds these items
            # to a Situation, and sets Players current state to that situation
            for index, item in enumerate(inventory):
                num = str(index + 1)
                string += ' ' * 10
                string += f'{num}. {item.desc}\n'
                choices[num] = Action(
                    key=num,
                    desc=f'{item.verb} {item.name}',
                    act=partial(use, item=item)
                )

            # Adds cancellation of 'look' situation to return to generic staet
            self.current_situation = Situation(desc=string, choices=choices)
            cancel = Action(key='c', desc="Close pack.",
                            act=self.clear_situation)
            self.current_situation.add_choice(cancel)

    def clear_situation(self):
        # clears out any special situation the Player might be in
        self.current_situation = None

    def situation(self):
        # checks to see if the player is in a special situation needing to
        # be resolved
        if not self.current_situation:
            loc = self.loc
            desc = f'Location: {loc.name}\n{loc.desc}'

            situation = Situation(desc=desc)

            choices = [('n', 'north'), ('e', 'east'),
                       ('s', 'south'), ('w', 'west')]

            # builds up a set of movement Actions for each direction
            for key, dir in choices:
                room = getattr(loc, dir)
                if room:
                    desc = f'Move {dir} to {room.name}'
                    act = partial(self.move, dir)
                    situation.add_choice(Action(key=key, act=act, desc=desc))

            look = Action(key='l', desc='Look around', act=self.look)
            situation.add_choice(look)

            check_inventory = Action(
                key='p', desc="Check pack", act=self.check_inventory)
            situation.add_choice(check_inventory)
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
        # the announce method is used by the adv.py to describe the situation
        str = ''
        str += self.desc + '\n'
        str += 'Choices:\n'

        for key, choice in self.choices.items():
            str += (f'{key}: {choice.desc}\n')

        return str
