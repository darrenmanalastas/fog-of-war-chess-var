
# Author: Darren Manalastas
# GitHub username: darrenmanalastas
# Date: 12/08/2024
# Description: Fog of War Chess program that performs the basic functionality of a chess game but with additional
# fog of war variant rules

class ChessVar:
    """Represents the Fog of War chess variant that handles the basic functionality of the chess game as well as the
    additional Fog of War rules"""
    def __init__(self):
        """Initializes the Chess Variant with the following private data members: self._game_state, self._turn,
        self._board, self._temp_board, self._curr_pos and self._next_pos"""
        self._game_state = 'UNFINISHED'
        self._turn = 1
        self._board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                       ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                       ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                       ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self._temp_board = []
        self._curr_pos = [0, 0]
        self._next_pos = [0, 0]

    def get_game_state(self):
        """Returns the private game_state variable"""
        return self._game_state

    def get_board(self, perspective):
        """Takes in the perspective as a parameter and returns the regular board if 'audience' was passed and
        returns the temp_board if 'white' or 'black' perspective was passed
        If white or black was passed the update_helper functions are called to update the temp_board
        then the temp_board is returned"""
        if perspective == 'audience':
            return self._board
        else:
            self._temp_board = []  # Reset the temp_board
            for row in self._board:
                self._temp_board.append(list(row))  # Creates a copy of the regular board
            self.update_board(perspective)
            return self._temp_board

    def set_game_state(self, captured):
        """Takes in the captured king piece as a parameter, changes the game_state to WHITE_WON if lowercase k was
        passed and changes game_state to BLACK_WON if uppercase K was passed"""
        if captured == 'k':
            self._game_state = 'WHITE_WON'
        if captured == 'K':
            self._game_state = 'BLACK_WON'

    def update_board(self, perspective):
        """Helper function that updates the temp_board for the get_board function
        Calls the update_board helper function to go through the list of possible moves to verify if there is a
        possible capture move, updating it to '*'
        Updates any letters to ' * ', and updates ' * ' to a letter based on the regular board"""
        if perspective == 'white':
            pieces = 'PNBRQK'
        if perspective == 'black':
            pieces = 'pnbrqk'
        for row_index in range(8):
            for char_index in range(8):
                char = self._temp_board[row_index][char_index]
                if char == ' ':
                    continue
                if char in pieces:  # Stores the current piece in the curr_pos variable if it is uppercase
                    self._curr_pos[0] = row_index
                    self._curr_pos[1] = char_index
                    self.update_board_helper(char, row_index, char_index)
        for row_index in range(8):  # For loop used to flip a letter into ' * ', and flip ' * ' into a letter
            for char_index in range(8):
                if perspective == 'white' and self._temp_board[row_index][char_index].islower()\
                        or perspective == 'black' and self._temp_board[row_index][char_index].isupper():
                    self._temp_board[row_index][char_index] = '*'
                elif self._temp_board[row_index][char_index] == '*':
                    self._temp_board[row_index][char_index] = self._board[row_index][char_index]
                else:
                    continue

    def update_board_helper(self, char, vert, hori):
        """Update_board helper function that goes through the list of possible capture moves for the
        current_position and checks if each is valid, updating the valid moves to ' * '"""
        poss_moves = {'p': [[vert-1, hori-1], [vert-1, hori+1]],
                      'r': [[vert+1, hori-0], [vert-0, hori+1], [vert-1, hori+0], [vert-0, hori-1]],
                      'b': [[vert+1, hori-1], [vert+1, hori+1], [vert-1, hori+1], [vert-1, hori-1]],
                      'n': [[vert-2, hori+1], [vert-2, hori-1], [vert+2, hori+1], [vert+2, hori-1],
                            [vert+1, hori-2], [vert+1, hori+2], [vert-1, hori+2], [vert-1, hori-2]],
                      'q': [[vert+1, hori-0], [vert-0, hori+1], [vert-1, hori+0], [vert-0, hori-1],
                            [vert+1, hori-1], [vert+1, hori+1], [vert-1, hori+1], [vert-1, hori-1]],
                      'k': [[vert+1, hori-0], [vert-0, hori+1], [vert-1, hori+0], [vert-0, hori-1],
                            [vert+1, hori-1], [vert+1, hori+1], [vert-1, hori+1], [vert-1, hori-1]]
                      }  # Dictionary of all possible capture moves
        if char == 'p':
            poss_moves[char] = [[vert+1, hori-1], [vert+1, hori+1]]  # Flip the pawns moves if black player
        for moves in poss_moves[char.lower()]:
            if moves[0] > 7 or moves[0] < 0 or moves[1] > 7 or moves[1] < 0:  # Check if move is within bounds
                continue
            if self._temp_board[moves[0]][moves[1]].isupper() and char.isupper() \
                    or self._temp_board[moves[0]][moves[1]].islower() and char.islower():
                # Check if the case is correct
                continue
            self._next_pos[0] = moves[0]
            self._next_pos[1] = moves[1]
            if self._temp_board[moves[0]][moves[1]] == ' ':
                if self._temp_board[vert][hori].lower() == 'p'\
                        or self._temp_board[vert][hori].lower() == 'n'\
                        or self._temp_board[vert][hori].lower() == 'k':
                    continue  # Since p, n, k do not have the ability to move multiple spaces
                if self._temp_board[vert][hori].lower() == 'b' \
                        or self._temp_board[vert][hori].lower() == 'r'\
                        or self._temp_board[vert][hori].lower() == 'q':
                    # b, r, q have the ability to move multiple spaces provided path is not blocked
                    vert_direction = moves[0] - vert
                    hori_direction = moves[1] - hori
                    while self._temp_board[moves[0]][moves[1]] == ' ':  # Iterates through path until it's not blocked
                        moves[0] += vert_direction
                        moves[1] += hori_direction
                        if moves[0] > 7 or moves[0] < 1 or moves[1] > 7 or moves[1] < 1:
                            break
                if moves[0] > 7 or moves[0] < 0 or moves[1] > 7 or moves[1] < 0 \
                        or self._temp_board[moves[0]][moves[1]].isupper() and char.isupper() \
                        or self._temp_board[moves[0]][moves[1]].islower() and char.islower():
                    continue  # Check if final move is within bounds and is the correct case after iteration
            if char.lower() == 'p':  # If a pawn, calls the pawn update helper function to check if its a legal move
                poss_move = self.pawn_update_helper(char, self._curr_pos[0], self._curr_pos[1])
            else:
                poss_move = self.legal_move(self._temp_board[vert][hori], self._temp_board[moves[0]][moves[1]])
            if poss_move is True:
                self._temp_board[moves[0]][moves[1]] = '*'  # Updates the possible capture move to a '*'

    def pawn_update_helper(self, char, vert, hori):
        """Update helper function for the pawn isolating its capture logic without keeping track of the turns
        Taking the char, vert and hori from the update_board_helper function"""
        if char == 'P':
            one_step = -1
        else:
            one_step = 1
        if self._board[self._next_pos[0]][self._next_pos[1]] != ' ':  # Pawn capture logic
            if hori > 0 and self._next_pos == [vert + one_step, hori - 1]:
                return True
            if hori < 7 and self._next_pos == [vert + one_step, hori + 1]:
                return True
        return False

    def make_move(self, move_1, move_2):
        """Takes in the current position and the next position as parameters
        Checks if the game_state is not unfinished and returns false if so
        Passes the moves to the convert_move function to convert it to the proper list indexing
        Calls the verify_move function to further test if the move is valid
        If it's valid the move is made and the captured piece is tracked
        If the captured piece is a King,the set_game_state function is called to end the game
        Increments the turn by one and Returns True"""
        if self._game_state != 'UNFINISHED':
            return False
        self.convert_move(move_1, move_2)
        valid_move = self.verify_move()
        if valid_move is False:
            return False
        captured = self._board[self._next_pos[0]][self._next_pos[1]]
        self._board[self._next_pos[0]][self._next_pos[1]] = self._board[self._curr_pos[0]][self._curr_pos[1]]
        self._board[self._curr_pos[0]][self._curr_pos[1]] = ' '
        if captured == 'k' or captured == 'K':
            self.set_game_state(captured)
        self._turn += 1
        return True

    def convert_move(self, curr_pos, next_pos):
        """Make_move helper function used to convert the parameters passed into the proper nested list indexing
        storing these values in the self._curr_pos and self._next_pos initialized in the class"""
        letters = 'abcdefgh'
        numbers = '87654321'
        self._curr_pos[0], self._curr_pos[1] = numbers.find(curr_pos[1]), letters.find(curr_pos[0])
        self._next_pos[0], self._next_pos[1] = numbers.find(next_pos[1]), letters.find(next_pos[0])

    def verify_move(self):
        """Make_move helper function that further tests if the move is valid
        If the indexing of the current_position is invalid then returns False
        If the current_piece is not a letter then returns False
        If the current_piece belongs to white player, and it is the black player's turn or vice versa returns false
        Call the legal_move helper function to check if the move follows the proper rules of a particular chess piece"""
        if (self._curr_pos[0] == -1 or self._curr_pos[1] == -1
                or self._next_pos[0] == -1 or self._next_pos[1] == -1):
            return False

        curr_piece = self._board[self._curr_pos[0]][self._curr_pos[1]]
        next_piece = self._board[self._next_pos[0]][self._next_pos[1]]
        if curr_piece.isalpha() is False:
            return False
        if curr_piece.islower() and self._turn % 2 == 1 or curr_piece.isupper() and self._turn % 2 == 0:
            return False
        return self.legal_move(curr_piece, next_piece)

    def legal_move(self, curr_piece, next_piece):
        """Verify_move helper function to tests the rules for a chess piece
        If the white/black player tries to capture its own piece return False
        The vertical and horizontal directions are calculated
        Call the current_piece function based on the chess_piece dictionary, passing the direction calculated
        as well as the vertical and horizontal positions of the current position, in order to verify if the move is
        valid for the specific rules of each individual chess piece"""
        chess_pieces = {'p': self.pawn,
                        'r': self.rook,
                        'b': self.bishop,
                        'n': self.knight,
                        'q': self.queen,
                        'k': self.king
                        }
        if curr_piece.islower() and next_piece.islower() or curr_piece.isupper() and next_piece.isupper():
            return False
        if self._next_pos[0] > self._curr_pos[0]:
            vert_direction = 1
        elif self._next_pos[0] < self._curr_pos[0]:
            vert_direction = -1
        else:
            vert_direction = 0

        if self._next_pos[1] > self._curr_pos[1]:
            hori_direction = 1
        elif self._next_pos[1] < self._curr_pos[1]:
            hori_direction = -1
        else:
            hori_direction = 0
        return chess_pieces[curr_piece.lower()](vert_direction, hori_direction, self._curr_pos[0], self._curr_pos[1])

    def pawn(self, vert_direction, hori_direction, vert, hori):
        """Pawn helper function containing the logic of a pawn chess piece
        Taking the vert_direction, hori_direction, vert and hori parameters from the legal_move function
        A pawn has different rules for its movement and capture so there are two different cases
        Returns false if the move is not valid and true if it is"""
        if self._turn % 2 == 1:
            one_step = -1
            valid_double_row = 6
        else:
            one_step = 1
            valid_double_row = 1

        if self._board[self._next_pos[0]][self._next_pos[1]] == ' ':  # Pawn movement logic
            if vert == valid_double_row:
                if self._board[vert+one_step][hori] != ' ':
                    return False
                if self._next_pos == [vert+one_step*2, hori]:
                    return True
            if self._next_pos == [vert+one_step, hori]:
                return True

        if self._board[self._next_pos[0]][self._next_pos[1]] != ' ':  # Pawn capture logic
            if hori > 0 and self._next_pos == [vert+one_step, hori-1]:
                return True
            if hori < 7 and self._next_pos == [vert+one_step, hori+1]:
                return True
        return False

    def rook(self, vert_direction, hori_direction, vert, hori):
        """Rook helper function containing the logic of a rook chess piece
        Taking the vert_direction, hori_direction, vert and hori parameters from the legal_move function
        Since the rook chess piece has similar logic as the queen chess piece, the queen function is called if
        the vertical/horizontal direction is 0, passing the vert_direction, hori_direction, vert and hori
        returning false otherwise"""
        if vert_direction == 0 or hori_direction == 0:
            return self.queen(vert_direction, hori_direction, vert, hori)
        return False

    def bishop(self, vert_direction, hori_direction, vert, hori):
        """Bishop helper function containing the logic of a bishop chess piece
        Taking the vert_direction, hori_direction, vert and hori parameters from the legal_move function
        Since the bishop chess piece has similar logic as the queen chess piece, the queen function is called if
        the vertical and horizontal direction is not 0, passing the vert_direction, hori_direction, vert and hori
        returning false otherwise"""
        if vert_direction != 0 and hori_direction != 0:
            return self.queen(vert_direction, hori_direction, vert, hori)
        return False

    def knight(self, vert_direction, hori_direction, vert, hori):
        """Knight helper function containing the logic of a knight chess piece
        Taking the vert_direction, hori_direction, vert and hori parameters from the legal_move function
        The vertical and horizontal direction must not be 0"""
        if vert_direction != 0 and hori_direction != 0:
            if [vert+2*vert_direction, hori+1*hori_direction] == self._next_pos:
                return True
            elif [vert+1*vert_direction, hori+2*hori_direction] == self._next_pos:
                return True
            else:
                return False
        else:
            return False

    def queen(self, vert_direction, hori_direction, vert, hori):
        """Queen helper function containing the logic of a queen chess piece
        Taking the vert_direction, hori_direction, vert and hori parameters from either the rook, bishop or legal_move
        functions
        The number of steps are calculated and a for loop is run for the number of steps to see if the path is blocked,
        if the ending position is not equal to the next position then False is returned"""
        steps = abs(self._curr_pos[0] - self._next_pos[0])
        if self._next_pos[0] == self._curr_pos[0]:
            steps = abs(self._curr_pos[1] - self._next_pos[1])

        for index in range(steps-1):
            if self._board[vert + vert_direction][hori + hori_direction] != ' ':
                return False
            vert += vert_direction
            hori += hori_direction
        if [vert + vert_direction, hori + hori_direction] != self._next_pos:
            return False
        else:
            return True

    def king(self, vert_direction, hori_direction, vert, hori):
        """King helper function containing the logic of a king chess piece
        Taking the vert_direction, hori_direction, verr and hori parameters from the legal_move function"""
        if [vert+1*vert_direction, hori+1*hori_direction] == self._next_pos:
            return True
        else:
            return False
