# improved_renderer.py - Improved rendering for the game

import pygame
from utils.constants import BLACK, GREY, BLUE, SQUARE_SIZE, ROWS, COLS, WIDTH, HEIGHT, RED, WHITE, INFO_HEIGHT, FONT_SIZE, \
    DARK_GREY, GREEN


class Renderer:
    def __init__(self):
        # Create a window that includes space for the info panel
        self.window = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))
        pygame.display.set_caption('Checkers')
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)
        self.small_font = pygame.font.SysFont('Arial', FONT_SIZE - 8)

    def draw_board(self):
        # Clear the board area (not including info panel)
        pygame.draw.rect(self.window, BLACK, (0, 0, WIDTH, HEIGHT))

        # Draw the checkerboard squares
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.window, GREY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, board):
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece:
                    piece.draw(self.window)

    def draw_valid_moves(self, valid_moves):
        for move in valid_moves:
            row, col = move
            # Draw a more visible indicator for valid moves
            pygame.draw.circle(self.window, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
            pygame.draw.circle(self.window, GREY,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15, 2)

    def draw_info_panel(self, red_turn, red_pieces, white_pieces, status_message=None):
        # Draw background for info panel
        pygame.draw.rect(self.window, DARK_GREY, (0, HEIGHT, WIDTH, INFO_HEIGHT))

        # Draw separator line
        pygame.draw.line(self.window, GREY, (0, HEIGHT), (WIDTH, HEIGHT), 2)

        # Section widths
        left_section_width = WIDTH // 3
        middle_section_width = WIDTH // 3
        right_section_width = WIDTH // 3

        # Draw turn indicator (left section)
        turn_text = f"Turn: {'RED' if red_turn else 'WHITE'}"
        turn_color = RED if red_turn else WHITE
        turn_surface = self.font.render(turn_text, True, turn_color)
        self.window.blit(turn_surface, (20, HEIGHT + 15))

        # Draw piece counts (middle section)
        red_text = f"Red Pieces: {red_pieces}"
        white_text = f"White Pieces: {white_pieces}"

        red_surface = self.font.render(red_text, True, RED)
        white_surface = self.font.render(white_text, True, WHITE)

        # Position the piece counts in the middle section
        red_x = left_section_width + (middle_section_width - red_surface.get_width()) // 2
        white_x = left_section_width + (middle_section_width - white_surface.get_width()) // 2

        self.window.blit(red_surface, (red_x, HEIGHT + 15))
        self.window.blit(white_surface, (white_x, HEIGHT + 50))

        # Highlight the current player's piece count
        if red_turn:
            pygame.draw.rect(self.window, GREEN,
                             (red_x - 5, HEIGHT + 13,
                              red_surface.get_width() + 10, red_surface.get_height() + 4), 2, border_radius=4)
        else:
            pygame.draw.rect(self.window, GREEN,
                             (white_x - 5, HEIGHT + 48,
                              white_surface.get_width() + 10, white_surface.get_height() + 4), 2, border_radius=4)

        # Draw game controls (right section)
        if status_message:
            # Split the message into multiple lines if needed
            words = status_message.split()
            lines = []
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = self.small_font.render(test_line, True, WHITE)

                if test_surface.get_width() < right_section_width - 40:
                    current_line.append(word)
                else:
                    if current_line:  # Don't add empty lines
                        lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:  # Add the last line
                lines.append(' '.join(current_line))

            # Draw each line
            for i, line in enumerate(lines):
                status_surface = self.small_font.render(line, True, WHITE)
                self.window.blit(status_surface, (2 * left_section_width + 20, HEIGHT + 15 + i * 25))

    def update_display(self):
        pygame.display.update()