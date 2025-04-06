import numpy as np
from uteis.board import *
from uteis.movimentos import valid_move, select_piece, move_piece
from uteis.check_win import *

    
def get_user_move():
    while True:
        try:
            move = input("\nEscreva a jogada (prateleira_inicial prateleira_final) ou q para desistir: ")
            if move.lower() == 'q':
                return None, None
            
            initial, final = map(int, move.split())
            return initial, final
        except ValueError:
            print("\nInválido: Escreva as duas prateleiras separadas por um espaço. ")


def main():
    
    while True:

        # Level selection
        level = input("Escolha um nivel (1-3) ou 'q' para desistir: ")
        if level.lower() == 'q':
            break
        
        try:
            level = int(level)
            if level not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print("\nApenas 1, 2, ou 3")
            continue
        
        # Create board
        board = create_board(level)
        moves = 0
        
        # Game loop
        while True:
            
            print_board(board, level)
            
            # Check win condition
            if check_win(board, level):
                print("\nGanhou!")
                break
            
            # Get user move
            initial_shelf, final_shelf = get_user_move()
            if initial_shelf is None:
                break
            
            # Validate shelf numbers
            max_shelf = 5 if level == 1 else 6 if level == 2 else 7
            if initial_shelf < 0 or initial_shelf > max_shelf or final_shelf < 0 or final_shelf > max_shelf:
                print(f"\nPrateleira inválida. Tem que estar entre 0 e {max_shelf}.")
                continue
            
            # Try to make the move
            if move_piece(board, initial_shelf, final_shelf):
                moves += 1
        



if __name__ == "__main__":
    main()