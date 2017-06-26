# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 950x392 - source: jfitz.com
CARD_SIZE = (73, 98)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize global variables
deck = []
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", self.suit, self.rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []
        self.card_space = 73
        
    def __str__(self):
        card_list_str = ""
        for card in self.card_list:
            card_list_str += str(card)
        return card_list_str

    def add_card(self, card):
        self.card_list.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if don't bust
    def get_value(self):
        is_able_to_add_10 = False
        card_sum = 0
        for card in self.card_list:
            value = VALUES[card.get_rank()]
            if(value == 1):
                is_able_to_add_10 = True
            card_sum += value
        if is_able_to_add_10 and card_sum <= 11:
            card_sum += 10
        return card_sum
    
    def busted(self):
        if(self.get_value() > 21):
            return True
        return False
    
    def draw(self, canvas, p):
       current_pos = p
       for card in self.card_list:
            card.draw(canvas, current_pos)
            current_pos[0] += self.card_space
 
        
# define deck class
class Deck:
    def __init__(self):
        self.card_list = []
        for i in range(4):
            for j in range(13):
                new_card = Card(SUITS[i],RANKS[j])
                self.card_list.append(new_card)
        self.shuffle()
        
    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.card_list)

    def deal_card(self):
        return self.card_list.pop()


#global variables for dealer, player and the deck
deck = Deck()
dealer = Hand()
player = Hand()

#define callbacks for buttons
def deal():
    global outcome, in_play, deck, dealer, player, score

    if in_play:
        outcome = "Dealer wins"
        score -= 1
        in_play = False
        return
    
    # your code goes here
    deck = Deck()
    dealer = Hand()
    player = Hand()
    
    for i in range(2):
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
    
    outcome = ""
    in_play = True

def hit():
    global outcome, in_play, deck, dealer, player,score
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
    else:
        return
    # if busted, assign an message to outcome, update in_play and score
    if player.busted():
        outcome = "You have busted, Dealer wins"
        score -= 1
        in_play = False
    
def stand():
    global outcome, in_play, deck, dealer, player,score
    
    if not in_play:
        return
    else:    
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while(dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
            
        # assign a message to outcome, update in_play and score
        if dealer.busted():
            outcome = "Dealer have busted, Player wins"
            score += 1
        else:
            if(dealer.get_value() >= player.get_value()):
                outcome = "Dealer wins"
                score -= 1
            else:
                outcome = "Player wins"
                score += 1
        in_play = False
                
def draw(canvas):
    canvas.draw_text("Blackjack", [200, 50], 50, 'Black')
    canvas.draw_text("Player: ", [20, 100], 20, 'Black')
    player.draw(canvas, [100,100])
    canvas.draw_text("Dealer: ", [20, 300], 20, 'Red')
    dealer.draw(canvas, [100,300])
    
    canvas.draw_text(outcome, [200, 430], 20, 'Black')
    if(in_play):
        canvas.draw_text("Hit or stand?", [200, 450], 20, 'Black')
        card_loc = (CARD_BACK_SIZE[0] * 0.5 , CARD_BACK_SIZE[1] * 0.5 )
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [100+0.5*CARD_SIZE[0],300+0.5*CARD_SIZE[1]], CARD_SIZE)
    else:
        canvas.draw_text("New deal?", [200, 450], 20, 'Black')
    
    canvas.draw_text("Score: " + str(score), [450, 50], 20, 'White')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()


# Grading rubric - 18 pts total (scaled to 100)

# 1 pt - The program opens a frame with the title "Blackjack" appearing on the canvas.
# 3 pts - The program displays 3 buttons ("Deal", "Hit" and "Stand") in the control area. (1 pt per button)
# 2 pts - The program graphically displays the player's hand using card sprites. 
#		(1 pt if text is displayed in the console instead) 
# 2 pts - The program graphically displays the dealer's hand using card sprites. 
#		Displaying both of the dealer's cards face up is allowable when evaluating this bullet. 
#		(1 pt if text displayed in the console instead)
# 1 pt - Hitting the "Deal" button deals out new hands to the player and dealer.
# 1 pt - Hitting the "Hit" button deals another card to the player. 
# 1 pt - Hitting the "Stand" button deals cards to the dealer as necessary.
# 1 pt - The program correctly recognizes the player busting. 
# 1 pt - The program correctly recognizes the dealer busting. 
# 1 pt - The program correctly computes hand values and declares a winner. 
#		Evalute based on player/dealer winner messages. 
# 1 pt - The dealer's hole card is hidden until the hand is over when it is then displayed.
# 2 pts - The program accurately prompts the player for an action with the messages 
#        "Hit or stand?" and "New deal?". (1 pt per message)
# 1 pt - The program keeps score correctly.