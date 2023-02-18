# Clean up the comments within this program
# Use comments to explain the why's and how's of your code.
# Avoid using comments to explain what your program does.
import random
from IPython.display import clear_output

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank + " of " + self.suit
    
class Deck:
    #initialize a list to hold a deck of cards
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.cards)
    def deal_one(self):
        return self.cards.pop()
    
class Hand:
    def __init__(self):
        #create an empty list for holding cards
        self.cards = []
        self.value = 0
        self.aces = 0
    #method to display the cards being played
    def __str__(self):
        show_cards = ''
        for card in self.cards:
            show_cards += card.__str__() + ", "
        return show_cards[:-2]
            
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1
    #adjust for aces
    def adjust_ace(self):
        if self.aces > 1 and self.value > 21:
            self.value -= 10
            self.aces -= 1

#chip class to keep track of player's chips
class Chip():
    def __init__(self):
        self.total = 100
        self.bet = 0
    def lose_bet(self):
        self.total -= self.bet
        print(f"\n-{self.bet} chips")
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
        print(f"\n+{self.bet} chips")
        self.bet = 0

def hit(hand,deck):
    card = deck.deal_one()
    hand.add_card(card)

def hit_or_stand(hand,deck):
    global playing
    response = 'wrong'
    
    while hand.value < 21 and playing:
        response = input("Player, hit or stand. 'h','s': ")[0].lower()
        if response == 'h':
            hit(hand,deck)
            print(f"Player's hand: {hand}, ({hand.value})\n")
        elif response == 's':
            break
        pass

def take_bet(chips):
    bet = 0
    while playing and int(bet) > chips.total or int(bet) <= 0:
        bet = input("Player, how many chips do you want to bet?: ")
        if bet.isdigit() != True:
            bet = 0
            continue
    chips.bet = int(bet)

#define winning conditions
def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def dealer_busts(chips):
    print("Dealer busted. Player wins!")
    chips.win_bet()

def player_wins(chips):
    print("Player beats dealer!")
    chips.win_bet()

def player_busts(chips):
    print("Player busted! Dealer wins!")
    chips.lose_bet()

def push(chips):
    chips.bet = 0
    print("It's a draw!")
    print("+0 chips")
    pass

#hide the dealer's first card and show the rest
def display_some(player,dealer):
    dealer_some = dealer.__str__()
    print(f"\nPlayer's cards: {player} ({player.value})")
    print(f"\nDealer's cards: ?{dealer_some[dealer_some.index(', '):]}\n")
    
#show all cards being played
def display_all(player,dealer):
    print(f"Player's cards: {player} ({player.value})")
    print(f"Dealer's cards: {dealer} ({dealer.value})\n")

#welcome the player
print("Welcome to Blackjack!")
#initialize the player's chips
chips = Chip()

#putting the pieces together
while True:
    #create a deck and give 2 cards to each player/dealer.
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    dealer = Hand()
    
    for n in range(2):
        player.add_card(deck.deal_one())
        dealer.add_card(deck.deal_one())
    
    #keep track of the player's chips
    print(f"Player has {chips.total} chips.")
    
    #prompt the player for their bet
    take_bet(chips)
    
    #display cards, but hide the dealer's first card
    display_some(player,dealer)
    
    while playing:
        #prompt the player to hit or stand
        hit_or_stand(player,deck)
        pass
        
        #dealer hits if value < 17
        while dealer.value < 17:
            hit(dealer,deck)
        
        if player.value > 21:
            player_busts(chips)
            break
        
        #clear the screen
        clear_output()
        
        #dealer busts
        if dealer.value > 21:
            dealer_busts(chips)
            break
            
        #display all cards
        display_all(player,dealer)
        
        #dealer wins
        if dealer.value > player.value:
            dealer_wins(chips)
        #player wins
        elif player.value > dealer.value:
            player_wins(chips)
        #tie game
        else:
            push(chips)
        
        break
        
        
    #display the player's chips
    print(f"Player's chips: {chips.total}")
        
    #ask to play again
    replay = False
    
    while replay not in ['y','n']:
        replay = input("Do you want to play again? Y/N: ")[0].lower()
    if replay == 'y':
        playing = True
        clear_output()
    else:
        break
    clear_output()
print("Thanks for playing!")

