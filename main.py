# Dustin Mays - CS 480 - Minimax Connect 4

from sys import stdout
from os import system, name
import copy, time
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


# show column numbers and print board
def print_player_dashboard(board):
    show_options()
    print_board(board)


# clear board with enter
def end_player_turn(board):
    clear()
    print_board(board)
    input("Press Enter to end your turn.")
    clear()


# clear screen, print board, and print winning statement
def player_wins(board):
    clear()
    print_board(board)
    input("You have won!\nPress Enter to end the game.")


# clear screen, print board, and print losing statement
def ai_wins(board):
    clear()
    print_board(board)
    input("You have lost!\nPress Enter to end the game.")


# create string from each column
def column_string(board):
    column_string = ""
    for column in range(0,7):
        for line in board:
            column_string = column_string + line[column]
        column_string = column_string + '-'

    return column_string


# create string from each row
def row_string(board):
    row_string = ""
    for line in board:
        for space in range(0,7):
            row_string = row_string + line[space]
        row_string = row_string + '-'

    return row_string


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


# create string from all rows, columns, and diagonals
def get_board_string(board):
    column = column_string(board)
    row = row_string(board)
    diagonals = get_dia_string(board)
    all_lines = column + row + diagonals
    return all_lines


# check if game is over
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

# return a tuple of lists
# each list represents the number of ways a player can win
# increments up from one piece occupied and then blanks
# up to four consecutive matching pieces
def win_opportunities(board):
    red1 = re.compile('R_{3,5}|_{3,5}R')
    red2 = re.compile('RR_{2,5}|_{2,5}RR')
    red3 = re.compile('RRR_{2,5}|_{2,5}RRR|RR_R|R_RR')
    red4 = re.compile('RRRR')
    blue1 = re.compile('B_{3,5}|_{3,5}B')
    blue2 = re.compile('BB_{2,5}|_{2,5}BB')
    blue3 = re.compile('BBB_{2,5}|_{2,5}BBB|BB_B|B_BB')
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
# validates input for column selection
# places player piece on board
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


# check that a column can accept additional pieces
def check_column_user(board, index):
    # check the first row to see if a blank is available
    if board[0][index - 1] == '_':
        return True
    return False


# is the board completely full?
def board_full(board):
    for space in board[0]:
        if space == '_':
            return False
    return True


# for a given column(index), give the lowest open row
def get_row(board, index):
    row_available = -1
    for row in board:
        if row[index] != '_':
            break
        else:
            row_available = row_available + 1
    return row_available


# place user's piece in row/col
def make_user_move(board, column, row):
    board[row][column] = 'B'


# place AI's piece in row/col
def make_AI_move(board, column, row):
    board[row][column] = 'R'


# generate all possible boards resulting from one AI turn
# return as a list of boards (2d lists)
def gen_child_boards(board, player):
    children = []
    for space in range(0, 7):
        if board[0][space] == '_':
            b = copy.deepcopy(board)
            b[get_row(board, space)][space] = player
            children.append(b)

    return children


# take scores list and generate evaluation score for current board state
# higher score means a win is more likely for AI
def evaluation(board):
    scores = win_opportunities(board)
    plus = scores[0][0] + 3*scores[0][1] + 20*scores[0][2] + 10000*scores[0][3]
    minus = scores[1][0] + 3*scores[1][1] + 20*scores[1][2] + 10000*scores[1][3]
    final = plus - minus
    return final


# class comprised of a board, its score, and a list of children nodes
class Node:
    def __init__(self, board):
        self.board = board
        self.children = []
        self.score = evaluation(self.board)

    def set_children(self, player):
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


# minimax algorithm with alpha-beta pruning
# depth of 7 (arbitrarily chosen)
# builds out game tree per alpha-beta algorithm presented in class
def alphabeta(parent, depth, alpha, beta, isMaxPlayer):
    board = parent.get_board()
    current_score = parent.get_score()
    if depth == 42 or board_full(board) or abs(current_score) >= 1000: # someone has won if the abs(score) > 1000
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
    else: # minPlayer
        parent.set_children('B')
        for child in parent.children:
            beta = min(beta, alphabeta(child, depth+1, alpha, beta, True))
            if beta <= alpha:
                break
            return beta


def minimax(parent, depth, max_player):
    board = parent.get_board()
    current_score = parent.get_score()
    if depth == 4 or board_full(board) or abs(current_score) >= 1000:
        return current_score
    elif max_player:
        parent.set_children('R')
        temp = []
        for child in parent.children:
            temp.append(minimax(child, depth+1, False))
        return max(temp)
    else:
        parent.set_children('B')
        temp = []
        for child in parent.children:
            temp.append(minimax(child, depth+1, True))
        return min(temp)




# generate root node from current game board
# run minimax/alphabeta algorithm to get scores on root's children
# perform move from child with highest score
# check if game is over
def ai_turn(board):
    root = Node(board)

    start_time = time.time()
    # alphabeta(root, 0, -100000, 100000, True)
    minimax(root, 0, True)
    print("AI Algorithm Time: ", time.time() - start_time)
    children = root.get_children()
    children_values = []
    for child in children:
        children_values.append(child.get_score())

    max_value = max(children_values)
    max_index = children_values.index(max_value)

    row = get_row(board, max_index)
    make_AI_move(board, max_index, row)

    if game_is_over(board, 0):
        ai_wins(board)
        return True

    return False


# Primary game runner
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
        ['_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_'],
             ]

    # Game loop starting with AI's turn
    while True:
        if ai_turn(board): #true if AI wins
            break
        elif player_turn(board): #true if player wins
            break


main()
