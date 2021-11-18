from sys import stdout
from os import system, name
import copy
import re

# Display Board Choices
def show_options():
    print(" 1 2 3 4 5 6 7")


# Display Board
def print_board(board):
    print("________________")
    for line in board:
        stdout.write('|')
        for char in line:
            stdout.write(char)
            stdout.write(' ')
        stdout.write('|')
        print()
    print("|==============|")


# from geeksforgeeks.org
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# Input from user
def get_user_choice():
    print("Please make your next move.\nChoose a column 1-7.")
    while True:
        try:
            user_in = int(input("Column #: "))
        except ValueError:
            print("That's not a number")
        else:
            if user_in in range(1,8):
                return user_in
            else:
                print("Out of range. Try again.")


def print_player_dashboard(board):
    show_options()
    print_board(board)


def end_player_turn(board):
    clear()
    print_board(board)
    input("Press Enter to end your turn.")
    clear()


def player_wins(board):
    clear()
    print_board(board)
    input("You have won!\nPress Enter to end the game.")


def ai_wins(board):
    clear()
    print_board(board)
    input("You have lost!\nPress Enter to end the game.")


# def check_column(board, column, player):
#     column_string = ""
#     blue = re.compile('B+')
#     red = re.compile('R+')
#
#     for line in board:
#         column_string = column_string + line[column]
#
#     if player == 'B':
#         m = blue.findall(column_string)
#     else:
#         m = red.findall(column_string)
#
#     return len(max(m, key=len))


def column_string(board):
    column_string = ""
    for column in range(0,7):
        for line in board:
            column_string = column_string + line[column]
        column_string = column_string + '-'

    return column_string

def row_string(board):
    row_string = ""
    for line in board:
        for space in range(0,7):
            row_string = row_string + line[space]
        row_string = row_string + '-'

    return row_string

# def check_row(board, column, player):
#     row_string = ""
#     blue = re.compile('B+')
#     red = re.compile('R+')
#
#     row_index = 0
#     for line in board:
#         if line[column] == 'O':
#             row_index += 1
#         else:
#             break
#
#     for char in board[row_index]:
#         row_string = row_string + char
#
#     if player == 'B':
#         m = blue.findall(row_string)
#     else:
#         m = red.findall(row_string)
#
#     return len(max(m, key=len))


# create string of diagonal chars separated by '-'
def get_dia_string(board):
    dia_string = ""
    inc = 0

    # top-left to bottom right
    for i in range(0, 4):
        dia_string = dia_string + board[0][i]
        for j in range(0, 5):
            temp = j + i + 1
            if temp > 6:
                break
            dia_string = dia_string + board[j + 1][temp]
        dia_string = dia_string + '-'

    # top-right to bottom left
    for i in range(6, 2, -1):
        dia_string = dia_string + board[0][i]
        for j in range(0, 5):
            inc += 1
            temp = i - inc
            if temp < 0:
                break
            dia_string = dia_string + board[j + 1][temp]
        inc = 0
        dia_string = dia_string + '-'

    # four edge cases
    for j in range(0, 5):
        dia_string = dia_string + board[j + 1][j]
    dia_string = dia_string + '-'
    for j in range(0, 4):
        dia_string = dia_string + board[j + 2][j]
    dia_string = dia_string + '-'
    for j in range(0, 5):
        dia_string = dia_string + board[j + 1][6 - j]
    dia_string = dia_string + '-'
    for j in range(0, 4):
        dia_string = dia_string + board[j + 2][6 - j]

    return dia_string


# def check_dia(board, column, player):
#
#     test_board = [
#         ['Q', 'R', 'Z', 'Y', 'X', 'V', 'W'],
#         ['S', 'O', 'O', 'O', 'O', 'O', 'U'],
#         ['T', 'O', 'O', 'O', 'O', 'O', 'T'],
#         ['Y', 'O', 'O', 'O', 'O', 'O', 'Y'],
#         ['X', 'O', 'O', 'O', 'O', 'O', 'Z'],
#         ['V', 'W', 'U', 'T', 'S', 'Q', 'R'],
#              ]
#     # print(get_dia_string(test_board))
#
#     dia_string = get_dia_string(board)
#
#     blue = re.compile('B+')
#     red = re.compile('R+')
#
#     if player == 'B':
#         m = blue.findall(dia_string)
#     else:
#         m = red.findall(dia_string)
#
#     return len(max(m, key=len))


def get_board_string(board):
    column = column_string(board)
    row = row_string(board)
    diagonals = get_dia_string(board)
    all_lines = column + row + diagonals
    return all_lines

def game_is_over(board, player):
    blue = re.compile('B{4,6}')
    red = re.compile('R{4,6}')

    board_string = get_board_string(board)

    # player: ai/R = 0, human/B = 1
    if player == 0:
        m = red.findall(board_string)
    else:
        m = blue.findall(board_string)

    if m:
        return True
    else:
        return False


def win_opportunities(board):
    red1 = re.compile('RO{3,5}|O{3,5}R')
    red2 = re.compile('RRO{2,5}|O{2,5}RR')
    red3 = re.compile('RRRO{2,5}|O{2,5}RRR|RROR|RORR')
    red4 = re.compile('RRRR')
    blue1 = re.compile('BO{3,5}|O{3,5}B')
    blue2 = re.compile('BBO{2,5}|O{2,5}BB')
    blue3 = re.compile('BBBO{2,5}|O{2,5}BBB|BBOB|BOBB')
    blue4 = re.compile('BBBB')

    board_string = get_board_string(board)
    m = re.split('-', board_string)

    red_match = [0, 0, 0, 0]
    blue_match = [0, 0, 0, 0]

    for line in m:
        if bool(re.search(red4, line)):
            red_match[3] += 1
        elif bool(re.search(red3, line)):
            red_match[2] += 1
        elif bool(re.search(red2, line)):
            red_match[1] += 1
        elif bool(re.search(red1, line)):
            red_match[0] += 1

        if bool(re.search(blue4, line)):
            blue_match[3] += 1
        elif bool(re.search(blue3, line)):
            blue_match[2] += 1
        elif bool(re.search(blue2, line)):
            blue_match[1] += 1
        elif bool(re.search(blue1, line)):
            blue_match[0] += 1

    score_pair = [red_match, blue_match]

    return score_pair


# returns True if player wins
def player_turn(board):
    print_player_dashboard(board)
    print()
    user_input = get_user_choice()
    while True:
        if check_column_user(board, int(user_input)) == True:
            break
        else:
            input("Move not legal.\nPress Enter and then try again.")
            clear()
            print_player_dashboard(board)
            user_input = get_user_choice()
    # Transform user_input (1-7) into board[] index (0-6)
    column = user_input - 1
    # Make change to board
    make_user_move(board, column, get_row(board, column))
    if game_is_over(board, 1):
        player_wins(board)
        return True
    else:
        end_player_turn(board)
        return False

def check_column_user(board, index):
    # check the first row to see if a blank is available
    if board[0][index - 1] == 'O':
        return True
    return False


def board_full(board):
    for space in board[0]:
        if space == 'O':
            return False
    return True


def get_row(board, index):
    row_available = -1
    for row in board:
        if row[index] != 'O':
            break
        else:
            row_available = row_available + 1
    return row_available


def make_user_move(board, column, row):
    board[row][column] = 'B'

def make_AI_move(board, column, row):
    board[row][column] = 'R'


def gen_child_boards(board, player):
    children = []
    for space in range(0, 7):
        if board[0][space] == 'O':
            b = copy.deepcopy(board)
            b[get_row(board, space)][space] = player
            children.append(b)

    return children


def evaluation(board):
    scores = win_opportunities(board)
    plus = scores[0][0] + 2*scores[0][1] + 10*scores[0][2] + 10000*scores[0][3]
    minus = scores[1][0] + 2*scores[1][1] + 10*scores[1][2] + 10000*scores[1][3]
    final = plus - minus
    return final


class Node:
    def __init__(self, board):
        self.board = board
        self.children = []
        self.score = evaluation(self.board)

    def set_children(self, player): # ! These need to be nodes themselves..
        temp_boards = gen_child_boards(self.board, player)
        for board in temp_boards:
            self.children.append(Node(board))

    def get_children(self):
        return self.children

    def get_board(self):
        return self.board

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score


def alphabeta(parent, depth, alpha, beta, isMaxPlayer):
    board = parent.get_board()
    current_score = parent.get_score()
    if depth == 4 or board_full(board) or abs(current_score) >= 1000: # someone has won if the abs(score) > 1000
        return current_score
    elif isMaxPlayer:
        parent.set_children('R')
        for child in parent.children:
            alpha = max(alpha, alphabeta(child, depth+1, alpha, beta, False))
            if beta <= alpha:
                break
            # if depth == 0:
            #     return child
            return alpha
    else: #minPlayer
        parent.set_children('B')
        for child in parent.children:
            beta = min(beta, alphabeta(child, depth+1, alpha, beta, True))
            if beta <= alpha:
                break
            return beta


def ai_turn(board):
    # print("AI Turn Placeholder")
    root = Node(board)

    alphabeta(root, 0, -100000, 100000, True)
    if game_is_over(board, 0):
        ai_wins(board)
        return True
    children = root.get_children()
    children_values = []
    for child in children:
        children_values.append(child.get_score())

    max_value = max(children_values)
    max_index = children_values.index(max_value)

    row = get_row(board, max_index)
    make_AI_move(board, max_index, row)

    return False


def main():
    test_board = [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['B', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['R', 'O', 'B', 'R', 'R', 'O', 'O'],
        ['B', 'B', 'B', 'R', 'R', 'O', 'O'],
        ['B', 'B', 'R', 'R', 'R', 'O', 'R'],
    ]
    board = [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
             ]

    # evaluation(test_board)
    # gen_child_boards(test_board, 'X')

    # Game loop starting with AI's turn
    while True:
        if ai_turn(board): #true if AI wins
            break
        elif player_turn(board): #true if player wins
            break


main()
