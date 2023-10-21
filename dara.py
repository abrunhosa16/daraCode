import random
import math
def ask_for_dimensions():
    # pede pelas dimensões e testa a sua validade
    # retorna as novas dimensões
    valid = False
    while not valid:
        try:
            row = int(input("Qual o numero de linhas desejado? >=5"))
            col = int(input("Numero de colunas desejado"))

            if row > 4  or col > 5:
                return [row,col]
            else:
                print("Numero de linhas tem de ser maior que 4 e colunas maior que 5")
        except ValueError:
            print("Erro, tente um valor inteiro")


def generate_board(width, height):
    # gera e retorna uma nova tabela de jogo
    matrix = []
    for i in range(width):
        vector = []
        for j in range(height):
            vector.append("_")
        matrix.append(vector)
    return matrix


def print_board(board):
    # printa a tabela de um jogo existente
    width, height = len(board), len(board[0])
    for i in range(width):
        for j in range(height):
            if board[i][j] == 'W':
                print("▨", end=" ")
            elif board[i][j] == 'B':
                print("■", end=" ")
            else:
                print("□", end=" ")
            if j == height - 1:
                print(" ")

#move = (x,y)
#turn = B or W

def isSpaceFree(board, move):
    #In my case the board is a matrix then the move need to be two coordinates
    return board[move[0] - 1][move[1] - 1] == '_'

def count_adjacent(board, move, turn, n):
    width, height = len(board), len(board[0])
    row_coord, col_coord = move
    row_coord = row_coord - 1
    col_coord = col_coord - 1
    acc = 0
    for i in range(col_coord, 0, -1):
        if board[row_coord][i - 1] == turn:
            acc += 1
        else:
            break
    for j in range(col_coord, height - 1):
        if board[row_coord][j + 1] == turn:
            acc += 1
        else:
            break
    if acc < n:
        return True
    else:
        return False


def count_column(board, move, turn, n):
    width, height = len(board), len(board[0])
    row_coord, col_coord = move
    row_coord = row_coord - 1
    col_coord = col_coord - 1
    acc = 0
    for i in range(row_coord, 0, - 1):
        if board[i - 1][col_coord] == turn:
            acc += 1
        else:
            break
    for j in range(row_coord, width - 1):
        if board[j + 1][col_coord] == turn:
            acc += 1
        else:
            break
    if acc < n:
        return True


def test_move_validity_drop_phase(board, move, turn):
    # testa se a jogada é válida para o estado de jogo atual na primeira fase
    # retorna true ou false
    return isSpaceFree(board,move) and count_adjacent(board, move, turn, 4) and count_column(board, move, turn, 4)

def test_move_validity_play_phase(board, move, pos):
    # testa se a jogada é válida para o estado de jogo atual na segunda fase
    # retorna true ou false
    row_pos, col_pos = pos
    row_move, col_move = move
    row_diff = math.abs(row_pos - row_move)
    col_diff = math.abs(col_pos - row_move)

    if row_diff <= 1 and col_diff <= 1 and col_diff*row_diff != 1 and isSpaceFree(board, move):
        return True
    else:
        return False

def test_move_validity_remove_phase(board, move, turn):
    # testa se a jogada é válida para o estado de jogo atual na fase de remoção
    #   (quando o na segunda fase o jogador formou uma linha de 3)
    return not count_adjacent(board, move, turn, 3) or not count_column(board, move, turn, 3)


def ask_for_first_player():
    # aqui tens que perguntar ao jogador quem é que deve jogar primeiro, as opções
    #   podem ser por exemplo "white", "black" ou "random" e retornas o valor relacionado
    valid = False
    while not valid:
        piece = input("Queres ser W, B or R?").upper()
        if piece == "W" or piece == "B":
            return piece
        elif piece == "R":
            m = random.randint(0,1)
            return "W" if m == 0 else "B"


def play_drop_phase(board, move, turn):
    # a jogada (que deve ser válida neste ponto) é jogada pelo jogador do turno atual
    move_row, move_col = move[0], move[1]
    if test_move_validity_drop_phase(board, move, turn):
        board[move_row - 1][move_col - 1] = turn
        return board

def adversario_encurralado(board, move, turn):
    width, height = len(board), len(board[0])
    list_w, list_b = [], []
    for i in range(width):
        for j in range(height):
            if turn == 'W':
                list_w.append(test_move_validity_play_phase(board, move, (i, j)))
            elif turn == 'B':
                list_b.append(test_move_validity_play_phase(board, move, (i, j)))

    if True in list_w or list_b:
        return False
    else:
        return True


def play_play_phase(board, move, turn, pos):
    # a jogada (que deve ser válida neste ponto) é jogada pelo jogador do turno atual
    # deve retornar um valor que refere se foi formada uma linha de três
    # deve retornar um valor que refere se o jogador encurralou o adversário e este não tem
    #   mais jogadas possíveis
    row_pos, col_pos = pos
    row_move, col_move = move
    if test_move_validity_play_phase(board, move, pos):
        board[row_move - 1][col_move - 1] = turn
        board[row_pos - 1][col_pos - 1] = '_'
        if test_move_validity_remove_phase(board, move, turn):
            return print("line 3")
        elif adversario_encurralado(board, move, turn):
            return "adversário encurralado"



def ask_for_next_move_drop_phase(board, turn):
    valid = False
    move_row, move_col = None, None
    while not valid:
        try:
            move_row = int(input("linhas"))
            move_col = int(input("colunas"))
        except:
            print("tente inteiros")
            continue
        valid = test_move_validity_drop_phase(board, (move_row,move_col), turn)

    return (move_row,move_col)


def ask_for_next_move_play_phase(board, turn):
    valid = False
    move = None
    while not valid:
        move = input("...")
        valid = test_move_validity_play_phase(board, move)

    return move


def ask_for_next_move_remove_phase(board, turn):
    valid = False
    move = None
    while not valid:
        move = input("...")
        valid = test_move_validity_remove_phase(board, move, turn)

    return move


def main():
    board = generate_board(*ask_for_dimensions())
    drop_piece_count = 25
    start_p = ask_for_first_player()

    # drop phase
    while drop_piece_count > 0:
        move = ask_for_next_move_drop_phase(board, start_p)
        play_drop_phase(board, move, start_p)

        move = ask_for_next_move_drop_phase(board, not start_p)
        play_drop_phase(board, move, not start_p)

        drop_piece_count -= 1

    # outras fases
    raise (NotImplementedError)


if __name__ == '__main__':
    main()