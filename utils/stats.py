# stats.py - Track and display game statistics

import pygame
from utils.constants import RED, WHITE, DARK_GREY, WIDTH, HEIGHT


class StatsTracker:
    def __init__(self):
        """Initialize the statistics tracker"""
        self.stats = {
            RED: {"wins": 0, "losses": 0},
            WHITE: {"wins": 0, "losses": 0},
        }
        self.draws = 0
        self.games_played = 0

    def record_win(self, winner_color):
        """Record a win for the given color"""
        if winner_color is None:
            # It's a draw
            self.draws += 1
        else:
            # Record win for winner and loss for loser
            loser_color = WHITE if winner_color == RED else RED
            self.stats[winner_color]["wins"] += 1
            self.stats[loser_color]["losses"] += 1

        self.games_played += 1

    def reset(self):
        """Reset all statistics"""
        for color in self.stats:
            self.stats[color]["wins"] = 0
            self.stats[color]["losses"] = 0
        self.draws = 0
        self.games_played = 0

    def draw_stats(self, window, font):
        """Draw statistics on the given window"""
        # Create background
        stats_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(window, DARK_GREY, stats_rect)
        pygame.draw.rect(window, WHITE, stats_rect, 2)

        # Draw title
        title_text = font.render("Game Statistics", True, WHITE)
        title_rect = title_text.get_rect(centerx=WIDTH // 2, top=HEIGHT // 4 + 20)
        window.blit(title_text, title_rect)

        # Draw stats for each color
        y_offset = HEIGHT // 4 + 80

        # Draw red stats
        red_wins_text = font.render(f"Red Wins: {self.stats[RED]['wins']}", True, RED)
        red_losses_text = font.render(f"Red Losses: {self.stats[RED]['losses']}", True, RED)

        window.blit(red_wins_text, (WIDTH // 3, y_offset))
        window.blit(red_losses_text, (WIDTH // 3, y_offset + 40))

        # Draw white stats
        white_wins_text = font.render(f"White Wins: {self.stats[WHITE]['wins']}", True, WHITE)
        white_losses_text = font.render(f"White Losses: {self.stats[WHITE]['losses']}", True, WHITE)

        window.blit(white_wins_text, (WIDTH // 3, y_offset + 80))
        window.blit(white_losses_text, (WIDTH // 3, y_offset + 120))

        # Draw draws and total
        draws_text = font.render(f"Draws: {self.draws}", True, WHITE)
        total_text = font.render(f"Total Games: {self.games_played}", True, WHITE)

        window.blit(draws_text, (WIDTH // 3, y_offset + 160))
        window.blit(total_text, (WIDTH // 3, y_offset + 200))

        # Draw close prompt
        close_text = font.render("Press any key to continue", True, WHITE)
        close_rect = close_text.get_rect(centerx=WIDTH // 2, bottom=HEIGHT // 4 + HEIGHT // 2 - 20)
        window.blit(close_text, close_rect)