def check_win(board, level):
    win = False
    if level == 1:
        prateleiras = 0
        for i in range(0,6):
            bolas = 1
            if sum(board[i]) == 0:
                continue
            else:
                for j in range(1,4):
                    if board[i][j] == board [i][j-1]:
                        bolas += 1
                if bolas == 4:
                    prateleiras += 1
        if prateleiras == 4:
            win = True

    elif level == 2:
        prateleiras = 0
        for i in range(0,7):
            bolas = 1
            if sum(board[i]) == 0:
                continue
            else:
                for j in range(1,4):
                    if board[i][j] == board [i][j-1]:
                        bolas += 1
                if bolas == 4:
                    prateleiras += 1
        if prateleiras == 5:
            win = True        

    elif level == 3:
        prateleiras = 0
        for i in range(0,8):
            bolas = 1
            if sum(board[i]) == 0:
                continue
            else:
                for j in range(1,4):
                    if board[i][j] == board [i][j-1]:
                        bolas += 1
                if bolas == 4:
                    prateleiras += 1
        if prateleiras == 6:
            win = True

    return win