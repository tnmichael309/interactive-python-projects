# implementation of card game - Memory

import simplegui
import random

closed_cards = range(16) # from pos 0 to pos 15
exposed_pos = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
next_card_to_open = -1 #no card selected in the beginning
current_turn_trial = 0
last_exposed_pos = []
turn_counter = 0
# helper function to initialize globals
def new_game():
    global turn_counter,closed_cards,exposed_pos,next_card_to_open,current_turn_trial,last_exposed_pos
    
    next_card_to_open = -1
    closed_cards = range(16)
    exposed_pos = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    current_turn_trial = 0
    last_exposed_pos = []
    random.shuffle(closed_cards)
    turn_counter = 0
    
def get_card_real_number(num):
    return int(num) // 2

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global next_card_to_open,current_turn_trial,last_exposed_pos,turn_counter
    if pos[1] >= 0 and pos[1] < 100:
        next_card_to_open = pos[0] // 50
        if(not exposed_pos[next_card_to_open]):
            current_turn_trial += 1
            if(current_turn_trial == 2):
                turn_counter += 1
            #print current_turn_trial
            if(current_turn_trial <= 2):
                exposed_pos[next_card_to_open] = True;
                last_exposed_pos.append(next_card_to_open)
            elif(current_turn_trial == 3):
                card1 = get_card_real_number(closed_cards[last_exposed_pos[0]])
                card2 = get_card_real_number(closed_cards[last_exposed_pos[1]])
                
                if(card1 != card2):
                    exposed_pos[last_exposed_pos[0]] = False
                    exposed_pos[last_exposed_pos[1]] = False
                    
                last_exposed_pos = []
                last_exposed_pos.append(next_card_to_open)
                exposed_pos[next_card_to_open] = True;
                current_turn_trial = 1
            else:
                print "Should never be here!"   
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    # draw lines to seperate cards
    for i in range(15):
        canvas.draw_line([(i+1)*50,0],[(i+1)*50,100], 5 ,'Red')
                 
    # draw open cards
    for i in range(16):
       if(exposed_pos[i]):
         cardNum = closed_cards[i];
         text = str(get_card_real_number(cardNum))
         canvas.draw_text(text, [i*50 + 16, 60], 36, "White")
   
    # update label "turn" counter
    label.set_text("Turn = " + str(turn_counter))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric