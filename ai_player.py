# ai_player.py - AI player using minimax with alpha-beta pruning

import random
from copy import deepcopy
from utils.constants import RED, WHITE


class AI:
    def __init__(self, color, difficulty=2):
        """
        Initialize the AI player.

        Parameters:
            color: RED or WHITE constant indicating the AI's color
            difficulty: Integer from 1-5 representing the AI's difficulty level
                1: Very Easy (depth 1, random moves sometimes)
                2: Easy (depth 2)
                3: Medium (depth 3)
                4: Hard (depth 4)
                5: Very Hard (depth 5)
        """
        self.color = color
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        """Set the AI difficulty level (1-5)"""
        self.difficulty = max(1, min(5, difficulty))  # Clamp between 1-5

        # Set the depth of the minimax search based on difficulty
        self.depth = self.difficulty

        # At very easy, we'll make some random moves
        self.random_move_chance = 0.3 if self.difficulty == 1 else 0

    def get_move(self, game):
        """
        Determine the best move for the AI to make.
        Parameters:
            game: The current Game object
        Returns:
            tuple: (piece, move) where piece is the Piece to move and move is the (row, col) to move to
        """
        # Make a deep copy of the board to avoid modifying the actual game
        board = deepcopy(game.board)

        # Check if we should make a random move (for very easy difficulty)
        if self.difficulty == 1 and random.random() < self.random_move_chance:
            return self.get_random_move(game)

        # Get all possible pieces that can be moved
        valid_pieces = []
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece(row, col)
                if piece and piece.color == self.color:
                    moves = board.get_valid_moves(piece)
                    if moves:
                        valid_pieces.append((piece, moves))

        if not valid_pieces:
            return None

        # Find the best move using minimax with alpha-beta pruning
        best_value = float('-inf') if self.color == RED else float('inf')
        best_move = None

        # Sort moves to improve alpha-beta pruning effectiveness
        # For capturing moves, try them first
        for piece, moves in valid_pieces:
            # Sort moves by number of pieces captured (try jumps first)
            sorted_moves = sorted(moves.items(),
                                  key=lambda x: len(x[1]),
                                  reverse=True)

            for move, skipped in sorted_moves:
                # Create a simulation board
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)

                # Simulate the move
                temp_board.move(temp_piece, move[0], move[1])
                if skipped:
                    temp_board.remove(skipped)

                # Use minimax to evaluate this move
                value = self.minimax(temp_board, self.depth - 1, float('-inf'), float('inf'), self.color != RED)

                # Update best move if needed
                if (self.color == RED and value > best_value) or (self.color == WHITE and value < best_value):
                    best_value = value

                    # Store the actual game piece and move, not the temp ones
                    best_move = (game.board.get_piece(piece.row, piece.col), move)

        return best_move

    def get_random_move(self, game):
        """Get a random valid move for the AI (used for very easy difficulty)"""
        board = game.board
        valid_moves = []

        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece(row, col)
                if piece and piece.color == self.color:
                    moves = board.get_valid_moves(piece)
                    for move in moves:
                        valid_moves.append((piece, move))

        if valid_moves:
            return random.choice(valid_moves)
        return None

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning to find the best move.
        Parameters:
            board: Board object representing current state
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: Boolean indicating if maximizing (RED) or minimizing (WHITE)
        Returns:
            float: The evaluated score of the board position
        """
        # Check for terminal state or maximum depth
        winner = board.winner()
        if winner == RED:
            return 1000  # RED wins
        elif winner == WHITE:
            return -1000  # WHITE wins
        elif depth == 0:
            return self.evaluate_board(board)

        # Get all possible moves for the current player
        current_color = RED if is_maximizing else WHITE
        max_value = float('-inf') if is_maximizing else float('inf')

        # Find all pieces that can move
        valid_pieces = []
        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece(row, col)
                if piece and piece.color == current_color:
                    moves = board.get_valid_moves(piece)
                    if moves:
                        # Sort moves with jumps first to improve pruning
                        sorted_moves = sorted(moves.items(),
                                              key=lambda x: len(x[1]),
                                              reverse=True)
                        valid_pieces.append((piece, sorted_moves))

        # If no valid moves, it's a draw (or the other player wins in checkers)
        if not valid_pieces:
            return 0 if is_maximizing else 0

        for piece, moves in valid_pieces:
            for move, skipped in moves:
                # Create a simulation board
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)

                # Simulate the move
                temp_board.move(temp_piece, move[0], move[1])
                if skipped:
                    temp_board.remove(skipped)

                # Recursively evaluate this position
                value = self.minimax(temp_board, depth - 1, alpha, beta, not is_maximizing)

                # Update value based on min/max
                if is_maximizing:
                    max_value = max(max_value, value)
                    alpha = max(alpha, max_value)
                else:
                    max_value = min(max_value, value)
                    beta = min(beta, max_value)

                # Alpha-beta pruning
                if beta <= alpha:
                    break

            # If we've pruned, no need to check other pieces
            if beta <= alpha:
                break

        return max_value

    def evaluate_board(self, board):
        """
        Evaluate the current board state and return a score.
        Positive scores favor RED, negative scores favor WHITE.

        This heuristic considers:
        1. Material advantage (piece count)
        2. King advantage (kings are worth more)
        3. Position advantage (pieces closer to becoming kings)
        4. Center control
        """
        red_score = 0
        white_score = 0

        for row in range(len(board.board)):
            for col in range(len(board.board[row])):
                piece = board.get_piece(row, col)
                if piece:
                    # Base piece value
                    piece_value = 10

                    # Kings are worth more
                    if piece.king:
                        piece_value = 15

                    # Pieces closer to becoming kings are worth more
                    elif piece.color == RED and row < 3:
                        piece_value += 3 - row  # 0-2 bonus based on proximity to king row
                    elif piece.color == WHITE and row > 4:
                        piece_value += row - 4  # 1-3 bonus based on proximity to king row

                    # Center control bonus (pieces in the center 4x4 area)
                    if 2 <= row <= 5 and 2 <= col <= 5:
                        piece_value += 1

                    # Add to appropriate score
                    if piece.color == RED:
                        red_score += piece_value
                    else:
                        white_score += piece_value

        # Return the difference (positive favors RED, negative favors WHITE)
        return red_score - white_score