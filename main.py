import random
def board_gen(x,y):
    matrix = []
    for row in range(x):
        vetor = []
        for col in range(y):
            vetor.append('_')
        matrix.append(vetor)
    return matrix

def print_board(board):
    x,y = len(board), len(board[0])
    for i in range(x):
        for j in range(y):
            if board_gen(x,y)[i][j] == 'W':
                print("▨", end=" ")
            elif board_gen(x,y)[i][j] == 'B':
                print("■", end=" ")
            else:
                print("□", end=" ")
            if j == y-1:
                print(" ")


def inputPlayersLetter(letter):
    # [first_player, second_player]
    if letter == 'W':
        return ['W', 'B']
    else:
        return ['B', 'W']

def whoGoesFirst():
    if random.randint(0,1) == 0:
        return "white"
    else:
        return "black"

#Colocar inicialmente as peças no tabuleiro
def piecesboard(board, letter, moveX, moveY):
    board[moveX][moveY] = letter

#fazer movimentos durante o jogo
def makeMove(board, letter, moveX, moveY):
    board[moveX][moveY] = letter

#Perdedor
def isLoser(board, letter):
    acc = 0
    for row in board:
        acc += row.count(letter)
    if acc <= 2:
        return True
    else:
        return False

def boardCopy(board):
    boardCopy = []
    for row in board:
        colCopy = []
        for col in row:
            colCopy.append(col)
        boardCopy.append(colCopy)
    return boardCopy

def isSpaceFree(board, move):
    #In my case the board is a matrix then the move need to be two coordinates
    return board[move[0]][move[1]] == '_'


# Como ainda nao percebi muito bem o main, vou deixar o input dentro da função drop e depois alterar quando perceber melhor
def getPlayerMove(board):
    moveX, moveY = ' ', ' '
    lenRow, lenCol = len(board), len(board[0])
    listRow = [i for i in range(lenRow + 1)][1:]
    listCol = [j for j in range(lenCol + 1)][1:]

    while not (moveX in listRow and moveY in listCol) or not isSpaceFree(board, int(moveX), int(moveY)):
        moveX = input("What is your next move row (1 - " + str(lenRow) + ')')
        moveY = input("What is your next move col (1 - " + str(lenCol) + ')')
    return (int(moveX), int(moveY))



def main():
    #board size
    row = input("Quantas linhas terá o tabuleiro?")
    column = input("Quantas colunas terá o tabuleiro?")

    #draw_board
    empty_board = board_gen(int(row),int(column))
    print_board(empty_board)

    #pieces choice
    letter = ''
    while not (letter == 'W' or letter == 'B'):
        letter = input("Queres ser brancas (w) ou pretas (b)?").upper()
    inputPlayersLetter(letter)

    pass
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


