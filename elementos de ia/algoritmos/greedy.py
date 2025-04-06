import sys
import os
import copy
import time
import heapq
from a_star import calculate_grouped_balls_heuristic

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from uteis.movimentos import *
from uteis.check_win import *
               
          
def greedy(initial_board, level, max_iterations=10000):
    start_time = time.perf_counter()
    
    def board_to_tuple(board):
        return tuple(tuple(row) for row in board)
    
    visited = set()
    visited.add(board_to_tuple(initial_board))
    
    # Fila de prioridade (max heap usando valores negativos)
    heap = []
    initial_heuristic = calculate_grouped_balls_heuristic(initial_board)
    heapq.heappush(heap, (initial_heuristic, copy.deepcopy(initial_board), []))
    
    iterations = 0
    
    while heap and iterations < max_iterations:
        heuristic, current_board, path = heapq.heappop(heap)
        current_heuristic = heuristic
        iterations += 1
        
        if check_win(current_board, level):
            elapsed = time.perf_counter() - start_time
            time_dict = {
                'minutes': int(elapsed // 60),
                'seconds': int(elapsed % 60),
                'milliseconds': int((elapsed % 1) * 1000)
            }
            return path, time_dict, len(path)
        
        all_possible = total_possible_moves(current_board, level)
        
        for move_info in all_possible:
            from_shelf, ball, to_shelves = move_info
            for to_shelf in to_shelves:
                new_board = copy.deepcopy(current_board)
                success = move_piece(new_board, from_shelf, to_shelf)
                
                if success:
                    new_state = board_to_tuple(new_board)
                    if new_state not in visited:
                        visited.add(new_state)
                        new_path = path + [(from_shelf, to_shelf)]
                        new_heuristic = calculate_grouped_balls_heuristic(new_board)
                        heapq.heappush(heap, (new_heuristic, new_board, new_path))
    
    # Caso não encontre solução dentro do limite de iterações
    elapsed = time.perf_counter() - start_time
    time_dict = {
        'minutes': int(elapsed // 60),
        'seconds': int(elapsed % 60),
        'milliseconds': int((elapsed % 1) * 1000)
    }
    return None, time_dict, 0

