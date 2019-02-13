from room import Room
from player import Player
from action import Action
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons",
                     [Item('rock'), Item('healing potion')]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across theuchasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
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
    # get current situation for player
    situation = player.situation()
    # add quite choice to situation's choices
    situation.add_choice(quit)

    # get description of current situation
    print(situation.announce())
    selection = input('>> ')
    try:
        # use input to attempt to access an Action from situation's
        # choices
        choice = situation.choices[selection]
    except:
        print(f'Chose {selection}. That is not a valid selection')
    else:
        # if valid action found, undertake action
        result = choice.act()
        if result:
            print(result)
            print('\n\n')
