def valid_move(board, prateleira_inicial, prateleira_final, bola):
    válido = True

    #ver se estamos a escolher uma prateleira c bolas
    if sum(board[prateleira_inicial]) == 0:  
        válido = False
        return válido

    #ver se estamos a mover para ua prateleira vazia ou para a frente de uma bola igual
    if sum(board[prateleira_final]) != 0:
        for i in range(3,-1,-1):
            if board[prateleira_final][i] == 0:
                continue
            else:
                if 0 not in board[prateleira_final]:
                    válido = False
                if board[prateleira_final][i] != bola:
                    válido = False
                break 

    return válido


    
def select_piece(board, prateleira_inicial, bola):
    válido1 = True
    bola = None

    for i in range(3, -1, -1):
        if board[prateleira_inicial][i] == 0:
            pass
        else:
            bola = board[prateleira_inicial][i]
            return bola, válido1
    
    válido1 = False
    return None, válido1

def possible_moves(board, prateleira_inicial, bola, level):
    moves = []
    
    if level == 1:
        #for i in range(0,len(board)):
        for i in range(0,6):
            if i == prateleira_inicial:
                pass
            else:
                if sum(board[i]) == 0:
                    moves.append(i)
                else:
                    if 0 in board[i]:
                        for j in range(3, -1, -1):
                            if board[i][j] != 0:
                                if board[i][j] == bola:
                                    moves.append(i)
                                break

    elif level == 2:
        for i in range(0,7):
            if i == prateleira_inicial:
                pass
            else:
                if sum(board[i]) == 0:
                    moves.append(i)
                else:
                    if 0 in board[i]:
                        for j in range(3, -1, -1):
                            if board[i][j] != 0:
                                if board[i][j] == bola:
                                    moves.append(i)
                                break

    elif level == 3:
        for i in range(0,8):
            if i == prateleira_inicial:
                pass
            else:
                if sum(board[i]) == 0:
                    moves.append(i)
                else:
                    if 0 in board[i]:
                        for j in range(3, -1, -1):
                            if board[i][j] != 0:
                                if board[i][j] == bola:
                                    moves.append(i)
                                break
        
    return moves

def total_possible_moves(board, level):
    moves_totais = []
    
    # Iterar sobre todas as prateleiras
    for prateleira_inicial in range(len(board)):
        # Procurar pela bola mais à direita na prateleira
        for j in range(3, -1, -1):  
            if board[prateleira_inicial][j] != 0:
                bola = board[prateleira_inicial][j]
                # Para a bola mais à direita encontrada, buscar os movimentos possíveis
                moves = possible_moves(board, prateleira_inicial, bola, level)
                if moves:
                    moves_totais.append((prateleira_inicial, bola, moves))
                break  # Uma vez que encontramos a bola mais à direita, podemos parar
        
    return moves_totais


def move_piece(board, prateleira_inicial, prateleira_final):
    bola, valid_selection = select_piece(board, prateleira_inicial, None)
    
    if not valid_selection or bola is None:
        print("\nInválido: Prateleira sem bolas")
        return False
    
    if not valid_move(board, prateleira_inicial, prateleira_final, bola):
        print("\nInválido: Não se pode colocar a bola aí")
        return False
    
    for i in range(3, -1, -1):
        if board[prateleira_inicial][i] != 0:
            board[prateleira_inicial][i] = 0  
            break
      
    for i in range(4):  
        if board[prateleira_final][i] == 0:
            board[prateleira_final][i] = bola
            break
    
    return True


