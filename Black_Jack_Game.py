'''
This is a code to build a Black Jack Game, using object-oriented programming

The game involves a computer dealer and a human player
By default, a player starts the game with $10,000 worth of chips
The dealer would only place a maximum of 5 times the players buy-in
The minimum a player can bet for each play turn is $500

HERE IS HOW THE GAME WORKS
The goal of the game is to get a total card value closer to 21 than the dealer
At the start of the game, both the player and computer dealer is given 2 cards
They may both choose to hit for more cards or stay (stop receiving cards)
Whoever has a total card value closer to 21 wins that round and get the opponent's chips placed
However, if the total card value exceeds 21 while the opponent's total is below 21, the player exceeding 21
bursts and losses that round. The opponent gets the chips placed

Jacks, Queen and King count as a value of 10
Aces can count as either 1 or 11, whichever the player or dealer chooses. Counting an Ace as 1 is softening the Ace
All other cards count as the face value of the card

p.s. Images of the cards are not displayed. Only the values, rank and suit of the cards are given
'''

import random
from IPython.display import clear_output
from colorama import Fore


# Define the default player buy in
default_buy_in = 10000

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six':6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Create a card class
class Card:
    # Class to hold card objects
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    # To unable printing the cards
    def __str__(self):
        return str(self.value) + ' ' + self.rank + ' of ' + self.suit

    # Method to soften an ace
    def change_ace(self):
        if self.rank == 'Ace':
            self.rank = 'Soft Ace'
            self.value = 1
        elif self.rank == 'Soft Ace':
            self.rank = 'Ace'
            self.value = 11

# Create a Deck of Cards
class Deck:
    # The entire card deck
    def __init__(self):
        self.full_deck = []
        for suit in suits:
            for rank in ranks:
               created_card = Card(rank,suit)
               self.full_deck.append(created_card)

    # Method to shuffle the deck
    def shuffle(self):
        # Method to shuffle cards
        random.shuffle(self.full_deck)

    # Method to deal one card
    def deal_one(self):
        return self.full_deck.pop(0)

    # Method to deal two cards
    def deal_two(self):
        return list((self.full_deck.pop(0), self.full_deck.pop(0)))


class Account:
    def __init__(self, player_balance=default_buy_in):
        self.player_balance = player_balance
        self.dealer_balance = self.player_balance * 5

    # Ask the player how much he/she wants to place for a bet
    # The amount cannot be more than his/her available balance
    # The minimum amount allowed is $500
    def place_bet(self):
        bet = ''
        while bet.isdigit() == False or (float(bet) > self.player_balance) or float(bet) < 500:
            bet = input('\nHow much chips do you want to place for a bet?  ')
            if bet.isdigit() == False:
                print('Please enter a valid amount')
                continue
            elif float(bet) > self.player_balance:
                print('Insufficient chips available to place bet')
                print(f'Your available chips is worth {self.player_balance} \nPlease enter an bet amount again')
                continue
            elif float(bet) < 500:
                print('The minimum bet you can place is $500')
                print(f'Your available chips are worth {self.player_balance} \n Please enter an bet amount again')
                continue
            else:
                bet = float(bet)
                return bet

    # Method when player wins the bet
    def player_win(self, bet):
        self.player_balance += bet
        self.dealer_balance -= bet
        print(f"Player's new balance is {self.player_balance}\n")

    # Method when player losses the bet
    def player_lose(self, bet):
        self.player_balance -= bet
        self.dealer_balance += bet
        print(f"Player's new balance is {self.player_balance}\n")

    # Method for a tie game
    def tie_game(self):
        print(f"Player's new balance is {self.player_balance}\n")

# FUNCTIONS
# To find the position of the ace on hand (Needed for dealer algorithm to identify the position of the ace on hand)
def find_ace(card_value_list, status='hard'):
    ace_index = 0
    ace_found = False
    for num in card_value_list:
        if (num == 11 and status == 'hard') or (num == 1 and status == 'soft'):
            ace_found = True
            break
        else:
            ace_index += 1
    if ace_found:
        return ace_index

# Get all cards on hard in a list (Needed for dealer algorithm to check if there is an ace on hand)
def card_list(card_list):
    cards = []
    for Card in card_list:
        cards.append(Card.value)
    return cards

# Get the total value of all cards on hand
def total_card_value(card_list):
    card_value = 0
    for Card in card_list:
        card_value += Card.value
    return card_value

# GAME LOGIC
print("WELCOME TO THIS CHIOMA'S CASINO!\nYOU WILL BE PLAYING A BLACK JACK GAME")

# Assign created classes to variables
game_account = Account()

# Game on
play = "Y"
while play in ['Y', 'YES', '1']:
    game_deck = Deck()

    #Call placebet
    bet = game_account.place_bet()
    print(f'You have placed a bet of ${bet}')

    #Shuffle the cards
    game_deck.shuffle()

    # **************************************** DEALER'S GAME **************************************** #
    ''' 
        A simple algorithm to play as a dealer
        If the dealers total is less than 15, dealer will always deal more
        If the dealer's total more than 21 or less than 18 and there is a hard ace, the dealer will soften the ace
        If the dealer's total is between 8 and 11 and there is a soft ace, the dealer will change that to a hard ace
        If the dealer's total is 15 or 16, a coin toss (by the algorithm) will determinw whether the dealer will or will
        not deal more cards
        In any case other than those above, the dealer will not deal more cards
    '''


    # Deal the dealer's first two cards. Each time a new card we dealt, we append to dealer_cards
    dealer_cards = []
    first_deal = game_deck.deal_two()
    dealer_cards.extend(first_deal)

    # Algorithm for the dealer (computer) to place the game
    Loop = True
    while Loop:
        dealer_card_list = card_list(dealer_cards)
        dealer_cards_value = total_card_value(dealer_cards)

        if (8 <= dealer_cards_value <= 11) and 1 in dealer_card_list:
            # when cards total value is between 8 and 11 and there is a soft ace on hand
            idx = ind_ace(dealer_card_list, 'soft')
            dealer_cards[idx].change_ace()

        elif dealer_cards_value < 15:
            # when card total value is less than 16
            next_deal = game_deck.deal_one()
            dealer_cards.append(next_deal)

        elif (dealer_cards_value > 21 or dealer_cards_value < 18) and 11 in dealer_card_list:
            # when card total value less then 17 or more then than 21 and there is a hard ace on hand
            idx = find_ace(dealer_card_list)
            dealer_cards[idx].change_ace()
            next_deal = game_deck.deal_one()
            dealer_cards.append(next_deal)

        elif dealer_cards_value < 17:
            # when card total value is 15 0r 16, do a coin toss to gamble whether or not to deal more
            coin_toss = random.randint(1, 2)
            if coin_toss == 1:
                next_deal = game_deck.deal_one()
                dealer_cards.append(next_deal)
        else:
            # In any other case, do not deal more
            Loop = False
            break

    # Dealer's card value after algorithm plays the dealer's game
    dealer_cards_value = total_card_value(dealer_cards)


    # **************************************** PLAYER'S GAME **************************************** #

    # Deal the player's first two cards. Each time a new card we dealt, we append to player_cards
    player_cards = []
    first_play_cards = game_deck.deal_two()
    player_cards.extend(first_play_cards )

    # Display the number of cards the dealer dealt and the dealer's first card.
    print(f'\nThe Dealer has {len(dealer_cards)} cards.\nThe Dealer first card:{dealer_cards[0]} \n')
    # Display the player's two first cards
    print(f'Your Cards: \n{player_cards[0]} and; \n{player_cards[1]} ')

    # Check if the player has an ace and inform him/her that the ace can be softened at any point in the game
    player_card_list = card_list(player_cards)
    if 11 in player_card_list:
        print(
            f'You have {player_card_list.count(11)} ace card(s) on hand. You may choose to soften the ace(s) when you finish hitting for more cards')

    # Subsequent Hits
    player_hit = input('Do you want to deal more cards? Enter "Y" or "Yes" or "1" to deal another card: ').upper()
    while player_hit in ['Y', 'YES', '1']:
        next_player_deal = game_deck.deal_one()
        player_cards.append(next_player_deal)

        # Display the dealer cards and all the player cards on hand
        print(f'\nThe Dealer has {len(dealer_cards)} cards.\nThe Dealer first card:{dealer_cards[0]} \n')
        print(f'Your Cards: \n{player_cards[0]} \n{player_cards[1]} \n{player_cards[2]}')
        if len(player_cards) > 3:
            for num in range(3, len(player_cards)):
                print(f'{player_cards[num]}')

        # Check if the player has an ace and inform him/her that the ace can be softened at any point in the game
        player_card_list = card_list(player_cards)
        player_cards_value = total_card_value(player_cards)
        if 11 in player_card_list:
            print(f'You have {player_card_list.count(11)} ace card(s) on hand. You may choose to soften the ace(s) when you finish hitting for more cards')

        # Check if the player can continue to hit
        if player_cards_value - (player_card_list.count(11) * 10) > 21:
            print(f'You can no longer hit for more cards')
            break
        else:
            # Ask again if the play want to continue to hit
            player_hit = input('Do you want to deal more cards? Enter "Y" or "Yes" or "1" to deal another card: ').upper()

    # Ask player if they want to soften ace on hand
    while 11 in player_card_list:
        player_soften_ace = input('Do you want to soften an ace? Once you choose to soften an ace, it cannot be reversed\
                                                \nEnter "Y" or "Yes" or "1" to soften an ace: ').upper()
        if player_soften_ace in ['Y', 'YES', '1']:
            idx = find_ace(player_card_list)
            player_cards[idx].change_ace()
            player_card_list = card_list(player_cards)
        else:
            break

    # Player's card value he's after he stops hitting
    player_cards_value = total_card_value(player_cards)

    # Clear screen and display bet amount again
    clear_output()
    print(Fore.BLUE + f'\nBet Amount ${bet}\n')

    # Determine the winner
    if dealer_cards_value > 21 and player_cards_value > 21:
        print('Player and Dealer Burst. No one wins the bet')
        game_account.tie_game()
    elif dealer_cards_value > 21 >= player_cards_value:
        print('Dealer Burst. Player wins the bet')
        game_account.player_win(bet)
    elif dealer_cards_value <= 21 < player_cards_value:
        print('Player Burst. Dealer wins the bet')
        game_account.player_lose(bet)
    elif dealer_cards_value > player_cards_value:
        print('Dealer Wins')
        game_account.player_lose(bet)
    elif dealer_cards_value < player_cards_value:
        print('Player Wins')
        game_account.player_win(bet)
    elif dealer_cards_value == player_cards_value:
        print('Tie Game. No one wins the bet')
        game_account.tie_game()

    # Display all the dealer's cards and dealer's total card value
    print(Fore.MAGENTA + 'Dealers Cards:')
    for num in range(0, len(dealer_cards)):
        print(f'{dealer_cards[num]}')
    print(f"Dealer's Total Value {dealer_cards_value} \n")

    # Display all the player's cards and player's total cards value
    print(Fore.CYAN + 'Your Cards:')
    for num in range(0, len(player_cards)):
        print(f'{player_cards[num]}')
    print(f"Your Total Value {player_cards_value}")

    if game_account.player_balance < 500:
        print(Fore.RED + f'\nYou do not have sufficient chips to play another game!\nYour balance is {game_account.player_balance}\n')
        break
    elif game_account.dealer_balance < bet:
        print(Fore.RED + f'\n You can no longer play. The dealer is out of chips \nYour balance is {game_account.player_balance}\n')
        break

    # Ask if player want to play another round
    play = ""
    while play not in ['Y', 'YES', '1', 'N', 'NO', 'EXIT', '0']:
        play = input(Fore.WHITE + '\nDO YOU WANT TO PLAY AGAIN? Enter "Y" or "Yes" or "1" to play again. Enter "N", "NO", "EXIT" OR "0" to quit:').upper()

print(Fore.BLUE + '\nThank you for playing!')