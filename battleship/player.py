import random

from battleship.board import Board
from battleship.convert import CellConverter
from battleship.ship import Ship

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        if board is None:
            self.board = Board()
        else:
            self.board = board
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name
    
    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a subclass to do something useful, for example to record a successful or failed attack.
        
        Returns:
            None
        """
        return None
    
    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))
        
    def select_target(self):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        
        # TODO: Add any other attributes necessary for your strategic player
        # Create set of cells that it doesn't make sense to attack
        self.do_not_attack_set = set()

        # Remember result of last hit
        self.was_last_hit = False
        self.was_last_sunk = False

        # Create a set of hit cells so far
        self.hit_so_far = set()

        # Create set of sunk ships so far
        self.sunk_ships = []

        # Remember last attacked cell
        self.last_attacked_cell = None

        # Create set of all cells in the board
        self.all_board_cells = set()
        x_list = list(range(1, self.board.width+1))
        y_list = list(range(1, self.board.height+1))
        for i in x_list:
            for j in y_list:
                self.all_board_cells.add((i,j))
        
        
    def select_target(self):
        """ Select target coordinates to attack.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        # TODO: Complete this method
        if self.was_last_hit:
            
            (x_coord, y_coord) = self.last_attacked_cell
            horizontal_neighbours = [(min(x_coord + 1, self.board.width), y_coord), (max(x_coord - 1, 1), y_coord)]
            vertical_neighbours = [(x_coord, min(y_coord + 1, self.board.height)), (x_coord, max(y_coord - 1, 1))]
            neighbours = set(horizontal_neighbours + vertical_neighbours)
            print(f"Last was a hit, the neighbours are: {neighbours}")
            already_attacked = True
            for target_cell in neighbours:
                already_attacked = target_cell in self.do_not_attack_set
                if not already_attacked:
                    # Remember the cell that you are about to attack
                    self.do_not_attack_set.add(target_cell)
                    self.last_attacked_cell = target_cell
                    return target_cell
        
        # If last was not a hit or all neighbours were already attacked
        # Generate random target
        target_cell = self.generate_random_target()

        # Remember the cell that you are about to attack
        self.do_not_attack_set.add(target_cell)
        self.last_attacked_cell = target_cell

        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that is not in
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        pointless_to_attack = True
        random_cell = None
        
        while pointless_to_attack:
            random_cell = self.get_random_coordinates()
            pointless_to_attack = random_cell in self.do_not_attack_set

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method records the outcome of the latest attack in the player attributes.
        
        Returns:
            None
        """

        # Add last attacked cell to set of hit cells
        self.was_last_hit = False
        if is_ship_hit:
            self.hit_so_far.add(self.last_attacked_cell)
            self.was_last_hit = True
            

        # If ship sunk add it to the set of sunk ships
        self.was_last_sunk = False
        if has_ship_sunk:
            self.was_last_sunk = True
            # print(f"Last attacked cell: {self.last_attacked_cell} of type {type(self.last_attacked_cell)}")
            # Intialize set that contains all of the cells belonging to the sunk ship
            ship_cells = set()
            ship_cells.add(self.last_attacked_cell)
            # print(f"Ship cells: {ship_cells} of type {type(ship_cells)}")
            checked_cells = set()

            # print(f"Hit so far: {self.hit_so_far} of type {type(self.hit_so_far)}")

            # Find all cells that belong to the sunk ship
            while ship_cells != checked_cells:
                # Take a snapshot of the current ship cells to iterate over it
                current_ship_cells = ship_cells.copy()
                # print(f"Ship cells: {ship_cells} of type {type(ship_cells)}")
                # print(f"Checked cells: {checked_cells} of type {type(checked_cells)}")
                for current_cell in current_ship_cells:
                    # Find adjacent previously hit cells of the current cell
                    if current_cell not in checked_cells:
                        # Find previously hit cells adjacent to current cell
                        for cell in self.hit_so_far:
                            is_adjacent_in_x = abs(current_cell[0] - cell[0]) == 1 and current_cell[1] == cell[1]
                            is_adjacent_in_y = abs(current_cell[1] - cell[1]) == 1 and current_cell[0] == cell[0]
                            is_adjacent = is_adjacent_in_x or is_adjacent_in_y
                            if is_adjacent:
                                ship_cells.add(cell)
                        # Do not check the same cell again
                        checked_cells.add(current_cell)

            # Create ship from ship cells
            sunk_ship = self.create_ship_from_cells(ship_cells)

            print(f"Sunk_ship: {sunk_ship}")

            # print(f"Do not attack set before update: {self.do_not_attack_set}")

            # Add all cells that are near sunk ship to do_not_attack_set
            self.do_not_attack_neighbours(sunk_ship)
            
            # print(f"Do not attack set after update: {self.do_not_attack_set}")
            
        return None

    def create_ship_from_cells(self, ship_cells):
        """Create a ship instance from a set of cells.

        Args:
            ship_cells (set[tuple]): All cells belonging to a ship.
            
        Returns:
            Ship: A ship instance made of the input ship cells.
        """

        # Separate set of cells into x and y coordinates
        unzipped_coords = list(zip(*ship_cells))
        x_coords = unzipped_coords[0]
        y_coords = unzipped_coords[1]

        # Find the start and end cells for the Ship constructor
        start_x = min(x_coords)
        start_y = min(y_coords)
        end_x = max(x_coords)
        end_y = max(y_coords)
        start = (start_x, start_y)
        end = (end_x, end_y)

        ship = Ship(start, end)

        return ship

    def do_not_attack_neighbours(self, sunk_ship):
        """Add cells near to a sunk ship to the do not attack set.

        Args:
            sunk_ship (Ship): Sunk ship.
            
        Returns:
            None
        """
        for cell in self.all_board_cells:
            if sunk_ship.is_near_cell(cell):
                self.do_not_attack_set.add(cell)
                # print(f"Added {cell} to do not attack set")