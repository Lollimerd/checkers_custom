# improved_menu.py - Provides an improved menu system for the game

import pygame
from utils.constants import WIDTH, HEIGHT, RED, WHITE, BLACK, GREY, GREEN, BLUE, DARK_GREY


class Menu:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Checkers - Game Setup')
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 32)
        self.font_small = pygame.font.SysFont('Arial', 24)

    def draw_button(self, rect, text, text_color, button_color, hover=False, selected=False):
        # Draw the button
        pygame.draw.rect(self.window, button_color, rect, border_radius=8)

        # Draw a highlight border for selected or hover effect
        if selected:
            pygame.draw.rect(self.window, GREEN, rect, 3, border_radius=8)
        elif hover:
            pygame.draw.rect(self.window, BLUE, rect, 2, border_radius=8)

        # Render the text
        text_surface = self.font_medium.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.window.blit(text_surface, text_rect)

    def show_menu(self):
        """Display the main menu and return the selected options"""
        # Default settings
        play_against_ai = True
        ai_color = WHITE  # Default AI is WHITE (player is RED)
        ai_difficulty = 3

        # Calculate layout dimensions
        margin = 20
        button_height = 60
        button_width = WIDTH // 3
        section_height = button_height + 70  # Section title + button

        # Define title area (top 15% of screen)
        title_area = pygame.Rect(0, HEIGHT * 0.05, WIDTH, HEIGHT * 0.15)

        # Define sections (evenly spaced in remaining 85%)
        # Each section takes about 20% of the screen height
        opponent_section_y = title_area.bottom + margin
        color_section_y = opponent_section_y + section_height + margin
        difficulty_section_y = color_section_y + section_height + margin
        start_button_y = difficulty_section_y + section_height + margin * 2

        # Opponent selection buttons
        opponent_label_pos = (WIDTH // 2, opponent_section_y)
        ai_button = pygame.Rect(WIDTH // 2 - button_width - margin // 2, opponent_section_y + 40, button_width,
                                button_height)
        human_button = pygame.Rect(WIDTH // 2 + margin // 2, opponent_section_y + 40, button_width, button_height)

        # Color selection buttons
        color_label_pos = (WIDTH // 2, color_section_y)
        red_button = pygame.Rect(WIDTH // 2 - button_width - margin // 2, color_section_y + 40, button_width,
                                 button_height)
        white_button = pygame.Rect(WIDTH // 2 + margin // 2, color_section_y + 40, button_width, button_height)

        # Difficulty selection buttons (5 smaller buttons)
        difficulty_label_pos = (WIDTH // 2, difficulty_section_y)
        diff_button_width = (WIDTH - (margin * 6)) // 5
        difficulty_buttons = []
        for i in range(5):
            difficulty_buttons.append(pygame.Rect(
                margin + i * (diff_button_width + margin),
                difficulty_section_y + 40,
                diff_button_width,
                button_height
            ))

        # Difficulty labels
        difficulty_labels = ["Very Easy", "Easy", "Medium", "Hard", "Very Hard"]

        # Start game button (centered, wider)
        start_button = pygame.Rect(WIDTH // 2 - button_width, start_button_y, button_width * 2, button_height)

        menu_active = True
        clock = pygame.time.Clock()

        while menu_active:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None, None  # Return None to exit game

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check opponent buttons
                    if ai_button.collidepoint(mouse_pos):
                        play_against_ai = True
                    elif human_button.collidepoint(mouse_pos):
                        play_against_ai = False

                    # Check color buttons (if AI opponent)
                    if play_against_ai:
                        if red_button.collidepoint(mouse_pos):
                            ai_color = WHITE  # Player is RED, AI is WHITE
                        elif white_button.collidepoint(mouse_pos):
                            ai_color = RED  # Player is WHITE, AI is RED

                        # Check difficulty buttons
                        for i, button in enumerate(difficulty_buttons):
                            if button.collidepoint(mouse_pos):
                                ai_difficulty = i + 1

                    # Check start button
                    if start_button.collidepoint(mouse_pos):
                        menu_active = False
                        return play_against_ai, ai_color, ai_difficulty

            # Clear screen with a dark background
            self.window.fill((30, 30, 30))

            # Get mouse position for hover effects
            mouse_pos = pygame.mouse.get_pos()

            # Draw title
            title_text = self.font_large.render("CHECKERS GAME SETUP", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, title_area.centery))
            self.window.blit(title_text, title_rect)

            # Draw separator line
            pygame.draw.line(self.window, GREY, (margin, title_area.bottom), (WIDTH - margin, title_area.bottom), 2)

            # Draw opponent selection section
            opponent_text = self.font_medium.render("Select Opponent:", True, WHITE)
            opponent_rect = opponent_text.get_rect(center=opponent_label_pos)
            self.window.blit(opponent_text, opponent_rect)

            self.draw_button(
                ai_button,
                "Computer AI",
                BLACK,
                GREEN if play_against_ai else GREY,
                ai_button.collidepoint(mouse_pos),
                play_against_ai
            )

            self.draw_button(
                human_button,
                "Human Player",
                BLACK,
                GREEN if not play_against_ai else GREY,
                human_button.collidepoint(mouse_pos),
                not play_against_ai
            )

            # Draw color and difficulty selection if AI opponent
            if play_against_ai:
                # Draw color selection section
                color_text = self.font_medium.render("You Play As:", True, WHITE)
                color_rect = color_text.get_rect(center=color_label_pos)
                self.window.blit(color_text, color_rect)

                self.draw_button(
                    red_button,
                    "Red",
                    BLACK,
                    RED,
                    red_button.collidepoint(mouse_pos),
                    ai_color == WHITE  # Player is red when AI is white
                )

                self.draw_button(
                    white_button,
                    "White",
                    BLACK,
                    WHITE,
                    white_button.collidepoint(mouse_pos),
                    ai_color == RED  # Player is white when AI is red
                )

                # Draw difficulty selection section
                diff_text = self.font_medium.render("AI Difficulty Level:", True, WHITE)
                diff_rect = diff_text.get_rect(center=difficulty_label_pos)
                self.window.blit(diff_text, diff_rect)

                for i, button in enumerate(difficulty_buttons):
                    self.draw_button(
                        button,
                        f"{i + 1}",
                        BLACK,
                        BLUE if ai_difficulty == i + 1 else GREY,
                        button.collidepoint(mouse_pos),
                        ai_difficulty == i + 1
                    )

                # Draw difficulty labels
                for i, label in enumerate(difficulty_labels):
                    label_surface = self.font_small.render(label, True, WHITE)
                    label_rect = label_surface.get_rect(
                        centerx=difficulty_buttons[i].centerx,
                        top=difficulty_buttons[i].bottom + 5
                    )
                    self.window.blit(label_surface, label_rect)

            # Draw start button
            self.draw_button(
                start_button,
                "Start Game",
                BLACK,
                GREEN,
                start_button.collidepoint(mouse_pos)
            )

            pygame.display.update()
            clock.tick(60)

        # Default return if something goes wrong
        return play_against_ai, ai_color, ai_difficulty