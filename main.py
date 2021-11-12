from sys import stdout
from os import system, name
import re

# Display Board Choices
def show_options():
    print("|1234567|")


# Display Board
def print_board(board):
    print("_________")
    for line in board:
        stdout.write('|')
        for char in line:
            stdout.write(char)
        stdout.write('|')
        print()
    print("|=======|")


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


def check_column(board, column, player):
    column_string = ""
    blue = re.compile('B+')
    red = re.compile('R+')

    for line in board:
        column_string = column_string + line[column]

    if player == 'B':
        m = blue.findall(column_string)
    else:
        m = red.findall(column_string)

    return len(max(m, key=len))


def check_row(board, column, player):
    row_string = ""
    blue = re.compile('B+')
    red = re.compile('R+')

    row_index = 0
    for line in board:
        if line[column] == 'O':
            row_index += 1
        else:
            break

    for char in board[row_index]:
        row_string = row_string + char

    if player == 'B':
        m = blue.findall(row_string)
    else:
        m = red.findall(row_string)

    return len(max(m, key=len))


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


def check_dia(board, column, player):

    test_board = [
        ['Q', 'R', 'Z', 'Y', 'X', 'V', 'W'],
        ['S', 'O', 'O', 'O', 'O', 'O', 'U'],
        ['T', 'O', 'O', 'O', 'O', 'O', 'T'],
        ['Y', 'O', 'O', 'O', 'O', 'O', 'Y'],
        ['X', 'O', 'O', 'O', 'O', 'O', 'Z'],
        ['V', 'W', 'U', 'T', 'S', 'Q', 'R'],
             ]
    # print(get_dia_string(test_board))

    dia_string = get_dia_string(board)

    blue = re.compile('B+')
    red = re.compile('R+')

    if player == 'B':
        m = blue.findall(dia_string)
    else:
        m = red.findall(dia_string)

    return len(max(m, key=len))


def game_is_over(board, column, player):
    # player: ai = 0, human = 1
    # set player symbol for matching
    if player == 0:
        symbol = 'R'
    else:
        symbol = 'B'

    if check_column(board, column, symbol) >= 4:
        return True
    if check_row(board, column, symbol) >= 4:
        return True
    if check_dia(board, column, symbol) >= 4:
        return True

    return False


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
    if game_is_over(board, column, 1):
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


def ai_turn(board):
    print("AI Turn Placeholder")
    return False


def main():
    board = [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['B', 'O', 'O', 'B', 'O', 'O', 'O'],
        ['R', 'O', 'R', 'O', 'O', 'O', 'O'],
        ['B', 'B', 'O', 'O', 'O', 'O', 'O'],
        ['B', 'O', 'O', 'O', 'O', 'O', 'O'],
             ]

    # Game loop starting with AI's turn
    while True:
        if ai_turn(board): #true if AI wins
            break
        elif player_turn(board): #true if player wins
            break



main()
