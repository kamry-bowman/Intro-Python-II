from functools import partial

from room import Room
from player import Player
from action import Action
from item import Item, LightSource

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons",
                     [
                         Item(name='rock', verb='throw', verb_past='threw'),
                         Item('healing potion')
                     ]
                     ),
    'foyer':    Room("Foyer",
                     """Dim light filters in from the south. Dusty passages run
                      north and east.""",
                     contents=[
                         LightSource(
                             'torch',
                             verb='brandish',
                             verb_past='brandished',
                             life=-1)
                     ]
                     ),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room(
        "Narrow Passage",
        """The narrow passage bends here from west to north. The smell of gold permeates the air.""",
        is_light=False
    ),

    'treasure': Room(
        "Treasure Chamber",
        """You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""",
        is_light=False)
}


# Link rooms together

room['outside'].north = room['foyer']
room['foyer'].south = room['outside']
room['foyer'].north = room['overlook']
room['foyer'].east = room['narrow']
room['overlook'].south = room['foyer']
room['narrow'].west = room['foyer']
room['narrow'].north = room['treasure']
room['treasure'].south = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player(name='John', loc=room['outside'])
# Write a loop that:
game_on = True


def end_game():
    global game_on
    game_on = False
    return 'Game ended. Goodbye'


quit = Action(key='q', desc='End game', act=end_game)

while game_on:
    # get current play state for player
    situation = player.render()
    # some situations are events that immediately resolve. These
    # are strings and can be immediately printed.
    if isinstance(situation, str):
        print(situation)
    else:
        # add take <item> choice
        take_specific = Action(key='take', target_string='item',
                               desc='Pick up <item>', act=player.take)
        situation.add_choice(take_specific)
        # add use <item> choice
        use_specific = Action(key='use', target_string='item',
                              desc='Use <item>', act=player.use)
        situation.add_choice(use_specific)
        # add drop <item> choice
        drop = Action(key='drop', target_string='item',
                      desc='Drop <item>', act=player.drop)
        situation.add_choice(drop)
        # add quit choice to player's choices
        situation.add_choice(quit)

        # get description of current state
        print(situation.announce())
        user_input = input('>> ').split(' ', 1)
        selection = user_input[0]
        argument = user_input[1] if len(user_input) > 1 else None

        try:
            # use input to attempt to access an Action from situation's
            # choices
            choice = situation.choices[selection]
        except:
            print(f'Chose {selection}. That is not a valid selection')
        else:
            # if valid action found, undertake action
            # check is the action requires two words, and handle appropriately
            if choice.target_string:
                if argument:
                    result = choice.act(argument)
                else:
                    result = f'{choice.desc} requires a target!'
            else:
                result = choice.act()
            if result and isinstance(result, str):
                print(result + '\n\n')
