board = [['', 'O', 'X'],
         ['X', 'O', 'X'],
         ['O', 'X', 'O'],]

def print_board():
    for i in range(3):
        print("-" * 14)
        print("|", end=" ")
        for j in range(3):
            elem = ''
            if(board[i][j] == ''): elem = ' ' 
            else: elem = board[i][j]
            print(elem, "|", end=" ")
        print()
    print("-" * 14)

print_board()