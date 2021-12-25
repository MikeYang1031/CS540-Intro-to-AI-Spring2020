"""
    File name: teeko_player.py
    Author: Zonglin Yang
    Project: P6 Game AI
    course: cs540 Spring2020
    credit: Piazza
"""
import random
from copy import deepcopy
from collections import Counter

INF = float('inf')


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.MAX_DEPTH = 2

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        count = 0
        # check for the drop state
        for row in state:
            for cell in row:
                if cell == self.my_piece:
                    count += 1
        drop_phase = count < 4

        if not drop_phase:
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            return self.minimax(state)

        return self.minimax(state)
        # # select an unoccupied space randomly
        # move = []
        # (row, col) = (random.randint(0,4), random.randint(0,4))
        # while not state[row][col] == ' ':
        #     (row, col) = (random.randint(0,4), random.randint(0,4))
        #
        # # ensure the destination (row,col) tuple is at the beginning of the move list
        # move.insert(0, (row, col))
        # return move

    def evaluate(self, state):
        # check horizontal wins
        total = 0
        scores = []
        for row in state:
            for i in range(2):
                line = [row[i], row[i + 1], row[i + 2], row[i + 3]]
                scores.append(self.check(line))

        # check vertical wins
        for col in range(5):
            for i in range(2):
                line = [state[i][col], state[i + 1][col], state[i + 2][col], state[i + 3][col]]
                scores.append(self.check(line))

        # check \ diagonal wins
        points = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for p in points:
            i, j = p
            line = [state[i][j], state[i + 1][j + 1], state[i + 2][j + 2], state[i + 3][j + 3]]
            scores.append(self.check(line))

        # check / diagonal wins
        points = [(0, 4), (0, 3), (1, 4), (1, 3)]
        for p in points:
            i, j = p
            line = [state[i][j], state[i + 1][j - 1], state[i + 2][j - 2], state[i + 3][j - 3]]
            scores.append(self.check(line))

        # check 2x2 box wins
        for i in range(4):
            for j in range(4):
                line = [state[i][j], state[i + 1][j], state[i][j + 1], state[i + 1][j + 1]]
                scores.append(self.check(line))

        return sum(scores)

    def check(self, line):
        c = Counter(line)
        my_num = c.get(self.my_piece, 0)
        opp_num = c.get(self.opp, 0)
        if my_num == 0 and opp_num > 0:
            return -4 ** opp_num
        if opp_num == 0 and my_num > 0:
            return 4 ** my_num
        return 0

    def max_value(self, state, depth):
        res = self.game_value(state)
        if res != 0:
            return res * INF
        if depth == self.MAX_DEPTH:
            return self.evaluate(state)

        actions = self.possible_actions(state, self.my_piece)
        values = [self.min_value(self.make_new_apply(state, a, self.my_piece), depth + 1) for a in actions]
        return max(values)

    def min_value(self, state, depth):
        res = self.game_value(state)
        if res != 0:
            return res * INF
        if depth == self.MAX_DEPTH:
            return self.evaluate(state)

        actions = self.possible_actions(state, self.opp)
        values = [self.max_value(self.make_new_apply(state, a, self.opp), depth + 1) for a in actions]
        return min(values)

    def minimax(self, state):
        actions = self.possible_actions(state, self.my_piece)
        return max(actions, key=lambda a: self.min_value(self.make_new_apply(state, a, self.my_piece), 0))

    def make_new_apply(self, state, move, piece):
        p = deepcopy(self)
        p.board = deepcopy(state)  # get the copy of the board without modify the previous one
        p.place_piece(move, piece)  # the next piece
        return p.board

    def possible_actions(self, state, piece):

        count = 0
        for row in state:
            for cell in row:
                if cell == piece:
                    count += 1
        drop_phase = count < 4

        moves = []
        if drop_phase:
            for r, row in enumerate(state):
                for c, cell in enumerate(row):
                    if cell == ' ':
                        moves.append([(r, c)])  # find empty space
        else:
            for r, row in enumerate(state):
                for c, cell in enumerate(row):
                    if cell == piece:
                        for rr in [-1, 0, 1]:
                            for cc in [-1, 0, 1]:
                                nr, nc = r + rr, c + cc  # check all the neighbor
                                if 0 <= nr < 5 and 0 <= nc < 5:
                                    if r == nr and c == nc:  # if on myself then continue
                                        continue
                                    if state[nr][nc] == ' ': # if neighbor empty then use it
                                        moves.append([(nr, nc), (r, c)])
        return moves

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        points = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for p in points:
            i, j = p
            if state[i][j] != ' ' and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == state[i + 3][j + 3]:
                return 1 if state[i][j] == self.my_piece else -1

        # check / diagonal wins
        points = [(0, 4), (0, 3), (1, 4), (1, 3)]
        for p in points:
            i, j = p
            if state[i][j] != ' ' and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == state[i + 3][j - 3]:
                return 1 if state[i][j] == self.my_piece else -1

        # check 2x2 box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j] == state[i][j + 1] == state[i + 1][j + 1]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
