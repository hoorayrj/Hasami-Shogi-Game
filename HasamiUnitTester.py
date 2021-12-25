# Description: Hasami Shogi Game Unit tester

import unittest
from HasamiShogiGame import HasamiShogiGame


class TestHasamiShogiGame(unittest.TestCase):
    """Contains unit tests for the Library class and methods"""

    def setUp(self):
        """Pass the setUp Method"""
        self.game = HasamiShogiGame()

    def test_get_player(self):
        """Test if the method active player"""
        player = self.game.get_active_player()

        # Check if active player is correctly returned
        self.assertEqual(player, 'BLACK')

        # Check if after a move, active player performed
        self.game.make_move('i2', 'h2')
        self.assertEqual('RED', self.game.get_active_player())

    def test_player_starting_piece(self):
        """Check if starting piece is the player's turn"""
        result = self.game.make_move('a1', 'b2')

        self.assertFalse(result)

    def test_empty_cell_move(self):
        """Check if the ending position is empty"""
        result = self.game.make_move('i4', 'a4')

        self.assertFalse(result)

    def test_player_turn(self):
        """Test if the player turn changes correctly"""
        self.game.make_move('i1', 'h1')

        # Test that the player turn changes correctly
        self.assertEqual('RED', self.game.get_active_player())

        # red turn
        self.game.make_move('a1', 'b1')
        self.assertEqual('BLACK', self.game.get_active_player())

    def test_horiz_vert_move(self):
        """Test if the move is a valid horizontal or vertical move"""
        result_vert = self.game.make_move('i1', 'd1')
        self.assertTrue(result_vert)

        # red move
        self.game.make_move('a1', 'b1')

        result_horiz = self.game.make_move('d1', 'd4')
        self.assertTrue(result_horiz)

        # Test if attempted diagonal move is false
        result_dia = self.game.make_move('b1', 'c2')
        self.assertFalse(result_dia)

    def test_pieces_between(self):
        """Tests that if there are pieces in the way of the move"""
        self.game.make_move('i1', 'd1')

        self.assertFalse(self.game.make_move('a1', 'g1'))

    def test_get_square_occupant(self):
        """Tests the return of the cell piece"""
        # Test Black piece
        self.assertEqual('BLACK', self.game.get_square_occupant('i1'))

        # Test Red piece
        self.assertEqual('RED', self.game.get_square_occupant('a1'))

        # Test empty cell
        self.assertEqual('NONE', self.game.get_square_occupant('c4'))

        # Test if get's the correct index of a cell
        self.assertEqual(0, self.game.search_board('a1', 'yes'))
        self.assertEqual(9, self.game.search_board('b1', 'yes'))

    def test_cell_start_change(self):
        "Tests that when a move has been make, the starting cell ID has changed."
        # Test for black move
        self.game.make_move('i7', 'd7')

        self.assertEqual('NONE', self.game.get_square_occupant('i7'))

        # Test for red move
        self.game.make_move('a4', 'g4')
        self. assertEqual('NONE', self.game.get_square_occupant('a4'))

    def test_cell_end_change(self):
        """Test that when a move has been made, the ending cell piece has been updated correctly"""
        # Test for black move
        self.game.make_move('i7', 'd7')

        self.assertEqual('BLACK', self.game.get_square_occupant('d7'))

        # Test for red move
        self.game.make_move('a3', 'd3')
        self.assertEqual('RED', self.game.get_square_occupant('d3'))

    def test_capture_check_right(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For right check
        self.game.make_move('i6', 'd6')
        self.game.make_move('a5', 'd5')
        self.game.make_move('i8', 'h8')
        self.game.make_move('a4', 'd4')
        self.game.make_move('i3', 'd3')

        # Check that Red has 2 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('d4'))
        self.assertEqual('NONE', self.game.get_square_occupant('d5'))
        self.assertEqual(2, self.game.get_num_captured_pieces('RED'))

    def test_capture_check_left(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For left check
        self.game.make_move('i1', 'd1')
        self.game.make_move('a4', 'd4')
        self.game.make_move('i2', 'h2')
        self.game.make_move('a5', 'd5')
        self.game.make_move('i9', 'h9')
        self.game.make_move('a3', 'd3')
        self.game.make_move('i8', 'h8')
        self.game.make_move('a2', 'd2')
        self.game.make_move('i6', 'd6')

        # Check that Red has 3 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('d4'))
        self.assertEqual('NONE', self.game.get_square_occupant('d5'))
        self.assertEqual('NONE', self.game.get_square_occupant('d2'))
        self.assertEqual(4, self.game.get_num_captured_pieces('RED'))

    def test_capture_check_bottom(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For bottom check
        self.game.make_move('i1', 'f1')
        self.game.make_move('a4', 'h4')
        self.game.make_move('f1', 'f2')
        self.game.make_move('a3', 'g3')
        self.game.make_move('f2', 'f3')
        self.game.make_move('g3', 'g4')
        self.game.make_move('f3', 'f4')

        # Check that Red has 2 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('h4'))
        self.assertEqual('NONE', self.game.get_square_occupant('g4'))
        self.assertEqual(2, self.game.get_num_captured_pieces('RED'))

    def test_capture_check_top(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For top check
        self.game.make_move('i1', 'b1')
        self.game.make_move('a9', 'e9')
        self.game.make_move('b1', 'b4')
        self.game.make_move('e9', 'd9')
        self.game.make_move('i4', 'c4')
        self.game.make_move('d9', 'd4')

        # Check that Black has 2 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('b4'))
        self.assertEqual('NONE', self.game.get_square_occupant('c4'))
        self.assertEqual(2, self.game.get_num_captured_pieces('BLACK'))

    def test_capture_check_bottom_right(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For bottom right corner check
        self.game.make_move('i8', 'h8')
        self.game.make_move('a9', 'h9')
        self.game.make_move('h8', 'h7')
        self.game.make_move('a8', 'i8')

        # Check that Black has 1 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('i9'))
        self.assertEqual(1, self.game.get_num_captured_pieces('BLACK'))

    def test_capture_check_bottom_left(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For bottom left corner check
        self.game.make_move('i2', 'h2')
        self.game.make_move('a1', 'h1')
        self.game.make_move('h2', 'h3')
        self.game.make_move('a2', 'i2')

        # Check that Black has 1 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('i1'))
        self.assertEqual(1, self.game.get_num_captured_pieces('BLACK'))

    def test_capture_check_top_right(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For top right corner check
        self.game.make_move('i9', 'b9')
        self.game.make_move('a8', 'b8')
        self.game.make_move('i8', 'c8')
        self.game.make_move('b8', 'b4')
        self.game.make_move('c8', 'a8')

        # Check that RED has 1 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('a9'))
        self.assertEqual(1, self.game.get_num_captured_pieces('RED'))

    def test_capture_check_top_left(self):
        """Test to make sure the pieces are captured according to the game rules"""
        # For top left corner check
        self.game.make_move('i2', 'h2')
        self.game.make_move('a4', 'd4')
        self.game.make_move('i6', 'h6')
        self.game.make_move('a5', 'd5')
        self.game.make_move('i7', 'b7')
        self.game.make_move('a6', 'c6')
        self.game.make_move('h6', 'g6')
        self.game.make_move('a9', 'b9')
        self.game.make_move('i3', 'd3')
        self.game.make_move('a1', 'b1')
        self.game.make_move('b7', 'b6')
        self.game.make_move('b1', 'c1')
        self.game.make_move('g6', 'd6')

        # Check that RED has 3 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('c6'))
        self.assertEqual('NONE', self.game.get_square_occupant('d4'))
        self.assertEqual('NONE', self.game.get_square_occupant('d5'))
        self.assertEqual(3, self.game.get_num_captured_pieces('RED'))

    def test_capture_check_two(self):
        """Test to check capture in row and column at the same time"""
        # For top left corner check
        self.game.make_move('i1', 'b1')
        self.game.make_move('a2', 'b2')
        self.game.make_move('i2', 'c2')
        self.game.make_move('b2', 'b3')
        self.game.make_move('c2', 'a2')

        # Check that RED has 1 pieces captured
        self.assertEqual('NONE', self.game.get_square_occupant('a1'))
        self.assertEqual(1, self.game.get_num_captured_pieces('RED'))

    def test_captured_pieces(self):
        """Checks the captured pieces, when first starting the game"""
        self.assertEqual(self.game.get_num_captured_pieces('BLACK'), 0)
        self.assertEqual(self.game.get_num_captured_pieces('RED'), 0)

        # Set the pieces to make a move, captures 2 of red's pieces.
        self.game.make_move('i6', 'd6')
        self.game.make_move('a5', 'd5')
        self.game.make_move('i8', 'h8')
        self.game.make_move('a4', 'd4')
        self.game.make_move('i3', 'd3')

        self.assertEqual(0, self.game.get_num_captured_pieces('BLACK'))
        self.assertEqual(2, self.game.get_num_captured_pieces('RED'))



    def test_game_sate(self):
        """Tests game_state method. Returns the correct game state also test multiple row and column
        capture"""
        result = self.game.get_game_state()

        # Check if the result is correct
        self.assertEqual(result, 'UNFINISHED')

        # Make a couple of moves to check the game state

        self.game.make_move('i2', 'h2')
        self.game.make_move('a4', 'd4')
        self.game.make_move('i6', 'h6')
        self.game.make_move('a5', 'd5')
        self.game.make_move('i7', 'b7')
        self.game.make_move('a6', 'c6')
        self.game.make_move('h6', 'g6')
        self.game.make_move('a9', 'b9')

        # Check that the result is correct
        self.assertEqual('UNFINISHED', self.game.get_game_state())

        self.game.make_move('i3', 'd3')
        self.game.make_move('a1', 'b1')
        self.game.make_move('b7', 'b6')
        self.game.make_move('b1', 'c1')
        self.game.make_move('g6', 'd6')
        self.game.make_move('a3', 'a5')
        self.game.make_move('i8', 'h8')
        self.game.make_move('a5', 'd5')
        self.game.make_move('i9', 'h9')
        self.game.make_move('a2', 'a4')
        self.game.make_move('h8', 'g8')
        self.game.make_move('a4', 'd4')
        self.game.make_move('h9', 'g9')
        self.game.make_move('a7', 'd7')
        self.game.make_move('g9', 'f9')
        self.game.make_move('a8', 'd8')
        self.game.make_move('f9', 'd9')
        self.game.make_move('c1', 'c6')
        self.game.make_move('i5', 'i6')
        self.game.make_move('b9', 'c9')
        self.game.make_move('i6', 'd6')
        self.game.print_board()

        # Check that black won
        self.assertEqual('BLACK_WON', self.game.get_game_state())
        self.assertEqual(8, self.game.get_num_captured_pieces('RED'))

        # Try to make additional moves after a player has won
        self.assertFalse(self.game.make_move('c9', 'c8'))

    def test_make_move(self):
        """Test make move returns True after successful move"""
        self.assertTrue(self.game.make_move('i3','d3'))

    def test_column_corner(self):
        """
        Tests the column and corner capture
        :return:
        """
        self.game.make_move('i1', 'h1')
        self.game.make_move('a3', 'g3')
        self.game.make_move('h1', 'h4')
        self.game.make_move('a1', 'i1')
        self.game.make_move('i3','h3')
        self.game.make_move('g3', 'g1')
        self.game.make_move('h4', 'e4')
        self.game.make_move('a2', 'f2')
        self.game.make_move('e4', 'e1')
        self.game.make_move('f2', 'f1')
        self.game.make_move('h3', 'h1')

        self.assertEqual(3, self.game.get_num_captured_pieces('RED'))