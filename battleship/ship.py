import random, time

from battleship.convert import CellConverter

class Ship:
    """ Represent a ship that is placed on the board.
    """
    def __init__(self, start, end):
        """ Creates a ship given its start and end coordinates on the board. 
        
        The order of the cells do not matter.

        Args:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
                where the first number is the horizontal coordinate x
                that is represented as a letter on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board

        Raises:
            ValueError: if the ship is neither horizontal nor vertical
        """
        # Start and end (x, y) cell coordinates of the ship
        self.x_start, self.y_start = start
        self.x_end, self.y_end = end

        # Make x_start on left and x_end on right
        self.x_start, self.x_end = min(self.x_start, self.x_end), max(self.x_start, self.x_end)
        
        # Make y_start on top and y_end on bottom
        self.y_start, self.y_end = min(self.y_start, self.y_end), max(self.y_start, self.y_end)

        if not self.is_horizontal() and not self.is_vertical():
            raise ValueError("The given coordinates are invalid. "
                "The ship needs to be either horizontal or vertical.")
        
        # Make sure coords are positive
        if not self.x_start > 0 or not self.y_start > 0:
            raise ValueError("The given coordinates are invalid. "
                "Coordinates must be positive.")

        # Set of all (x,y) cell coordinates that the ship occupies
        self.cells = self.get_cells()
        
        # Set of (x,y) cell coordinates of the ship that have been damaged
        self.damaged_cells = set()
    
    def __len__(self):
        return self.length()
        
    def __repr__(self):
        return f"Ship(start=({self.x_start},{self.y_start}), end=({self.x_end},{self.y_end}))"
        
    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """
     
        if self.x_start == self.x_end:
            return True
        return False
   
    def is_horizontal(self):
        """ Check whether the ship is horizontal.
        
        Returns:
            bool : True if the ship is horizontal. False otherwise.
        """
   
        if self.y_start == self.y_end:
            return True
        return False
    
    def get_cells(self):
        """ Get the set of all cell coordinates that the ship occupies.
        
        For example, if the start cell is (3, 3) and end cell is (5, 3),
        then the method should return {(3, 3), (4, 3), (5, 3)}.
        
        This method is used in __init__() to initialise self.cells
        
        Returns:
            set[tuple] : Set of (x ,y) coordinates of all cells a ship occupies
        """

        # If horizontal, generate cells horizontally, if vertical, vertically
        if self.is_horizontal():
            # Generate list of x coordinates
            x_coords = list(range(self.x_start, self.x_end+1))
            # Generate list of y coords
            y_coords = [self.y_start]*len(x_coords)
            # Zip each x and y in a tuple to represent a cell
            zipped = zip(x_coords, y_coords)
            coords_set = set(zipped)

        elif self.is_vertical:
            # Generate list of y coordinates
            y_coords = list(range(self.y_start, self.y_end+1))
            # Generate list of x coords
            x_coords = [self.x_start]*len(y_coords)
            # Zip each x and y in a tuple to represent a cell
            zipped = zip(x_coords, y_coords)
            coords_set = set(zipped)

        return coords_set

    def length(self):
        """ Get length of ship (the number of cells the ship occupies).
        
        Returns:
            int : The number of cells the ship occupies
        """
        # Count number of ship cells
        ship_len = len(self.cells)
        return ship_len

    def is_occupying_cell(self, cell):
        """ Check whether the ship is occupying a given cell

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to check

        Returns:
            bool : return True if the given cell is one of the cells occupied 
                by the ship. Otherwise, return False
        """

        if cell in self.cells:
            return True
        return False
    
    def receive_damage(self, cell):
        """ Receive attack at given cell. 
        
        If ship occupies the cell, add the cell coordinates to the set of 
        damaged cells. Then return True. 
        
        Otherwise return False.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the cell coordinates that is damaged

        Returns:
            bool : return True if the ship is occupying cell (ship is hit). 
                Return False otherwise.
        """

        if self.is_occupying_cell(cell):
            self.damaged_cells.add(cell)
            return True
        return False
    
    def count_damaged_cells(self):
        """ Count the number of cells that have been damaged.
        
        Returns:
            int : the number of cells that are damaged.
        """

        return len(self.damaged_cells)
        
    def has_sunk(self):
        """ Check whether the ship has sunk.
        
        Returns:
            bool : return True if the ship is damaged at all its positions. 
                Otherwise, return False
        """

        if self.length() == self.count_damaged_cells():
            return True
        return False
    
    def is_near_ship(self, other_ship):
        """ Check whether a ship is near another ship instance.
        
        Hint: Use the method is_near_cell(...) to complete this method.

        Args:
            other_ship (Ship): another Ship instance against which to compare

        Returns:
            bool : returns True if and only if the coordinate of other_ship is 
                near to this ship. Returns False otherwise.
        """
        assert isinstance(other_ship, Ship)
        
        # Check if any cell of other_ship is near our ship
        for cell in other_ship.cells:
            if self.is_near_cell(cell):
                return True
        return False

    def is_near_cell(self, cell):
        """ Check whether the ship is near an (x,y) cell coordinate.

        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any part of the ship OR is at the corner of the ship. Returns False otherwise.
        """
        return (self.x_start-1 <= cell[0] <= self.x_end+1 
                and self.y_start-1 <= cell[1] <= self.y_end+1)


class ShipFactory:
    """ Class to create new ships in specific configurations."""
    def __init__(self, board_size=(10,10), ships_per_length=None):
        """ Initialises the ShipFactory class with necessary information.
        
        Args: 
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
        """
        self.board_size = board_size
        
        if ships_per_length is None:
            # Default: lengths 1 to 5, one ship each
            self.ships_per_length = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        else:
            self.ships_per_length = ships_per_length

    @classmethod
    def create_ship_from_str(cls, start, end, board_size=(10,10)):
        """ A class method for creating a ship from string based coordinates.
        
        Example usage: ship = ShipFactory.create_ship_from_str("A3", "C3")
        
        Args:
            start (str): starting coordinate of the ship (example: 'A3')
            end (str): ending coordinate of the ship (example: 'C3')
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)

        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        converter = CellConverter(board_size)
        return Ship(start=converter.from_str(start),
                    end=converter.from_str(end))

    def generate_ships(self):
        """ Generate a list of ships in the appropriate configuration.
        
        The number and length of ships generated must obey the specifications 
        given in self.ships_per_length.
        
        The ships must also not overlap with each other, and must also not be too close to one another (as defined earlier in Ship::is_near_ship())
        
        The coordinates should also be valid given self.board_size
        
        Returns:
            list[Ships] : A list of Ship instances, adhering to the rules above
        """
        # TODO: Complete this method

        def try_generate_ships():
            """ Helper function that tries to generate a valid set of ships. """
            ships = []
            for ship_length, num_ships in self.ships_per_length.items():
                for i in range(num_ships):

                    # Generate a random ship until it is valid
                    is_valid_candidate = False
                    start_time = time.time()
                    while not is_valid_candidate:

                        # Check how much time spent in while loop, if more than 1 sec, break
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        if elapsed_time > 1:
                            # print("Couldn't find a valid set of ships.")
                            return []

                        # Generate random orientation (0 for vertical, 1 for horizontal)
                        orient = random.randint(0,1)
                        
                        if orient == 0:
                            # Create a vertical ship
                            # Generate random start_x coordinate
                            start_x = random.randint(1, self.board_size[0])
                            end_x = start_x
                            # Generate random start_y coordinate, such that end_y is inside board
                            start_y = random.randint(1, self.board_size[1] - (ship_length - 1))
                            end_y = start_y + ship_length - 1

                        elif orient == 1:
                            # Create a horizontal ship
                            # Generate random start_x coordinate, such that end_x is inside board
                            start_x = random.randint(1, self.board_size[0] - (ship_length - 1))
                            end_x = start_x + ship_length - 1
                            # Generate random start_y coordinate
                            start_y = random.randint(1, self.board_size[1])
                            end_y = start_y

                        # Create candidate ship
                        start = (start_x, start_y) 
                        end = (end_x, end_y)
                        ship_cand = Ship(start, end)

                        # Check if candidate ship is near existing ships
                        is_close_ship = False
                        for ship in ships:
                            is_close_ship = ship.is_near_ship(ship_cand)
                            # Break loop if found at least one close ship
                            if is_close_ship:
                                break
                        
                        is_valid_candidate = not is_close_ship

                    # Append valid candidate to list of ships
                    ships.append(ship_cand)

            # Return generated ships in the helper function
            return ships

        # Try to generate a valid set of ships
        generated_ships = []
        start_time = time.time()
        while not generated_ships:
            # Stop trying if can't find valid set of ships in 10 seconds
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 10:
                break
            # Use helper function to try to generate a set of ships
            generated_ships = try_generate_ships()

        return generated_ships
        
        
if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    ship = Ship(start=(3, 3), end=(5, 3))
    # ship = Ship(start=(5, 3), end=(5, 3))
    # print(ship.is_horizontal())
    # print(ship.is_vertical())

    # print(ship.get_cells())
    # print(ship.length())
    # print(ship.is_horizontal())
    # print(ship.is_vertical())
    # print(ship.is_occupying_cell((4, 3)))
    # # print(ship.is_near_cell((5, 3)))
    

    # print(ship.receive_damage((4, 3)))
    # print(ship.receive_damage((5, 3)))
    # print(ship.has_sunk())
    # print(ship.receive_damage((3, 3)))
    # print(ship.damaged_cells)
    # print(ship.length())
    # print(ship.has_sunk())
    
    # ship2 = Ship(start=(2, 1), end=(2, 2))
    # print(ship.is_near_ship(ship2))

    # For Task 3
    ships = ShipFactory().generate_ships()
    print(ships)
        
    