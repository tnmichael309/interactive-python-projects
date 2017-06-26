# define global variables
import simplegui    

is_able_to_increase_time = False
has_been_started = False
time = 0
num_of_trial = 0
num_of_success = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minute = t/600
    seconds = t%600
    resultStr = str(minute) + ":" + str(seconds/100) + str((seconds%100)/10) + "." + str(seconds%10)
    return resultStr 
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    global is_able_to_increase_time,time,has_been_started
    is_able_to_increase_time = True
    if(not has_been_started):
        time = 0
        has_been_started = True
      

def stop_button_handler():
    global is_able_to_increase_time,num_of_trial,num_of_success
    if(has_been_started and is_able_to_increase_time):
        num_of_trial = num_of_trial + 1
        if(time % 10 == 0):
            num_of_success = num_of_success + 1
    is_able_to_increase_time = False
    
def reset_button_handler():
    global is_able_to_increase_time,time,has_been_started,num_of_trial,num_of_success
    is_able_to_increase_time = False
    time = 0
    has_been_started = False
    num_of_trial = 0
    num_of_success = 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    global time
    if(is_able_to_increase_time):
        time = time + 1
        
# define draw handler
def draw(canvas):
    canvas.draw_text(format(time), (125, 175), 100, "White");
    playing_status = str(num_of_success) + "/" + str(num_of_trial)
    canvas.draw_text(playing_status, (400, 50), 50, "Green");
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 500, 300)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start_button_handler, 100)
frame.add_button("Stop", stop_button_handler,100)
frame.add_button("Reset", reset_button_handler,100)

# start frame
timer = simplegui.create_timer(100, tick)

# Please remember to review the grading rubric
frame.start()
timer.start()