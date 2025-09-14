# board.py - Defines the Board class for board state

from utils.constants import ROWS, COLS, RED, WHITE
from entities.piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_pieces = self.white_pieces = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def create_board(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

        # Place the pieces
        for row in range(ROWS):
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):  # Checkerboard pattern
                    if row < 3:
                        self.board[row][col] = Piece(row, col, WHITE)
                    elif row > 4:
                        self.board[row][col] = Piece(row, col, RED)

    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def move(self, piece, row, col):
        # Swap positions in the board array
        self.board[piece.row][piece.col], self.board[row][col] = None, self.board[piece.row][piece.col]

        # Update piece position
        piece.move(row, col)

        # Check if piece should be crowned
        if row == 0 and piece.color == RED:
            piece.make_king()
            self.red_kings += 1
        elif row == ROWS - 1 and piece.color == WHITE:
            piece.make_king()
            self.white_kings += 1

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece.color == RED:
                self.red_pieces -= 1
            else:
                self.white_pieces -= 1

    def winner(self):
        if self.red_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # Different move directions based on color and king status
        if piece.color == RED or piece.king:
            # Moving upward (red pieces and kings)
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:
            # Moving downward (white pieces and kings)
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=None):
        if skipped is None:
            skipped = []

        moves = {}
        last = []

        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.get_piece(r, left)
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=None):
        if skipped is None:
            skipped = []

        moves = {}
        last = []

        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.get_piece(r, right)
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves