def find_empty(board):
    empty_spaces = [(i+1)*10 + (j+1) for i in range(3) for j in range(3) if board[i][j] == '']
    return empty_spaces[0] if empty_spaces else None


board = [['', 'O', 'X'],
         ['X', 'O', 'X'],
         ['O', 'X', 'O']]

empty_index = str(find_empty(board))

if empty_index is not None:
    print(empty_index)  # output: 11
else:
    print("Board is full!")