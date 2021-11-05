from sys import stdout


# Ask for input from user
    # Display Board Choices

def show_options():
    print("|1234567|")

# Input from user
def get_user_choice():
    print("Please choose your next move. Enter a number 1-7 corresponding with a column.")
    while True:
        try:
            user_in = int(input("Column #: "))
        except ValueError:
            print("That's not a number")
        else:
            if user_in in range(1,7):
                return user_in
            else:
                print("Out of range. Try again.")


# Check legal move -> ask for new input
    # Within bounds of board
    # Block already there

# Check that game is complete/won

# Announce correct winner

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

# Choose AI move

# Perform AI move

def main():
    board = [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
             ]
    show_options()
    print_board(board)
    print(get_user_choice())

main()