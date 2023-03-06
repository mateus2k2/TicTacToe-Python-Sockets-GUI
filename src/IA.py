import random
import numpy as np

class IAOponent:
    
    def getRandomMove(self, board, moves):
        possibleMoves = []
        for i in moves:
            if board[i] == ' ':
                possibleMoves.append(i)

        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None
    
    def makeMove(self, board, letter, move):
        if board[move] == ' ':
            board[move] = letter

    def isWinner(self, board, letter):
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use board instead of board and le instead of letter so we don't have to type as much.
        return ((board[7-1] == letter and board[8-1] == letter and board[9-1] == letter) or # across the top
                (board[4-1] == letter and board[5-1] == letter and board[6-1] == letter) or # across the middle
                (board[1-1] == letter and board[2-1] == letter and board[3-1] == letter) or # across the bottom
                (board[7-1] == letter and board[4-1] == letter and board[1-1] == letter) or # down the left side
                (board[8-1] == letter and board[5-1] == letter and board[2-1] == letter) or # down the middle
                (board[9-1] == letter and board[6-1] == letter and board[3-1] == letter) or # down the right side
                (board[7-1] == letter and board[5-1] == letter and board[3-1] == letter) or # diagonal
                (board[9-1] == letter and board[5-1] == letter and board[1-1] == letter)) # diagonal

    def getBoardCopy(self, board):
        dupeBoard = []

        for i in board:
            dupeBoard.append(i)

        return dupeBoard
    
    def getExpertMove(self, board, computerletter, theFirstPlayer, turnNumber):
        if computerletter == 'X':
            playersLetter = 'O'
        else:
            playersLetter = 'X'
        # Check for each place in the board

        for i in range(1-1, 10-1):
            copy = self.getBoardCopy(board)
            self.makeMove(copy, computerletter, i)
            if self.isWinner(copy, computerletter):
                return i


        # Check if player could win in next move, and block them
        for i in range(1-1, 10-1):
            copy = self.getBoardCopy(board)
            self.makeMove(copy, playersLetter, i)
            if self.isWinner(copy, playersLetter):
                return i

        if theFirstPlayer == 'player':
            if board[5-1] == ' ':
                return 5-1

        if turnNumber == 2 and theFirstPlayer == 'player':
            move = self.getRandomMove(board, [2-1, 4-1, 6-1, 8-1])
            if move != None:
                return move



        # Take one of the cornors is free, using the Choose random move from list function
        move = self.getRandomMove(board, [7-1, 9-1, 1-1, 3-1])
        if move != None:
            return move
        # Try to take the center if free
        if board[5-1] == ' ':
            return 5-1

        # Take on of the sides. Using the choose random move from list function
        move = self.getRandomMove(board, [2-1, 4-1, 6-1, 8-1])
        if move != None:
            return move

    def getBeginnerMove(self, board, computerletter):
        move = self.getRandomMove(board, [1-1, 2-1, 3-1, 4-1, 5-1, 6-1, 7-1, 8-1, 9-1])
        if move != None:
            return move

    def getEasyMove(self, board, computerletter):
        if computerletter == 'X':
            playersLetter = 'O'
        else:
            playersLetter = 'X'

        for i in range(1-1, 10-1):
            copy = self.getBoardCopy(board)
            self.makeMove(copy, computerletter, i)
            if self.isWinner(copy, computerletter):
                return i
        # Check if player could win in next move, and block them
        for i in range(1-1, 10-1):
            copy = self.getBoardCopy(board)
            self.makeMove(copy, playersLetter, i)
            if self.isWinner(copy, playersLetter):
                return i

        move = self.getRandomMove(board, [1-1, 2-1, 3-1, 4-1, 5-1, 6-1, 7-1, 8-1, 9-1])
        if move != None:
            return move

    def getIntermediateMove(self, board, computerletter):
        if computerletter == 'X':
            playersLetter = 'O'
        else:
            playersLetter = 'X'

        for i in range(1-1, 10-1):
            copy = self.getBoardCopy(board)
            self.makeMove(copy, computerletter, i)
            if self.isWinner(copy, computerletter):
                return i
        # Check if player could win in next move, and block them
        for i in range(1-1, 10-1):
            copy = self.getBoardCopy(board)
            self.makeMove(copy, playersLetter, i)
            if self.isWinner(copy, playersLetter):
                return i

        move = self.getRandomMove(board, [7-1, 9-1, 1-1, 3-1])
        if move != None:
            return move
        # Try to take the center if free
        if board[5-1] == ' ':
            return 5-1

        move = self.getRandomMove(board, [2-1, 4-1, 6-1, 8-1])
        if move != None:
            return move

    def getComputerMove(self, boardMatrix, computerletter, theFirstPlayerNumber, turnNumber, difficulty):
        board = np.array(boardMatrix).flatten()
        board[board==''] = ' '
        
        if(theFirstPlayerNumber == 0): theFirstPlayer = 'player'
        if(theFirstPlayerNumber == 1): theFirstPlayer = 'computer' 
        
        if difficulty == 0:
            move = self.getEasyMove(board, computerletter)
        if difficulty == 1:
            move = self.getBeginnerMove(board, computerletter)
        if difficulty == 2:
            move = self.getIntermediateMove(board, computerletter)
        if difficulty == 3:
            move = self.getExpertMove(board, computerletter, theFirstPlayer, turnNumber)    
            
        dict = {0: "11", 1: "12", 2: "13", 3: "21", 4: "22", 5: "23", 6: "31", 7: "32", 8: "33"}
        return dict[move]


# boardMatrix = [['X', '', ''], ['', '', ''], ['', '', '']]
# computerletter = 'X'
# theFirstPlayerNumber = 0
# turnNumber = 0
# difficulty = 3

# obj = IAOponent()
# retorno = obj.getComputerMove(boardMatrix, computerletter, theFirstPlayerNumber, turnNumber, difficulty)
# print("MOVE: " + retorno)