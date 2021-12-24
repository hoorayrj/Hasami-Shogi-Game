# Simulator for the Hasami Shogi Game also known as Intercepting Chess. This is a 2 player game, where players take turns making their moves.
# The rules of the game follow variant 1 from https://en.wikipedia.org/wiki/Hasami_shogi. Run the game and have fun!

class HasamiShogiGame:
    """
    Hasami Shogi Game Simulator, including all methods to play the game. This is the only class for the game.
    """

    def __init__(self):
        """
        Initializes all data members for the Hasami Shogi Game. Includes board, player piece info, and game state.
        """
        # Self._players will be a list to keep track  the player pieces. Both players will start with 9 pieces each.
        # self._player_turn  will alternate from 'BLACK'/'RED' after each player's turn.
        self._player_cap_pieces = [['BLACK', 0], ['RED', 0]]
        self._player_turn = 'BLACK'
        self._game_state = 'UNFINISHED'
        self._print = "  "
        self._sequence_check = []
        self._captured_cells = []
        self._cell_id = None
        self._cell_search = None

        # Initialize Hasami Shogi Board stored in a list. The board/list will keep all the squares/coordinates of the
        # board and keep track of occupancy of each square. For example, ['a', '1', 'R'] will represent the column 1,
        # row 'a' and has 'RED' player on there.
        self._hasami_board = []

        # Creates first row with Red pieces
        for column in range(1, 10):
            cell = 'a' + str(column)
            self._hasami_board.append([cell, 'R'])

        # Creates an empty board
        for row in range(98, 105):
            for column in range(1, 10):
                cell = chr(row) + str(column)
                self._hasami_board.append([cell, '.'])

        # Creates last row, with Black pieces
        for column in range(1, 10):
            cell = 'i' + str(column)
            self._hasami_board.append([cell, 'B'])

    def get_game_state(self):
        """
        Takes no parameters, and provides the state of the game.
        :return: 'UNFINISHED', 'RED_WON', 'BLACK_WON'
        """
        # Check the number of pieces captured for each player, if each player has more than 1 piece left, then
        # set game as 'UNFINISHED'.
        if self.get_num_captured_pieces('BLACK') < 8 and self.get_num_captured_pieces('RED') < 8:
            self._game_state = 'UNFINISHED'
            # Else if 'black' has less than 2 pieces left, either 1 or 0 pieces, Red wins
        elif self.get_num_captured_pieces('BLACK') >= 8:
            self._game_state = 'RED_WON'
        elif self.get_num_captured_pieces('RED') >= 8:
            self._game_state = 'BLACK_WON'

        return self._game_state

    def get_active_player(self):
        """
        Takes no parameters and returns who's turn it is.
        :return: either 'RED' or 'BLACK'
        """
        return self._player_turn

    def get_num_captured_pieces(self, player):
        """
        Method that takes given player ('RED' or 'BLACK') and returns the number of pieces of that color that have been
        captured.
        :param player: Either 'RED' or 'BLACK'
        :return: the number of pieces of the player that have been captured
        """
        for color in self._player_cap_pieces:
            if player in color:
                return color[1]

    def make_move(self, cell_start, cell_end):
        """
        Method that takes two parameters and performs the move of the given start and end cells/squares.
        :param cell_start: Starting square to be moved
        :param cell_end: Ending square of the moved piece
        :return: True or False (depending if the move have been performed)
        """
        # Check if entered start and end cells are valid.
        # Check if the active player has a piece on the starting cell if not return False
        if self.get_square_occupant(cell_start)[0] != self.get_active_player()[0]:
            return False

        # Check if the ending cell is empty
        elif self.get_square_occupant(cell_end) != 'NONE':
            return False

        # Check if the if move is legal.
        # Check if the move is a valid horizontal or vertical move. If the rows and columns are different, then
        # that is a diagonal move, which is not valid.
        elif cell_start[0] != cell_end[0] and cell_start[1] != cell_end[1]:
            return False

        # Check if there are any pieces in between the start and end cell. Call the method move_check
        elif self.move_check(cell_start, cell_end) is False:
            return False

        # Check the status of the game, to make sure it is not finished already
        elif self.get_game_state() != 'UNFINISHED':
            return False

        else:
            # If the move is valid, then let the player make the move. Change the start cell as 'NONE' and the
            # end cell as the active player

            # Set the start cell as none
            # Use square_occupant to get the index of the start cell
            self.set_board(self.search_board(cell_start, 'yes'), cell_start, '.')

            # Set the end cell as the active player, using the index of the ending cell
            self.set_board(self.search_board(cell_end, 'yes'), cell_end, self.get_active_player()[0])

            # After the move is done, then need to check if pieces can be taken. Call the capture method.
            # Check to the right of the ending cell
            self.capture_check(cell_end, 'right')
            # Check to the left of the ending cell
            self.capture_check(cell_end, 'left')
            # Check to the bottom of the ending cell
            self.capture_check(cell_end, 'bottom')
            # Check to the top of the ending cell
            self.capture_check(cell_end, 'top')
            # Check corner capture
            self.corner_check(cell_end)

            # If the captured list is not empty, then start reducing the opponents pieces, and set the cells to empty
            if self._captured_cells is not None:
                # Update the number of opponent pieces captured
                if self.get_active_player() == 'BLACK':
                    # Update the red pieces
                    self._player_cap_pieces[1][1] += len(self._captured_cells)
                elif self.get_active_player() == 'RED':
                    # Update the black pieces
                    self._player_cap_pieces[0][1] += len(self._captured_cells)
                # Then set the captured cells to None
                # Loop through the captured cell list then set the cells to None.
                for index in self._captured_cells:
                    self._hasami_board[index][1] = '.'
                # Set the captured cell list to empty:
                self._captured_cells = []

            # Check and update game state
            self.get_game_state()

            # Change the active player
            if self.get_game_state() == 'UNFINISHED':
                if self.get_active_player() == 'BLACK':
                    self._player_turn = 'RED'
                else:
                    self._player_turn = 'BLACK'

            return True

    def search_board(self, cell, index=None):
        """
        Method that searches the board given using binary search
        :param cell: The cell to be checked. Enter cell string, ex. 'b1'
        :param index: If None, then this method only returns the piece occupying the given cell. If not none,
        then this method returns the index of the given cell
        :return: Either occupant of cell or cell index
        """
        # Perform binary search of the board information.
        # Initialize first index number
        first_index = 0
        # Set final index number
        last_index = len(self._hasami_board) - 1

        # Do a while loop to search through the list, stopping when the first index reaches the last index number
        while first_index <= last_index:
            # Set the middle to floor division of first and last index number, gets the middle of the list
            middle_index = (first_index + last_index) // 2
            # Check if the middle number is the target
            if self._hasami_board[middle_index][0] == cell and index is None:
                return self._hasami_board[middle_index][1]
            elif self._hasami_board[middle_index][0] == cell and index is not None:
                # Rest index to None
                index = None
                return middle_index

            # If not check if the middle number is greater than the target
            if self._hasami_board[middle_index][0] > cell:
                # Set the last as the middle number - 1
                last_index = middle_index - 1
            else:
                # Else set the first as the middle number + 1
                first_index = middle_index + 1
        return

    def get_square_occupant(self, cell):
        """
        Method that returns the piece occupied given the cell.
        :param cell: The cell to be checked. Cell to be 'row & column' (for example 'b1')
        :return: 'RED', 'BLACK', or 'NONE', or index of given cell
        """

        occupant = self.search_board(cell)

        if occupant == '.':
            return 'NONE'
        elif occupant == 'R':
            return 'RED'
        elif occupant == 'B':
            return 'BLACK'

    def move_check(self, cell_start, cell_end):
        """
        Takes two parameters and checks whether the move is valid. This checks if the move is either horizontal or
        vertical, and also checks if there are any pieces between the start and ending cells by looping through the
        board information.
        :param cell_start: Starting position of the piece to be moved
        :param cell_end: Ending position of th piece moved
        :return: True if the move is valid, or false, the move is not valid.
        """
        # Check if there are any pieces in between the start and end cell.
        # If move is vertical, columns are the same
        if cell_start[1] == cell_end[1]:
            # Check which direction this move is. Must be checked for the loop to work in the right direction.
            if cell_start[0] > cell_end[0]:
                limit1 = cell_end[0]
                limit2 = cell_start[0]
            else:
                limit1 = cell_start[0]
                limit2 = cell_end[0]
            # Loop through the list.
            for row in range(ord(limit1[0])+1, ord(limit2[0])):
                # Concatenate to combine the row and the column
                cell = chr(row) + str(cell_start[1])
                # Check if the all the cells are empty, if not return False
                if self.get_square_occupant(cell) != 'NONE':
                    return False
        # If move is horizontal, rows are the same.
        else:
            if cell_start[1] > cell_end[1]:
                limit1 = cell_end[1]
                limit2 = cell_start[1]
            else:
                limit1 = cell_start[1]
                limit2 = cell_end[1]
            for column in range(int(limit1)+1, int(limit2)):
                cell = cell_start[0] + str(column)
                if self.get_square_occupant(cell) != 'NONE':
                    return False

    def capture_check(self, cell, line, seq_check=None):
        """
        Recursive method that takes parameters, and returns the number of pieces that has been captured after a move.
        :param cell: ending cell from the player's move
        :param line: Directs the check whether right row, left row, top column, or bottom
        :param seq_check: A list with the cell indexes that have been captured
        :return: Does not return anything
        """
        # To capture pieces, it will follow the Custodian Capture. Where a player's pieces surround the opponent's
        # piece. Given the ending cell, check the row and column to see if there are any pieces that can be taken.
        # Right refers to the right of the cell, left to the left of the cell, top, refers to each row above the cell,
        # and below refers to the rows below the cell.
        if line == 'top':
            # Check column to the top of the ending cell. Convert cell letter to ASCII using ord to get next row over
            self._cell_id = ord(cell[0]) - 1
            # Get the string of the cell to search for the index. Concatenate for the next cell.
            self._cell_search = chr(self._cell_id) + cell[1]
        elif line == 'bottom':
            # Check column to the bottom of the ending cell. Convert cell letter to ASCII using ord to get next
            # row
            self._cell_id = ord(cell[0]) + 1
            # Get the string of the cell to search for the index. Concatenate for the next cell.
            self._cell_search = chr(self._cell_id) + cell[1]
        elif line == 'left':
            # Check row to the left of the ending cell
            self._cell_id = int(cell[1]) - 1
            # Get the string of the cell to search for the index. Concatenate for the next cell.
            self._cell_search = cell[0] + str(self._cell_id)
        elif line == 'right':
            # Check row to the right
            self._cell_id = int(cell[1]) + 1
            # Get the string of the cell to search for the index. Concatenate for the next cell.
            self._cell_search = cell[0] + str(self._cell_id)

        # Base cases to end the recursion
        # If the next cell is beyond the size of the board > i, then stop checking
        if line == 'top' and self._cell_id < ord('a') or line == 'bottom' and self._cell_id > ord('i') or \
                line == 'left' and self._cell_id < 1 or line == 'right' and self._cell_id > 9:
            self._sequence_check = []
            return
        # Set a base case, where the cell to the next cell is the same as the active player, then end it.
        elif self.get_square_occupant(self._cell_search)[0] == self.get_active_player()[0]:
            if self._sequence_check is not None:
                for captured_cell in self._sequence_check:
                    self._captured_cells.append(captured_cell)
                self._sequence_check = []
            return
        # If the next cell after that is empty, then that means no sequence, clear the sequence check list and return
        elif self.get_square_occupant(self._cell_search) == 'NONE':
            self._sequence_check = []
            return

        # Search for the index of that cell to search
        board_index = self.search_board(self._cell_search, 'yes')
        # Check the value of that cell if it is empty or if doesn't equal the active player
        if self._hasami_board[board_index][1] != '.' or self._hasami_board[board_index][1] != \
                self.get_active_player()[0]:
            # Add the index to the list of checked cells
            self._sequence_check.append(board_index)
            # Call the check again to search the next cell
            self.capture_check(self._cell_search, line, self._sequence_check)

        return

    def corner_check(self, cell):
        """
        Method that takes 1 parameter, and checks a corner capture in the game.
        :param cell: the ending cell from the player's move
        :return: If the corner piece has been captured
        """
        # Check the top left corner
        if cell == 'a2' or cell == 'b1':
            if self.get_square_occupant('a1') != self.get_active_player()[0] and \
                    self.get_square_occupant('a1') != 'NONE':
                if self.get_square_occupant('b1')[0] == self.get_active_player()[0] and \
                        self.get_square_occupant('a2')[0]\
                        == self.get_active_player()[0]:
                    self._captured_cells.append(self.search_board('a1', 'yes'))

        # Check the top right corner of the board
        elif cell == 'a8' or cell == 'b9':
            if self.get_square_occupant('a9') != self.get_active_player()[0] and \
                    self.get_square_occupant('a9') != 'NONE':
                if self.get_square_occupant('b9')[0] == self.get_active_player()[0] and \
                        self.get_square_occupant('a8')[0]\
                        == self.get_active_player()[0]:
                    self._captured_cells.append(self.search_board('a9', 'yes'))

        # Check the bottom left corner of the board
        elif cell == 'h1' or cell == 'i2':
            if self.get_square_occupant('i1') != self.get_active_player()[0] and \
                    self.get_square_occupant('i1') != 'NONE':
                if self.get_square_occupant('h1')[0] == self.get_active_player()[0] and \
                        self.get_square_occupant('i2')[0]\
                        == self.get_active_player()[0]:
                    self._captured_cells.append(self.search_board('i1', 'yes'))

        # Check the bottom right corner of the board
        elif cell == 'h9' or cell == 'i8':
            if self.get_square_occupant('i9') != self.get_active_player()[0] and \
                    self.get_square_occupant('i9') != 'NONE':
                if self.get_square_occupant('h9')[0] == self.get_active_player()[0] and \
                        self.get_square_occupant('i8')[0]\
                        == self.get_active_player()[0]:
                    self._captured_cells.append(self.search_board('i9', 'yes'))

    def print_board(self):
        """
        Prints the board to see the moves
        :return: the board
        """
        # Add a couple of spaces
        self._print = '  '
        # header row, loop through to print the column header numbers
        for i in range(1, 10):
            self._print += str(i) + ' '
        print(self._print)
        # Set the row as the ASCII Number letter a
        row = 97
        # Loop through the letters and the board information to print them.
        for cell in range(0, len(self._hasami_board)):
            # Print a new row
            if cell == 0 or cell % 9 == 0:
                self._print = chr(row)
            # Get the information from the board and print
            if self._hasami_board[cell][1] == 'R':
                self._print += ' ' + 'R'
            elif self._hasami_board[cell][1] == 'B':
                self._print += ' ' + 'B'
            else:
                self._print += ' ' + self._hasami_board[cell][1]

            # Checks if the cell ends with these specific numbers. If so, then prints the row.
            if cell == 8 or cell == 17 or cell == 26 or cell == 35 or cell == 44 or cell == 53 or cell == 62 or \
                    cell == 71 or cell == 80:
                print(self._print)
                row += 1

        print(' ')

    def set_board(self, index, cell, piece):
        """
        Takes three parameters. This method updates the board list with the given information.
        :param index: An integer, that is used to update the list within the board information list
        :param cell: A string, that represents the cell that is being replaced.
        :param piece: Either 'R', 'B', or '.', represents the pieces in the game
        :return: Does not return anything.
        """
        self._hasami_board[index] = [cell, piece]
        return

def main():
    """
    Main function to run the Hasami Shogi game. This lets the players take turn, and after each move is made, the
    board is printed to see the move of the player
    :return: Doesn't return anything
    """

    print("--------------------------------------")
    print("---Welcome to the Hasami Shogi Game---")
    print("--------------------------------------")
    print("Rules: Game consists of 2 players, each taking turns. One player moves the Black Pieces (B) and the \n"
          "second player moves the Red Pieces (R). Purpose of the game is for the one player to capture as many of the \n"
          "opponent's pieces. When a player has captured all of the opponents pieces or remaining one piece, then the \n"
          "player won. To capture a pieces, a player needs to surround the opponents piece on a move. Also known as a \n"
          "Custodian Capture. For example, B R R R B, the B pieaces surround the Red pieces, so all 3 Red Pieces have \n"
          "been captured. A Corner Capture, is when a player's pieace surrounds an opponents piece at the corner of \n"
          "the board, on both the column and the row position.")
    print("Game Play: Black moves first. Then Red moves. Player takes turns. Pieces can only go vertical or horizontal. \n"
          "Diagonal moves are not allowed. Players can move as many places as they want, only if there are no pieaces \n"
          "in the way. To move type in the starting piece you want to move and the cell you want to move to. For \n"
          "example, 'f1, f4'. \n")

    print("The Board")
    game = HasamiShogiGame()
    game.print_board()


    while game.get_game_state() == "UNFINISHED":
        print(game.get_active_player() + "'s" + " " + "turn")

        start_move = str(input("Type in piece to move [ENTER]: "))
        end_move = str(input("Enter cell to move piece [ENTER]: "))

        game.make_move(start_move, end_move)

        game.print_board()

    if game.get_game_state() == 'BLACK_WON':
        print("Black Won!!")
    else:
        print("Red Won!!")

# Check if the file is run as a script.
if __name__ == '__main__':
    main()