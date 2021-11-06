from sys import stdout
from os import system, name

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


def game_is_over(board, player):
    # player: ai = 0, human = 1
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
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
             ]

    # Game loop starting with AI's turn
    while True:
        if ai_turn(board):
            break
        elif player_turn(board):
            break



main()
