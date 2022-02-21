# Introduction
print("WELCOME TO GUESS ME!")
print("I'm thinking of a number between 1 and 100")
print("If your guess is more than 10 away from my number, I'll tell you you're COLD")
print("If your guess is within 10 of my number, I'll tell you you're WARM")
print("If your guess is farther than your most recent guess, I'll say you're getting COLDER")
print("If your guess is closer than your most recent guess, I'll say you're getting WARMER")
print("LET'S PLAY!")
50
# Get the Special Random Number
from random import randint

reply = 'y'
while reply == 'y':
    special_no = randint(1, 100)


    # Function to get user input
    def user_input():
        result = 'x'
        while result.isdigit() == False:
            result = input('Enter a number now (1 to 100):')
            if result.isdigit() == False:
                print('Invalid Number')
        return int(result)


    # Request gamer's first guess
    first_guess = user_input()

    # Check first guess
    first_diff = abs(first_guess - special_no)
    if first_guess < 1 or first_guess > 100:
        print('OUT OF BOUNDS')
    elif first_diff < 11:
        print('WARM')
    else:
        print('COLD')

    # Assign first guess outputs to variables to be used in a loop
    prev_diff = first_diff
    sub_guess = first_guess
    guess_no = 1

    # Loop through subsequent guesses
    while sub_guess != special_no:
        sub_guess = user_input()

        sub_diff = abs(sub_guess - special_no)

        if (sub_guess < 1 or sub_guess > 100) and (sub_diff < prev_diff):
            print('OUT OF BOUNDS! WARMER')
        elif (sub_guess < 1 or sub_guess > 100) and (sub_diff > prev_diff):
            print('OUT OF BOUNDS! COLDER')
        elif sub_diff < prev_diff:
            print("WARMER")
        else:
            print('COLDER')
        prev_diff = sub_diff
        guess_no += 1

    # You've finally guessed right
    print('You have guessed correctly!\nThe special number is {}. \nIt took you {} guesses.'.format(special_no, guess_no))

    reply=input('\ndo you want to play again (y=yes n=no)')