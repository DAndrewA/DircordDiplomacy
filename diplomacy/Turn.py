class Turn:
    '''Class for each Turn in the diplomacy game.
    Each Turn will have an initial Map state, anda list of Orders submitted by each Team.
    The Turn will allow for Orders to be resolved. This will result in a minimum instruction set for how to evolve the state of the Map from its initial state to the next Turn.
    
    I might also write the functionality to generate a narrative from the Orders, such that things like bounces, convoys, etc, can be displayed to the players in a fun and engaging format.
    '''

    def __init__(self, year, season):
        pass