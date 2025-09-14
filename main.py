# improved_main.py - Improved main file with better UI integration

import pygame, sys, time
from utils.constants import SQUARE_SIZE, RED, WHITE, HEIGHT, WIDTH
from components.game import Game
from components.renderer import Renderer
from ai_player import AI
from components.menu import Menu
from utils.stats import StatsTracker


def main():
    pygame.init()

    # Create stats tracker
    stats = StatsTracker()

    # Game loop
    running_game = True

    while running_game:
        # Show the menu first
        menu = Menu()
        play_against_ai, ai_color, ai_difficulty = menu.show_menu()

        # Exit if menu was closed
        if play_against_ai is None:
            running_game = False
            break

        # Initialize the game
        game = Game()
        renderer = Renderer()
        clock = pygame.time.Clock()
        running = True

        # Initialize AI if playing against it
        ai = AI(ai_color, ai_difficulty) if play_against_ai else None

        # Player color (opposite of AI color)
        player_color = WHITE if ai_color == RED else RED if play_against_ai else None

        # Track if the AI is currently thinking
        ai_thinking = False

        # Flag to show stats after game
        show_stats = False
        game_winner = None

        # Game mode description for info panel
        if play_against_ai:
            game_mode = f"Playing against AI (Level {ai_difficulty}). You are {'RED' if player_color == RED else 'WHITE'}."
            controls = "Press 1-5 to change difficulty. ESC to restart. S for stats."
        else:
            game_mode = "Two Player Mode"
            controls = "Press ESC to restart. S for stats."

        # Main game loop
        while running:
            clock.tick(60)

            # Check if it's AI's turn
            if play_against_ai and ((game.red_turn and ai.color == RED) or
                                    (not game.red_turn and ai.color == WHITE)):
                if not ai_thinking:
                    # Start AI thinking (visual indicator could be added here)
                    ai_thinking = True
                    # Draw "AI Thinking..." message
                    renderer.draw_board()
                    renderer.draw_valid_moves(game.valid_moves)
                    renderer.draw_pieces(game.board)
                    board = game.get_board()
                    renderer.draw_info_panel(
                        game.red_turn,
                        board.red_pieces,
                        board.white_pieces,
                        f"{game_mode} AI is thinking..."
                    )
                    renderer.update_display()

                    # Add a small delay to make the AI's move visible
                    pygame.time.delay(800 - ai_difficulty * 100)  # Faster delay at higher difficulties

                    # Get the AI's move
                    ai_move = ai.get_move(game)

                    if ai_move:
                        piece, move = ai_move
                        # Select the piece (this will load valid moves)
                        game.select(piece.row, piece.col)
                        # Make the move
                        game.select(move[0], move[1])

                    ai_thinking = False

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    running_game = False

                if event.type == pygame.KEYDOWN:
                    # Change AI difficulty with number keys 1-5
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                        if play_against_ai:
                            new_difficulty = int(event.unicode)
                            ai.set_difficulty(new_difficulty)
                            ai_difficulty = new_difficulty
                            game_mode = f"Playing against AI (Level {ai_difficulty}). You are {'RED' if player_color == RED else 'WHITE'}."
                    # Restart game with ESC key
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    # Show stats with S key
                    elif event.key == pygame.K_s:
                        show_stats = True

                # Handle clicks (only when it's the player's turn)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not play_against_ai or (
                            (game.red_turn and ai.color != RED) or
                            (not game.red_turn and ai.color != WHITE)):

                        pos = pygame.mouse.get_pos()
                        # Only register clicks on the board area, not the info panel
                        if pos[1] < HEIGHT:
                            col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                            game.select(row, col)

            # Draw everything
            renderer.draw_board()
            renderer.draw_valid_moves(game.valid_moves)
            renderer.draw_pieces(game.board)

            # Draw the info panel with current game state
            board = game.get_board()

            # Display appropriate status message
            status_message = f"{game_mode} {controls}"

            renderer.draw_info_panel(
                game.red_turn,
                board.red_pieces,
                board.white_pieces,
                status_message
            )

            # Check for the winner
            winner = game.winner()
            if winner:
                game_winner = winner
                # Create a win message
                font = pygame.font.SysFont('Arial', 50)
                win_text = f"{'RED' if winner == RED else 'WHITE'} WINS!"
                win_color = winner
                win_surface = font.render(win_text, True, win_color)

                # Display a win message in the center of the board
                win_rect = win_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                renderer.window.blit(win_surface, win_rect)

                # Display a restart message
                restart_font = pygame.font.SysFont('Arial', 30)
                restart_text = "Press ESC to play again or S for stats"
                restart_surface = restart_font.render(restart_text, True, WHITE)
                restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
                renderer.window.blit(restart_surface, restart_rect)

                # Record the win in stats
                stats.record_win(winner)

                # Update display to show a win message
                renderer.update_display()

                # Wait for key press to continue
                waiting_for_key = True
                while waiting_for_key:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            running_game = False
                            waiting_for_key = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_s:
                                show_stats = True
                                waiting_for_key = False
                            elif event.key == pygame.K_ESCAPE:
                                waiting_for_key = False
                    clock.tick(30)

                # End the current game loop
                running = False

            # Draw stats if requested
            if show_stats:
                stats.draw_stats(renderer.window, pygame.font.SysFont('Arial', 30))
                renderer.update_display()

                # Wait for a key press to continue
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            running_game = False
                            waiting = False
                        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                            waiting = False
                            show_stats = False

            # Update display
            renderer.update_display()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()