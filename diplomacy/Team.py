class Team:
    '''Class for each Team in the diplomacy game.
    
    Each Team can be assigned multiple players, will have a team name, and will have units and held territories.
    '''

    def __init__(self, id, players, name, territories):
        '''Initialisation of Team object.
        
        INPUTS:
            id [int]: ID given by the game to the team, for use in tracking territories

            players [dictionary name:discriminator]: dictionary of player IDs for the team
            
            name [string]: team name to be displayed.

            territories [dictionary tile_index:unit]: dictionary of which territories are held by the Team, and what units are in each territory.
                + 00: no units, but last to hold the territory
                + 01: land unit
                + 10: sea unit
        '''
        self.id = id
        self.players = players
        self.name = name
        self.territories = territories


    def check_territories_valid(self, map):
        '''Method to check the validity of the Team territories against a Map.occupation dictionary.
        
        INPUTS:
            map [Map object]: the Map object against which to check the validity of the Team knowledge of pieces.
        '''
        # from map, extract a territories dictionary in the self.territories format.
        map_territories = {k:v[1] for k,v in map.occupation.items() if v[0] == self.id}
        if self.territories == map_territories:
            return True
        else:
            return False


    def update_territories_from_map(self, map):
        '''Method to extract the territories from a Map.occupation dictionary for the given Team.id
        
        INPUTS:
            map [Map object]: Map object to extract the territories from.
        '''
        map_territories = {k:v[1] for k,v in map.occupation.items() if v[0] == self.id}
        self.territories == map_territories


    def update_map_from_territories(self, map):
        '''Method to update the Map.occupation dictionary from the Team.territories dictionary.
        
        INPUTS:
            map [Map object]: Map object to be updated'''

        for k,v in self.territories.items():
            map.occupation[k] = [self.id,v]

        