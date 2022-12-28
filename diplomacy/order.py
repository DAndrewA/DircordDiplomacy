import Map

class Order:
    '''Class for each Order given by a Team in a Turn of the diplomacy game.
    
    The Order will consist of a verb, an initial target, and if required, an adverb (i.e. final location, route of convoying, etc, supporting, etc).
    The Order class will also contain methods to validate orders:
    
    validate_1: this will be a first order validation, that the written message can be parsed into the target:verb:adverb format.
    validate_2: this will be a second order validation, that checks if the Order is valid within the rules of the game. That is, players will not be able to Order units that they do not have, or make illegal moves, etc.
    '''

    def __init_(self,message,team):
        '''Initialisation of the Order object
        
        INPUTS:
            message [str]: message to be formatted into the target:verb:adverb format.
            
            team [Team object]: the Team to which the Order belongs.
        
        RETURNS:
            self.error: None: no error in the validation
                        str: a string explaining the first error found in the validation.
        '''

        self.message = message.lower()
        self.Team = team

        self.parsed, self.error = validate_1(self)


def validate_1(order, map):
    '''A function to validate if the Order can be parsed into the target:verb:adverb format.

    Possible verbs are:
    hold: a unit on a given space holds its position. Needs no adverb.
        "h", "hold", "holds"
    move: a unit on a given space moves to another location. Takes adverbs.
        One adverb -- move to an allowed adjacent location
        Multiple adverbs -- a sequence of adjacent locations for the unit to be convoyed through (in order)
        "m", "move", "moves"
    support: a unit supports a move to an adjacent tile by another unit. Takes two adverbs.
        First adverb -- the intial location of the unit being supported
        Second adverb -- the location the supporting unit is moving to
        "s", "support", "supports"
    convoy: a sea unit helps convoy a unit of given origin; only origin is required as an adverb as this allows other players convoying to be taken advantage of...
        One adverb -- origin of unit being convoyed
        "c", "convoy", "convoys"

    
    INPUT:
        order [Order object]: the Order to be parsed into the format.

        map [Map object]: the Map object that targets should point to

    RETURNS:
        parsed [list]: list containing the Order in a succesfully parsed format. If the validation fails, then is None. Otherwise, the format is [verb, intial, adverbs...]

        error [string]: if the parsing fails, then contains a string denoting the first found error. Otherwise, is None.
    '''
    parsed = []
    order_txt = order.message
    order_txt = [txt.strip() for txt in order_txt.split(':')] # splits the order message by ':' chars and removes trailing and leading whitespace from each element.
    if len(order_txt) == 1: # if there are no ':' chars in the order message
        parsed = []
        error = "':' character not used in command"
        return parsed, error

    adverbs = None
    # checking if a valid verb has been given
    verb = order_txt[1] # extract the verb, which is the second element in the order
    if verb in ['h','hold','holds']:
        num_adverb = 0
        adverbs = [order_txt[0]] # in the hold case, the only target is the first element of the order
    elif verb in ['s','support','supports']:
        num_adverb = 2
    elif verb in ['c','convoy','convoys']:
        num_adverb = 1
    elif verb in ['m','move', 'moves', 'moves to']:
        num_adverb = len(order_txt) - 2
        if num_adverb == 0: # if the miniumum number of adverbs for a move is not given, an error has occured
            parsed = []
            error = 'No adverbs given for move order'
            return parsed, error
    else:
        parsed = []
        error = f'Verb "{verb}" not recognised.'
        return parsed, error

    parsed.append(verb[0]) # the first element of the parsed instruction is the verb

    # check if the number of adverbs given matches the number of adverbs required.
    if len(order_txt) != num_adverb + 2:
        parsed = []
        error = f'Number of adverbs given is {len(order_txt)-2}, {num_adverb} expected.'

    # generate a list of the targets/adverbs and ensure all are valid targets
    if adverbs is None:
        adverbs = [order_txt[0], *order_txt[2:]]
    
    for target in adverbs:
        target_id = map.find_tile_id_from_target(target)
        if target_id is None:
            parsed = []
            error = f'Target "{target}" not found in Map.abbrvs'
            return parsed, error
        parsed.append(target_id)

    # once this has been done, we can return the validated parsed order.
    return parsed, None
        

def validate_2(order, map):
    '''Function to check the validity of a parsed order according to the rules of the game.
    
    INPUTS:
        order [Order object]: the order to be validated against the game rules. It should already have passed the validate_1 function.

    RETURNS:
        error [string]: if not None then an error has occured and it should describe the error thats ocurred.
        warning [string]: if not None, a string that includes possible issues to do with the order (i.e. convvoying another Team's unit)
    '''
    error = None
    warning = None

    parsed = order.parsed
    team_id = order.Team.id

    # check that the initial location is one with a unit belonging to the Team on it.
    initial = parsed[1]
    initial_info = map.get_info_from_tile_id(initial)
    if initial_info[0] != team_id: # the team_id of the ordered unit/tile doesn't match the team giving the order
        error = f'Team {order.Team.name} cannot make order for tile {initial}: doesn\'t belong to Team.'
        return error, warning
    if initial_info[1] == 0: # in this case, there is no unit on the tile to be ordered.
        error = f'Order on tile {initial} invalid, unit code is {initial_info[1]} (not unit).'
        return error, warning

    if parsed[0] == 'h':
        # if a hold order is given and the initial is valid, then the order is valid
        return None, None # the return for a valid order
    elif parsed[0] == 's':
        # a support order is given to support a unit moving from one tile into a tile thats adjacent to both the moving and supporting unit.
        supported = parsed[2]
        target_location = parsed[3]
        # we need to check that 1) intial is adjacent to the target_location; 2) supported is adjacent to the target_location (or are the same); 3) if target != supported, then they do not have units that belong to the same team (self-attack).
        adj = map.adjacency_matrix[initial][target_location]
        if not adj:
            error = f'Initial tile {initial} and target location {target_location} aren\'t adjacent.'
            return error, warning

        if supported == target_location: # in this instance we are supporting a hold
            # check that there is infact a unit on the tile
            info = map.get_info_from_tile_id(supported)
            if info[1] == 0:
                # if there's no unit on the tile, this is an invalid order
                error = f'No unit on target tile {supported} for hold to work with'


def check_valid_support(order,map):
    '''Function to determine if a support order is valid.

    A parsed support order looks like ['s', initial, supported, target_location]
    For a support order to be valid, it must satisfy the conditions:
    1) initial and target_location are adjacent
    2) supported and target_location are adjacent
    3) that there's a unit on supported to support
    4) supported -> target_location is a valid movement (i.e. no tanks on water)
    5) if supported != target_location, then supported isn't attacking one of its own units

    INPUTS:
        order [Order object]: The order object that is being validated.
        
        map [Map object]: the Map on which the game is being played.

    RETURNS:
        error [string]: None if no errors, a string explaining any problems if there is an issue.
        
        warning [ string]: a string explaining any considerations that may need to be made about a given order.
    '''
    error = None
    warning = None
    parsed = order.parsed
    initial = parsed[1]
    supported = parsed[2]
    target_location = parsed[3]
    # 1) check the adjacency of intial and target_location
    adj = map.adjacency_matrix[initial][target_location]
    if not adj:
        error = f'Initial tile {initial} can\'t support on tile {target_location}: not adjacent.'
        return error, warning
    # 2) check the adjacency of supported and target_location
    adj = map.adjacency_matrix[supported][target_location]
    if not adj:
        error = f'Supported tile {supported} can\'t be suppported on tile {target_location}: not adjacent.'
        return error, warning
    # 3) check there's a unit on supported to be supported
    supported_info = map.get_info_from_tile_id(supported)
    if not supported_info[1]:
        error = f'Supported tile {supported} has no unit: {supported_info=}'
        return error, warning
    # 4) check supported -> target_location is a valid move
    target_location_info = map.get_info_from_tile_id(target_location)
    supported_type = map.adjacency_matrix[supported][supported]
    target_location_type = map.adjacency_matrix[target_location][target_location]
    unit_type = supported_info[1]
    # the units in binary are land: 01; water: 10. Bitwise and with the type should be non-zero if movement is allowed
    if not((unit_type&supported_type) and (unit_type&target_location_type)):
        list_units = ['None', 'LAND', 'SEA']
        list_tiles = ['None', 'LAND', 'SEA', 'COASTAL']
        error = f'Trying to support a {list_units[unit_type]} unit moving from a {list_tiles[supported]} tile to a {list_tiles[target_location]} tile.'
        return error, warning
    # 5) if supported != target_location then we aren't supporting an attack on a team's own units
    id = supported_info[0]
    if (supported != target_location) and (id == target_location_info[0]):
        error = f'Trying to support a self attack by Team.{id=}: invalid.'
        return error, warning
    # if we have got to here, the support order is valid. The only warnings should be if we are supporting an enemy unit.
    if id != map.get_info_from_tile_id(initial)[0]:
        warning = f'Supporting move by another Team; Team.{id=}; {supported}: m: {target_location}.'
    return error, warning


def check_valid_convoy(order,map):
    '''Function to determine if a convoy order is valid.
    
    A parsed convoy order looks like ['c', initial, target]
    Here, initial is the unit being ordered to help in the convoy, and target is the unit being convoyed.
    For a convoy order to be valid, it must satisfy:
    1) initial must be a sea tile (the existence of a sea unit is already accounted for).
    2) target must be a coastal tile.
    3) target must contain a land unit. If it belongs to another team, then this will throw a warning
    
    INPUTS:
        order [Order object]: The order object that is being validated.
        
        map [Map object]: the Map on which the game is being played.

    RETURNS:
        error [string]: None if no errors, a string explaining any problems if there is an issue.
        
        warning [ string]: a string explaining any considerations that may need to be made about a given order.
    '''
    error = None
    warning = None
    
    initial = order.parsed[1]
    target = order.parsed[2]
    # 1) checking that the initial tile is a SEA tile
    list_tiles = ['None', 'LAND', 'SEA', 'COASTAL']
    initial_type = map.adjacency_matrix[initial][initial]
    if initial_type != 2:
        error = f'Convoy: initial tile must be SEA, is {list_tiles[initial_type]}.'
        return error, warning
    # 2) target must be a coastal tile
    target_type = map.adjacency_matrix[target][target]
    if target_type != 3:
        error = f'Convoy: target tile must be COASTAL, is {list_tiles[target_type]}.'
        return error, warning
    # 3) check target contains a land unit
    target_info = map.get_info_from_tile_id(target)
    if target_info[1] != 1:
        list_units = ['None', 'LAND', 'SEA']
        error = f'Convoy: target unit must be LAND, is a {list_units[target_info[1]]}-unit.'
        return error, warning
    # otherwise, convoy is valid, check if for another team:
    if order.Team.id != target_info[0]:
        warning = f'Convoy warning: Order by Team.id={order.Team.id} to convoy unit from Team.id={target_info[0]}.'
    return error, warning


def check_valid_move(order,map):
    '''Function to determine the validity of a Move Order.
    
    A parsed move order can take two forms:
        a) ['m', initial, target]
        b) ['m', initial, convoy_1, ..., convoy_n, target]
        
    For a move order to be valid:
    a)  1) initial and target have an adjacency that allows movement of the unit on initial.
        2) there isn't a friendly unit on target (no self-attacking).
    
    b)  1) intial and target are both coastal tiles
        2) the unit on initial is a land unit
        3) there isn't a friendly unit on target (no self-attacking)
        4) For each consecutive pair of indices, they are adjacent so a convoy can be made
        5) SEA units exist on each tile in the convoy that is a SEA tile

    INPUTS:
        order [Order object]: The order object that is being validated.
        
        map [Map object]: the Map on which the game is being played.

    RETURNS:
        error [string]: None if no errors, a string explaining any problems if there is an issue.
        
        warning [ string]: a string explaining any considerations that may need to be made about a given order.    
    '''
    error = None
    warning = None
    
    parsed = order.parsed
    initial = parsed[1]
    target = parsed[-1]
    initial_info = map.get_info_from_tile_id(initial)
    target_info = map.get_info_from_tile_id(target)
    unit = initial_info[0]
    
    list_units = ['None', 'LAND', 'SEA']
    list_tiles = ['None', 'LAND', 'SEA', 'COASTAL']

    # first, determine the type of move order being given, a or b:
    if len(parsed) == 3: # type (a)
        target = parsed[2]
        # a1) initial and target have the right adjacency for the unit
        adj = map.adjacency_matrix[initial][parsed]
        if not (unit & adj): # bitwise operation as seen in check_valid_support
            error = f'Move: {list_units[unit]} unit cannot move along {list_tiles[adj]} adjacency.'
            return error, warning
        # a2) there isn't a friendly unit on target
        if (target_info[0] == order.Team.id) and target_info[1]:
            error = f'Move: cannot move into a tile where a friendly unit already exists (self-attacking).'
            return error, warning
        # otherwise, the move is valid, return None and None
        return None, None
    # type (b): in this case, convoy orders have hopefully been issued.
    convoy = parsed[1:] # initially include initial and target in the convoy List for checking adjacency.
    # b1) both initial and target are coastal tiles
    initial_type = map.adjacency_matrix[initial][initial]
    target_type = map.adjacency_matrix[target][target]
    if initial_type != 3:
        error = f'Move - convoy: Initial tile {initial} is of type {list_tiles[initial_type]}, not COASTAL.'
        return error,warning
    if target_type != 3:
        error = f'Move - convoy: Target tile {target} is of type {list_tiles[target_type]}, not COASTAL.'
        return error, warning
    # b2) check the unit on initial is a land unit
    if unit != 1:
        error = f'Move - convoy: Unit on initial tile {initial} is of type {list_units[unit]}, not LAND.'
        return error, warning
    # b3) check no self-attacking
    if (order.Team.id == target_info[0]) and target_info[1]:
        error = f'Move - convoy: Friendly unit on target tile: no self-attacking.'
        return error, warning
    # b4) for each adjacent pair of indices, check they are ocean-adjacent (i.e. adj&2)
    for i,c2 in convoy[1:]: # this way, i refers to the value before c2 in convoy
        c1 = convoy[i]
        adj = map.adjacency_matrix[c1][c2]
        if not adj&2: # if not ocean-adjacent
            error = f'Move - convoy: Adjacency ({i=}) between {c1} and {c2} is of type {list_tiles[adj]}, not OCEANIC.'
            return error, warning
    # b5) SEA units exist on each part of the convoy
    convoy = parsed[2:-1]
    for c in convoy:
        c_info = map.get_info_from_tile_id(c)
        if c_info[1] != 2:
            error = f'Move - convoy: unit on {c} is of type {list_units[c_info[1]]}, not SEA.'
            return error, warning
        if c_info[0] != order.Team.id:
            if warning is None:
                warning = 'Move - convoy: warning: '
            warning += f'unit on tile {c} belongs to Team.id={c_info[0]}; '
    # all checks have been made!
    return error, warning



