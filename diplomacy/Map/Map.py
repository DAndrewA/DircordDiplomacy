class Map:
    '''Class for the boardgame map.
    
    This class will store information on the adjacency of the map tiles, map tile types, display names for the tiles, etc.
    '''

    def __init__(self, tile_names, supply_centres, adjacency_matrix, occupation={}, abbreviations=None, polygons=None):
        '''Initialisation function for the Map class.
        
        INPUTS:
            tile_names [list of str](m): list of strings for the display names for the tiles
            
            supply_centres [list of bool](m): list of booleans determining which tiles are supply centres
            
            adjacency_matrix [mxm matrix]: matrix of how tiles are connected to each other. First index (row) is the initial tile, second index (column) is the final tile. This allows for directed transport. For undirected graphs, should be symmetric. Diagonal determines the tile-type:
                + 00: no adjacency
                + 01: land adjacency (or land tile)
                + 10: ocean adjacency (or ocean tile)
                + 11: land and ocean adjacency (coastal tile)

            occupation [dictionary tile_index:[Team.id, unit] ]: disctionary of lists for the Team.id and unit for a given tile_index

            abbreviations [dictionary 'abrv':tile-index]: allows different abbreviations to be used when giving commands for tiles

            polygons [list of polygons]: allows for lists of polygon corners to be given. These will allow displays of the maps to be given more easily.
        '''
        self.tile_names = tile_names
        self.num_tiles = len(tile_names)
        self.supply_centres = supply_centres
        self.adjacency_matrix = adjacency_matrix
        self.occupation = occupation
        self.abbrv = abbreviations
        self.polygons = polygons

        # if no abbreviations are given, turn the tile_names into the abbreviation dictionary.
        if self.abbrv is None:
            self.abbrv = {n:i for i,n in enumerate(tile_names)}

    
    def find_tile_id_from_target(self, target):
        '''Method to return a valid tile_id for a given target string.
        This will be achieved by searching the Map.abbrv dictionary
        
        INPUTS:
            target [string]: string that is the target for the tiles

        RETURNS:
            target_id [int]: the id of the tile the target refers to. None if not valid target.
        '''
        try:
            target_id = self.abbrv[target]
        except:
            target_id = None
        return target_id


    def get_info_from_tile_id(self,tile_id):
        '''Method to get the team_id of a unit on a tile given by tile_id.
        
        INPUTS:
            tile_id [int]: the id of the tile to be checked.
            
        RETURNS:
            info [list [int, int] ]: list identifying Team.id and unit on tile
        '''
        try:
            info = self.occupation[tile_id]
        except:
            info = [0,0] # no team, no unit
        return info

