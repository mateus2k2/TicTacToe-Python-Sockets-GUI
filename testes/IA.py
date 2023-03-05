#https://github.com/maxrimmer/Tic-Tac-Toe-AI/blob/master/tictactoe.py#enroll-beta
# Tic Tac Toe A.I
# Created by Max Rimmer Larsen, 2016

# Import declarations
import random

turnNumber = 0

def getDifficulty():
    difficulty = ''
    while not (difficulty == 'b' or difficulty == 'e' or difficulty == 'i' or difficulty == 'x'):
        print("Please enter a difficulty level: b, e, i, or x")
        difficulty = input()
    return difficulty

def drawboard(board):
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')


# Get players input letter, void
def getLetter():
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print ("Choose X or O")
        letter = input().upper()

    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


# Get who goes first, void
def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'
# Play again? Void

def playAgain():
    playAgain = ''
    print ("Do you want to play again? Y or N")
    while not (playAgain ==  'Y' or playAgain == 'N'):
        playAgain = input().upper()
    if playAgain == 'Y':
        return True
    else:
        return False


# Make move taking argument board letter and move
def makeMove(board, letter, move):
    if isSpaceFree(board, move):
        board[move] = letter


# Is winner taking argument board and letter
def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal
# Get a copy of the board, taking argument board
def getBoardCopy(board):
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard
# Is space free, taking argument board and move
def isSpaceFree(board, move):
    if board[move] == ' ':
        return True
    else:
        return False

# Get player move, taking argument board
def getPlayerMove(board):
    print ("Choose a place to put your letter. Remember the board goes: 7, 8, 9. 4, 5, 6. 1, 2, 3")
    move = 0
    while not (move > 0 and move < 10) or not isSpaceFree(board, move):
        move = int(input())
    return move

# Choose random move from list taking argument board and list of moves
def getRandomMove(board, moves):
    possibleMoves = []
    for i in moves:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None
# Get A.I move, taking argument board and computerletter
def getExpertMove(board, computerletter, theFirstPlayer, turnNumber):
    if computerletter == 'X':
        playersLetter = 'O'
    else:
        playersLetter = 'X'
    # Check for each place in the board

    for i in range(1, 10):
        copy = getBoardCopy(board)
        makeMove(copy, computerletter, i)
        if isWinner(copy, computerletter):
            return i


    # Check if player could win in next move, and block them
    for i in range(1, 10):
        copy = getBoardCopy(board)
        makeMove(copy, playersLetter, i)
        if isWinner(copy, playersLetter):
            return i

    if theFirstPlayer == 'player':
        if isSpaceFree(board, 5):
            return 5

    if turnNumber == 2 and theFirstPlayer == 'player':
        move = getRandomMove(board, [2, 4, 6, 8])
        if move != None:
            return move



    # Take one of the cornors is free, using the Choose random move from list function
    move = getRandomMove(board, [7, 9, 1, 3])
    if move != None:
        return move
    # Try to take the center if free
    if isSpaceFree(board, 5):
        return 5

    # Take on of the sides. Using the choose random move from list function
    move = getRandomMove(board, [2, 4, 6, 8])
    if move != None:
        return move

def getBeginnerMove(board, computerletter):
    move = getRandomMove(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    if move != None:
        return move

def getEasyMove(board, computerletter):
    if computerletter == 'X':
        playersLetter = 'O'
    else:
        playersLetter = 'X'

    for i in range(1, 10):
        copy = getBoardCopy(board)
        makeMove(copy, computerletter, i)
        if isWinner(copy, computerletter):
            return i
    # Check if player could win in next move, and block them
    for i in range(1, 10):
        copy = getBoardCopy(board)
        makeMove(copy, playersLetter, i)
        if isWinner(copy, playersLetter):
            return i

    move = getRandomMove(board, [1, 2,3,4,5,6,7,8,9])
    if move != None:
        return move

def getIntermediateMove(board, computerletter):
    if computerletter == 'X':
        playersLetter = 'O'
    else:
        playersLetter = 'X'

    for i in range(1, 10):
        copy = getBoardCopy(board)
        makeMove(copy, computerletter, i)
        if isWinner(copy, computerletter):
            return i
    # Check if player could win in next move, and block them
    for i in range(1, 10):
        copy = getBoardCopy(board)
        makeMove(copy, playersLetter, i)
        if isWinner(copy, playersLetter):
            return i

    move = getRandomMove(board, [7, 9, 1, 3])
    if move != None:
        return move
    # Try to take the center if free
    if isSpaceFree(board, 5):
        return 5

    move = getRandomMove(board, [2,4,6,8])
    if move != None:
        return move

def getComputerMove(board, computerletter, theFirstPlayer, turnNumber, difficulty):
    if difficulty == 'e':
        move = getEasyMove(board, computerletter)
        return move
    if difficulty == 'b':
        move = getBeginnerMove(board, computerletter)
        return move
    if difficulty == 'i':
        move = getIntermediateMove(board, computerletter)
        return move
    if difficulty == 'x':
        move = getExpertMove(board, computerletter, theFirstPlayer, turnNumber)
        return move

# Is board full, taking argument board
def boardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True
# Welcome to tic tac toe, let me tell you on before hand that you won't win...
print ("Welcome to tic tac toe, let me tell you on before hand that you won't win...")
# While true
while True:
    difficulty = getDifficulty()
    board = [' '] * 10
    playersLetter, computerletter = getLetter()
    turn = whoGoesFirst()
    theFirstPlayer = turn
    if turn == 'player':
        print ("You go first")
    else:
        print ("The computer goes first")
    gameIsPlaying = True
    turnNumber = 0


    # While gameIsPlaying
    while gameIsPlaying:
        if turn == 'player':
            drawboard(board)
            move = getPlayerMove(board)
            makeMove(board, playersLetter ,move)

            if isWinner(board, playersLetter):
                drawboard(board)
                print ("Wow you won! There must be a mistake in the A.I algorithm...")
                gameIsPlaying = False
            if boardFull(board):
                drawboard(board)
                print ("It is a tie!")
                gameIsPlaying = False
            else:
                turn = 'computer'

        else:
            turnNumber += 1
            move = getComputerMove(board, computerletter, theFirstPlayer, turnNumber, difficulty)
            makeMove(board, computerletter, move)

            if isWinner(board, computerletter):
                drawboard(board)
                print ("The computer won, no wonder uh?")
                gameIsPlaying = False
            if boardFull(board):
                drawboard(board)
                print ("It is a tie!")
                gameIsPlaying = False
            else:
                turn = 'player'

    if not playAgain():
        break