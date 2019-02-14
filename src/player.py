from functools import partial

from collections import OrderedDict
from action import Action

from item import Item, LightSource
# Write a class to hold player information, e.g. what room they are in
# currently.

# helper func to grab first item matching predicate from iterable


def pick(predicate, content):
    eligible = [thing for thing in content if predicate(thing)]
    return eligible[0] if eligible else None


class Player:
    def __init__(self, name, loc, **kwargs):
        self.name = name
        self.loc = loc
        self.current_state = None
        self.inventory = []
        self.max_hp = kwargs.get('max_hp') or 10
        self.hp = self.max_hp

    def move(self, dir):
        target = getattr(self.loc, dir)
        if target:
            self.loc = target
            return f'You moved into {self.loc.name}...'
        else:
            return False

    def take(self, item):
        if not self.sufficient_light():
            self.clear_state()
            return 'It is too dark to find anything.'
        if isinstance(item, str):
            found_item = pick(lambda x: x.name == item, self.loc.contents)
            if not found_item:
                return f'{item} is not something you can pick up here.'
            else:
                item = found_item
        if not isinstance(item, Item):
            raise Exception('Can only take items')
        self.inventory.append(item)
        self.loc.contents.remove(item)
        return f'Picked up {item.name}'

    def use_up(self, item):
        self.inventory.remove(item)
        if item.original_life != 1:
            return f'You used up {item.name}'

    def drop(self, item):
        if isinstance(item, str):
            found_item = pick(lambda x: x.name == item, self.inventory)
            if not found_item:
                return f'{item} is not something you can drop'
            else:
                item = found_item
        if not isinstance(item, Item):
            raise Exception('Can only drop items')
        self.inventory.remove(item)
        self.loc.contents.append(item)
        string = f'You dropped {item.name}'
        result = item.on_drop()
        if isinstance(result, str):
            string += '\n' + result
        return string

    def look(self):
        if not self.sufficient_light():
            self.clear_state()
            return 'It is too dark to look around'
        contents = self.loc.contents
        if not contents:
            self.clear_state()
            return 'You do not see anything of interest.\n'
        else:
            # generates specific pickup actions for different items, gets
            # bound in loop below
            def pickup(item):
                result = self.take(item) + '\n'
                return result

            string = 'Looking around, you notice the following: \n'
            choices = OrderedDict()
            # loop creates a return Action for each item around, adds these items
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
            situation = Situation(desc=string, choices=choices)
            cancel = Action(key='c', desc="Don't touch anything.",
                            act=self.clear_state)
            situation.add_choice(cancel)
            return situation

    def use(self, item):
        if isinstance(item, str):
            found_item = pick(lambda x: x.name == item, self.inventory)
            if not found_item:
                return f'{item} is not something you can use.'
            else:
                item = found_item
        if not isinstance(item, Item):
            raise Exception('Can only use items')

        result = item.use(self) + '\n'
        return result

    def check_inventory(self):
        inventory = self.inventory
        if not inventory:
            string = "Your inventory is empty."
            self.clear_state()
            return string
        else:
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
                    act=partial(self.use, item=item)
                )

            # Adds cancellation of 'look' situation to return to generic staet
            situation = Situation(desc=string, choices=choices)

            cancel = Action(key='c', desc="Close pack.",
                            act=self.clear_state)
            situation.add_choice(cancel)
            return situation

    def sufficient_light(self):
        return bool(self.loc.is_light or pick(
            lambda x: isinstance(x, LightSource), self.inventory)
        )

    def clear_state(self):
        # clears out any special situation the Player might be in
        self.current_state = None

    def render(self):
        # checks to see if the player is in a special situation needing to
        # be resolved
        if self.current_state:
            return self.current_state()
        # otherwise returns the basic survey the area state
        else:
            loc = self.loc
            if self.sufficient_light():
                desc = f'Location: {loc.name}\n{loc.desc}'
            else:
                desc = f"Location: {loc.name}\nIt's pitch black."

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

            look = Action(key='l', desc='Look around',
                          act=lambda: self.update_state('look'))
            situation.add_choice(look)

            check_inventory = Action(
                key='i',
                desc="Check inventory",
                act=lambda: self.update_state('check_inventory'))
            situation.add_choice(check_inventory)
            return situation

    # updates player into special states (which are themselves functions
    # that return Situations to adv.py)
    def update_state(self, transition):
        self.current_state = getattr(self, transition, lambda x: None)
        return self.current_state()


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
        str += self.desc + '\n\n'
        str += 'Choices:\n'

        for key in self.choices:

            str += '     ' + self.choices[key].announce()

        return str
