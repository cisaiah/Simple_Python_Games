'''
This is a simple Tic Tac Toe game meant for two players
Use the numbers 1 to 9 to select the positions

      1  |  2  | 3
    ----------------
      4  |  5  | 6
    ----------------
      7  |  8  | 9
'''


# Function to get user input for Player 1
def player1_symbol(player1_name):
    result = 'a'
    while result not in ['X','O','x','o']:
        result = input('\n' + player1_name + ', Do you want to be X or O? ')
        if result.upper() not in ['X','O']:
            print('Invalid Choice! Choose either X or O')
    return result.upper()

# Assign the other character to player 2
def player2_symbol(player1):
    if player1 == 'X':
        return 'O'
    else:
        return 'X'

# Function to draw the board
def display_board(row1, row3, row5):
    rowblank = ('           ')
    rowline =  ('-----------')
    print(rowblank)
    print(row1)
    print(rowline)
    print(row3)
    print(rowline)
    print(row5)
    print(rowblank)

# Function for each play turn.
def play_turn():
    play = 0
    while play not in list(range(1,10)):
        play = input('Choose a position on you NumPad (1-9): ')
        if play.isdigit() == False:
            print('Please enter and valid number!')
        elif int(play) not in list(range(1,10)):
            print('Invalid Position! Choose a position on you NumPad (1-9)')
        else:
            play = int(play)
    return play

# Function to check that player does not choose a position that is already taken
def check_position(position, row1, row2, row3):
    # Check if the position is empty
    if (position == 1 and row1[1] != ' ') or (position == 2 and row1[5] != ' ') or (position == 3 and row1[9] != ' ') \
            or (position == 4 and row2[1] != ' ') or (position == 5 and row2[5] != ' ') or (
            position == 6 and row2[9] != ' ') \
            or (position == 7 and row3[1] != ' ') or (position == 8 and row3[5] != ' ') or (
            position == 9 and row3[9] != ' '):
        print('Position already taken')
        return 'bad'
    else:
        return 'good'

# Assign player's character (X/O) to player's chosen position
def assign_position(position, play_sign, row1, row3, row5):
    list1 = list(row1)
    list3 = list(row3)
    list5 = list(row5)

    # Assign the position
    if position == 1:
        list1[1] = play_sign
        return ''.join(list1)
    elif position == 2:
        list1[5] = play_sign
        return ''.join(list1)
    elif position == 3:
        list1[9] = play_sign
        return ''.join(list1)
    elif position == 4:
        list3[1] = play_sign
        return ''.join(list3)
    elif position == 5:
        list3[5] = play_sign
        return ''.join(list3)
    elif position == 6:
        list3[9] = play_sign
        return ''.join(list3)
    elif position == 7:
        list5[1] = play_sign
        return ''.join(list5)
    elif position == 8:
        list5[5] = play_sign
        return ''.join(list5)
    elif position == 9:
        list5[9] = play_sign
        return ''.join(list5)

# Determine if/when there is a winner
def win(row1, row3, row5):
    if (row1[1] == row1[5] == row1[9] and row1[1] != ' ') or (row3[1] == row3[5] == row3[9] and row3[1] != ' ') or (row5[1] == row5[5] == row5[9] and row5[1] != ' ') \
    or (row1[1] == row3[1] == row5[1] and row1[1] != ' ') or (row1[5] == row3[5] == row5[5] and row1[5] != ' ') or (row1[9] == row3[9] == row5[9] and row1[9] != ' ') \
    or (row1[1] == row3[5] == row5[9] and row1[1] != ' ') or (row1[9] == row3[5] == row5[1] and row1[9] != ' '):
        return 'winner'
    elif row1[1] != ' ' and row1[5] != ' ' and row1[9] != ' ' and row3[1] != ' ' and row3[5] != ' ' and row3[9] != ' ' \
    and row5[1] != ' ' and row5[5] != ' ' and row5[9] != ' ':
        return 'no_winner'
    else:
        return 'none'



# LET THE GAME BEGIN
# Introduction
print('WELCOME TO THIS TIC TAC TOE GAME \nPlay the game using numbers 1-9 to choose positions\n')

from IPython.display import clear_output

# Get names of players
player1 = input('\nEnter name of Player1: ').upper()
player2 = input('\nEnter name of Player2: ').upper()

# Ask Player 1 if he/she wants to be X or O
play_sign1 = player1_symbol(player1)

# Assign the other symbol to player2
play_sign2 = player2_symbol(play_sign1)

play_again = 'Y'
while play_again in ('Y','y'):

    # Draw the board
    row1 = ('   |   |   ')
    row3 = ('   |   |   ')
    row5 = ('   |   |   ')

    # Display board
    display_board(row1, row3, row5)

    # Determine the player's turn
    winner = 'none'
    x = 1
    while winner == 'none':
        if x % 2 != 0:
            print(f"{player1}'S TURN")
            pos_empty = 'a'
            while pos_empty != 'good':
                play1 = play_turn()
                pos_empty = check_position(play1, row1, row3, row5)
            output1 = assign_position(play1, play_sign1, row1, row3, row5)
        else:
            print(f"{player2}'S TURN")
            pos_empty = 'a'
            while pos_empty != 'good':
                play2 = play_turn()
                pos_empty = check_position(play2, row1, row3, row5)
            output2 = assign_position(play2, play_sign2, row1, row3, row5)

        if x % 2 != 0:
            play = play1
            output = output1
        else:
            play = play2
            output = output2

        if play in [1, 2, 3]:
            row1 = output
        elif play in [4, 5, 6]:
            row3 = output
        else:
            row5 = output

        clear_output()
        display_board(row1, row3, row5)
        winner = win(row1, row3, row5)

        if winner == 'no_winner':
            print('GAMEOVER - IT IS A TIE')
        elif winner == 'winner':
            if x % 2 != 0:
                print(f'{player1} IS THE WINNER')
            else:
                print(f'{player2} IS THE WINNER')

        x = x + 1

    print('\nThank you for playing!')
    play_again = input('\n\nDo you want to play again? (Y/N): ').upper()


