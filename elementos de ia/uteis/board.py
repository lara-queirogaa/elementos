import random
import numpy as np

def create_board(level):
    if level == 1:
        #lista c todos os numeros
        numbers = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    
        #shuffle
        random.shuffle(numbers)
    
        #4x4
        matrix = np.zeros((6, 4), dtype=int)
        matrix[:4, :] = np.array(numbers).reshape(4, 4)
    
    elif level == 2:
        numbers = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]
        random.shuffle(numbers)
        matrix = np.zeros((7, 4), dtype=int)
        matrix[:5, :] = np.array(numbers).reshape(5, 4)

    elif level == 3:
        numbers = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]
        random.shuffle(numbers)
        matrix = np.zeros((8, 4), dtype=int)
        matrix[:6, :] = np.array(numbers).reshape(6, 4)

    return matrix

def print_board(board, level):
    print("\nEstado atual do jogo:")
    for i, shelf in enumerate(board):
        shelf_content = [str(ball) if ball != 0 else '0' for ball in shelf]
        print(f"Prateleira {i}: {' '.join(shelf_content)}")
