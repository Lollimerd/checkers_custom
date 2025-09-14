# piece.py - Defines the Piece class
import pygame
from utils.constants import SQUARE_SIZE, PIECE_PADDING, BLUE


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, window):
        radius = SQUARE_SIZE // 2 - PIECE_PADDING
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            # Draw a crown for kings
            pygame.draw.circle(window, BLUE, (self.x, self.y), radius // 2)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()