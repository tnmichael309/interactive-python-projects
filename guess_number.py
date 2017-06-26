# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

secret_number = 0
max_range = 100
remain_guess = 7

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(0,max_range)
    print "New game. Range is from 0 to", str(max_range)
    
    global remain_guess
    if(max_range == 100):
        remain_guess = 7
    else:
        remain_guess = 10
    
    print "Number of remaining guesses is",str(remain_guess)
    print
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global max_range
    max_range = 100
    new_game()
    
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global max_range
    max_range = 1000
    new_game() 

    
def input_guess(guess):
    # main game logic goes here	
    print "Guess was", guess
    global secret_number, remain_guess
    if(remain_guess != 1):
        if(int(guess) > secret_number):
            print "Lower!"
        elif(int(guess) == secret_number):
            print "Correct!"
            print
            new_game()
            return
        else:
            print "Higher!"
        remain_guess = remain_guess - 1
        print
    else:
        if(int(guess) == secret_number):
            print "Correct!"
        else:
            print "You ran out of guesses.  The number was", str(secret_number)
        print
        new_game()
            
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_input("Enter a guess", input_guess, 200)
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
