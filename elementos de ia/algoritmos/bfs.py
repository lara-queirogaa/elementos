import sys
import os
from collections import deque
import copy
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from uteis.movimentos import *
from uteis.check_win import *

def bfs_solution(initial_board, level):
    """
    Returns a tuple containing:
    - solution_path (list of moves or None)
    - time_dict (dictionary with minutes, seconds, milliseconds)
    - move_count (number of moves in solution)
    """
    start_time = time.perf_counter()
    
    # Initialize BFS
    queue = deque()
    queue.append((copy.deepcopy(initial_board), []))
    visited = set()
    
    def board_to_tuple(board):
        return tuple(tuple(row) for row in board)
    
    visited.add(board_to_tuple(initial_board))
    
    # BFS main loop
    while queue:
        current_board, path = queue.popleft()
        
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
                        queue.append((new_board, new_path))
    
    # If no solution found
    elapsed = time.perf_counter() - start_time
    time_dict = {
        'minutes': int(elapsed // 60),
        'seconds': int(elapsed % 60),
        'milliseconds': int((elapsed % 1) * 1000)
    }
    return None, time_dict, 0


