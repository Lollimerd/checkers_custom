# game.py - Contains game state logic

from utils.constants import RED, WHITE
from .board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.selected_piece = None
        self.red_turn = True
        self.valid_moves = {}

    def update(self):
        # Game state updates that happen each frame
        pass

    def select(self, row, col):
        # If a piece is already selected, try to move it
        if self.selected_piece:
            result = self._move(row, col)
            if not result:
                # If move failed, deselect and try to select a new piece
                self.selected_piece = None
                self.select(row, col)

        # Try to select a piece
        piece = self.board.get_piece(row, col)
        if piece and piece.color == (RED if self.red_turn else WHITE):
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected_piece and (row, col) in self.valid_moves and not piece:
            self.board.move(self.selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            return True

        return False

    def change_turn(self):
        self.valid_moves = {}
        self.selected_piece = None
        self.red_turn = not self.red_turn

    def get_board(self):
        return self.board

    def winner(self):
        return self.board.winner()