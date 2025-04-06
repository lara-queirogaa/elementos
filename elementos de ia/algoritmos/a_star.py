import sys
import os
import copy
import time
import heapq
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from uteis.movimentos import *
from uteis.check_win import *

def calculate_grouped_balls_heuristic(board):
    """
    Heurística que conta o número total de bolas do mesmo tipo que estão adjacentes.
    Quanto maior o numero de bolas agrupadas, melhor o estado do tabuleiro.
    Para usar na função a_star é retornado este valor mas negativo.
    """
    grouped_balls = 0
    
    for shelf in board:
        if sum(shelf) == 0:  # Prateleira vazia
            continue
        
        current_ball = None
        current_count = 0
        
        for ball in shelf:
            if ball == 0:  # Ignorar espaços vazios
                continue
                
            if ball == current_ball:
                current_count += 1
            else:
                if current_count > 1:
                    grouped_balls += current_count
                current_ball = ball
                current_count = 1
        
        # Adicionar o último grupo da prateleira
        if current_count > 1:
            grouped_balls += current_count
    
    return -grouped_balls

def a_star_solution(initial_board, level, max_iterations=1000000):
    start_time = time.perf_counter()

    # Convert board to a more efficient representation
    def board_to_tuple(board):
        return tuple(tuple(row) for row in board)
    
    # Priority queue: (f_score, g_score, board_tuple, path)
    heap = []
    
    # Initial state
    initial_tuple = board_to_tuple(initial_board)
    initial_h = calculate_grouped_balls_heuristic(initial_board)
    heapq.heappush(heap, (initial_h, 0, initial_tuple, []))
    
    # Visited dictionary with the best g_score for each state
    visited = {initial_tuple: 0}
    
    # To detect and skip duplicate states more efficiently
    seen_states = set()
    seen_states.add(initial_tuple)
    
    iterations = 0
    solution_found = False
    solution_path = None
    
    # Pre-calculate the win condition board structure for early checking
    target_balls_per_shelf = len(initial_board[0]) if level == 1 else (len(initial_board[0]) - 1 if level == 2 else len(initial_board[0]))
    
    while heap and iterations < max_iterations and not solution_found:
        current_f, current_g, current_tuple, path = heapq.heappop(heap)
        current_board = np.array(current_tuple)
        
        # Early win check - before expanding nodes
        if check_win(current_board, level):
            solution_path = path
            solution_found = True
            break
        
        # Get all possible moves
        all_possible = total_possible_moves(current_board, level)
        
        for move_info in all_possible:
            from_shelf, ball, to_shelves = move_info
            for to_shelf in to_shelves:
                # Create new board state
                new_board = np.array(current_tuple)
                if move_piece(new_board, from_shelf, to_shelf):
                    new_tuple = board_to_tuple(new_board)
                    
                    # Skip if we've seen this state with better or equal g_score
                    if new_tuple in visited and visited[new_tuple] <= current_g + 1:
                        continue
                    
                    # Calculate heuristic and f_score
                    new_h = calculate_grouped_balls_heuristic(new_board)
                    new_g = current_g + 1
                    new_f = new_g + new_h
                    
                    # Add to priority queue
                    heapq.heappush(heap, (new_f, new_g, new_tuple, path + [(from_shelf, to_shelf)]))
                    
                    # Update visited and seen states
                    visited[new_tuple] = new_g
                    seen_states.add(new_tuple)
        
        iterations += 1
        
    
    elapsed = time.perf_counter() - start_time
    time_dict = {
        'minutes': int(elapsed // 60),
        'seconds': int(elapsed % 60),
        'milliseconds': int((elapsed % 1) * 1000)
    }
    
    if solution_found:
        return solution_path, time_dict, len(solution_path)
    else:
        print(f"Failed to find solution after {iterations} iterations")
        return None, time_dict, 0
    
