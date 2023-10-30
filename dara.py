import random

def ask_for_dimensions():
    # pede pelas dimensões e testa a sua validade
    # retorna as novas dimensões
    valid = False
    while not valid:
        try:
            row = int(input("Qual o numero de linhas desejado? >= 5 "))
            col = int(input("Numero de colunas desejado >= 6 "))

            if row > 4 and col > 5:
                return [row, col]
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
    for m in range(height+1):
        print(m, end=" ")
    print(" ")
    for i in range(width):
        print(i + 1, end=" ")
        for j in range(height):
            if board[i][j] == 'W':
                print("W", end=" ")
            elif board[i][j] == 'B':
                print("B", end=" ")
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
    row_coord, col_coord  = move[0], move[1]
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
    row_coord, col_coord = move[0], move[1]
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
    if not ((move[0] > 0 and move[0] <= len(board)) and (move[1] > 0 and move[1] <= len(board[0]))):
        print("Fora das margens")
        return False

    if not isSpaceFree(board, move):
        print("Espaço não disponível")
        return False

    if not (count_adjacent(board, move, turn, 3) and count_column(board, move, turn, 3)):
        print("Proibido mais de 3 em linha")
        return False
    return True

def moviment(move):
    move_return = [move[0], move[1]]
    if move[2] == 'C':
        move_return[0] -= 1
    elif move[2] == 'B':
        move_return[0] += 1
    elif move[2] == 'E':
        move_return[1] -= 1
    elif move[2] == 'D':
        move_return[1] += 1
    return move_return



def test_move_validity_play_phase(board, move, turn):
    # testa se a jogada é válida para o estado de jogo atual na segunda fase
    # retorna true ou false
    if not ((move[0] > 0 and move[0] <= len(board)) and (move[1] > 0 and move[1] <= len(board[0]))):
        print("Fora das margens")
        return False

    if  board[move[0] - 1][move[1] - 1] != turn:
        print("Essa não é sua peça amiguinho!!!")
        return False

    if move[2] not in ['C', 'E', 'B', 'D']:
        print("Fora das opções seu desatento")
        return False

    margens = moviment(move)

    if not ((margens[0] > 0 and margens[0] <= len(board)) and (margens[1] > 0 and margens[1] <= len(board[0]))):
        print("Fora das margens")
        return False

    if not isSpaceFree(board, margens):
        print("Casinha não esta vaziaaa")
        return False

    return True



def test_move_validity_remove_phase(board, move, turn):
    # testa se a jogada é válida para o estado de jogo atual na fase de remoção
    #   (quando o na segunda fase o jogador formou uma linha de 3)
    return not count_adjacent(board, move, turn, 2) or not count_column(board, move, turn, 2)


def ask_for_first_player():
    # aqui tens que perguntar ao jogador quem é que deve jogar primeiro, as opções
    #   podem ser por exemplo "white", "black" ou "random" e retornas o valor relacionado
    valid = False
    while not valid:
        piece = input("Queres ser W, B or R? ").upper()
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



def play_play_phase(board, move, turn):
    # a jogada (que deve ser válida neste ponto) é jogada pelo jogador do turno atual
    # deve retornar um valor que refere se foi formada uma linha de três
    # deve retornar um valor que refere se o jogador encurralou o adversário e este não tem
    #   mais jogadas possíveis
    if test_move_validity_play_phase(board, move, turn):
        board[moviment(move)[0] - 1][moviment(move)[1] - 1] = turn
        board[move[0] - 1][move[1] - 1] = '_'
    return board



def ask_for_next_move_drop_phase(board, turn):
    valid = False
    move_row, move_col = None, None
    while not valid:
        try:
            move_row = int(input("Em qual linha queres pôr a peça? "))
            move_col = int(input("Em qual coluna queres pôr a peça? "))
        except ValueError:
            print("tente inteiros")
            continue
        valid = test_move_validity_drop_phase(board, (move_row,move_col), turn)
    return (move_row, move_col)


def ask_for_next_move_play_phase(board, turn):
    valid = False
    move = None
    while not valid:
        move_row = int(input("Em qual linha está a peça? "))
        move_col = int(input("Em qual coluna está a peça? "))
        move_where = input("Pra where queres mover? ").upper()
        move = [move_row, move_col, move_where]
        valid = test_move_validity_play_phase(board, move, turn)
    return move


def ask_for_next_move_remove_phase(board, turn):
    move = None
    valid = False
    while not valid:
        try:
            move_row = int(input("linha da peça ser removida "))
            move_col = int(input(" e coluna "))
            move = [move_row - 1, move_col - 1]
        except ValueError:
            print("Tente inteiros")
            continue
        valid = (board[move[0]][move[1]] == turn)
    return move


def play_remove_phase(board, move):
    board[move[0]][move[1]] = '_'
    return board

def pieces_count(board):
    w_acc=0
    b_acc = 0
    for lista in board:
        w_acc += lista.count("W")
        b_acc += lista.count("B")
    return [w_acc, b_acc]

##################################
#Create AI
def possible_play_moves(board, turn):
    width, height = len(board), len(board[0])
    lis = []
    for i in range(1, width + 1):
        for j in range(1, height + 1):
            if board[i - 1][j - 1] == turn:
                for options in ["C", "B", "E", "D"]:
                    if test_move_validity_play_phase(board, [i, j, options], turn):
                        lis.append([i, j, options])
    return lis

def possible_drop_phase(board):
    valid = False
    row = None
    col = None
    while not valid:
        row = random.randint(1, len(board))
        col = random.randint(1, len(board[0]) )
        valid = (board[row - 1][col - 1] == '_')
    return (row, col)


def main():
    board = generate_board(*ask_for_dimensions())
    drop_piece_count = 4
    start_p = ask_for_first_player()

    if start_p == 'W':
        sec_p = "B"
    else:
        sec_p = "W"

    # drop phase
    while drop_piece_count > 0:
        print_board(board)
        print("First Player " + str(drop_piece_count) + " peças")
        move = ask_for_next_move_drop_phase(board, start_p)
        play_drop_phase(board, move, start_p)


        print_board(board)
        print("Second Player " + str(drop_piece_count) + " peças")

        move = possible_drop_phase(board)
        play_drop_phase(board, move, sec_p)


        drop_piece_count -= 1
    valid = True
    while valid:
        print_board(board)
        print("First Player ")
        move = ask_for_next_move_play_phase(board, start_p)
        play_play_phase(board, move, start_p)
        if test_move_validity_remove_phase(board, moviment(move), start_p):
            print_board(board)
            remove = ask_for_next_move_remove_phase(board, sec_p)
            play_remove_phase(board, remove)

        if pieces_count(board)[1] < 3 or len(possible_play_moves(board, sec_p)) == 0:
            print("first wins")
            break



        print_board(board)
        print("Second Player ")
        move = random.choice(possible_play_moves(board, sec_p))
        play_play_phase(board, move, sec_p)
        if test_move_validity_remove_phase(board, moviment(move), sec_p):
            print_board(board)
            remove = ask_for_next_move_remove_phase(board, start_p)
            play_remove_phase(board, remove)

        if pieces_count(board)[0] < 3 or len(possible_play_moves(board, start_p)) == 0:
            print("scnd wins")
            break

        valid = True







if __name__ == '__main__':
    main()