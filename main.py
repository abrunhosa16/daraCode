import random
def board_gen(x,y):
    matriz = []
    for linha in range(x):
        vetor = []
        for coluna in range(y):
            vetor.append('_')
        matriz.append(vetor)
    return matriz

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
    for col in board:
        colCopy = []
        for row in col:
            colCopy.append(row)
        boardCopy.append(colCopy)
    return boardCopy

def spaceIsFree(board, moveX,moveY):
    #In my case the board is a matrix then the move need to be two coordinates
    return board[moveX][moveY] == '_'


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


