# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group, canvas):
    rs = set([])
    
    for member in group:
        if member.update() == False:
            rs.add(member)
        else:
            pass
        member.draw(canvas)
    group.difference_update(rs)
    
def group_collide(group, other_object):
    global explosion_group
    rs = set([])
    is_collide = False
    zero_vector = [0,0]
    for member in group:
        if member.collide(other_object):
            rs.add(member)
            explosion_group.add(Sprite(member.get_position(),zero_vector , 0, 0, explosion_image, explosion_info,explosion_sound))
            is_collide = True
    
    group.difference_update(rs)
    return is_collide

def group_group_collide(group1, group2):
    rs = set([])
    number = 0
    for member in group1:
         if group_collide(group2, member):
                rs.add(member)
                number += 1
    group1.difference_update(rs)
    return number

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.acc = 0.5
        self.friction_coefficient = 0.03
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if not self.thrust:
            canvas.draw_image(ship_image, ship_info.get_center(), ship_info.get_size(), self.pos, ship_info.get_size(), self.angle)
        else:
            canvas.draw_image(ship_image, [135, 45], ship_info.get_size(), self.pos, ship_info.get_size(), self.angle)
        
    def set_ship_state(self, direction, is_on):
        if is_on:
            if direction == 'LEFT':
                self.angle_vel = -0.05
            if direction == 'RIGHT':
                self.angle_vel = 0.05
            if direction == 'UP':
                self.thrust = True
                ship_thrust_sound.play()
        else:
            if direction == 'LEFT' or direction == 'RIGHT':
                self.angle_vel = 0
            if direction == 'UP':
                self.thrust = False
                ship_thrust_sound.pause()
    
    def update(self):
        #update angular velocity
        self.angle = (self.angle + self.angle_vel)
        
        #update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        #update friction
        self.vel[0] *= (1-self.friction_coefficient)
        self.vel[1] *= (1-self.friction_coefficient) 
        
        #update velocity
        forward = [math.cos(self.angle), math.sin(self.angle)]
        
        if self.thrust:
            self.vel[0] += forward[0]*self.acc
            self.vel[1] += forward[1]*self.acc
            
    def shoot(self):
        global missile_group
        forward = [math.cos(self.angle), math.sin(self.angle)]
        ini_pos = [self.pos[0] + self.image_size[0]*forward[0]/2, self.pos[1] + self.image_size[1]*forward[1]/2]
        ini_vel = [self.vel[0] + forward[0]*3 ,self.vel[1]+ forward[1]*3]
        ini_angel = 0
        ini_angel_vel = 0
        
        missile_group.add(Sprite(ini_pos, ini_vel, ini_angel, ini_angel_vel, missile_image, missile_info, missile_sound))
    
    def get_position(self):
        return self.pos
    def get_radius(self):
        return self.radius   
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated == True:
            size = self.image_size
            canvas.draw_image(self.image, [self.image_center[0] + size[0]*self.age, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else: 
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
            
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]       
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.age += 1
        if self.age > self.lifespan:
            return False
        else:
            return True
        
    def is_out_of_screen(self):
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            return True
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            return True
        return False
    def collide(self, other):
        distance = dist(self.pos, other.get_position())
        if distance <= (self.radius + other.get_radius()):
            return True
        else:
            return False
        
    def get_position(self):
        return self.pos
    def get_radius(self):
        return self.radius
    
def draw(canvas):
    global time, lives, score, rock_group, is_started, missile_group, my_ship, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if is_started:
        # update and draw ship
        my_ship.update()
        my_ship.draw(canvas)
        
        # draw groups of rocks and missles
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group (explosion_group, canvas)
        score += group_group_collide(missile_group, rock_group)
        
        is_collide_with_rock = group_collide(rock_group, my_ship)
        if is_collide_with_rock:
            lives -= 1
        if lives == 0:
            is_started = False
            lives = 3
            score = 0
            rock_group = set([])
            missile_group = set([])
            explosion_group = set([])
            my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
            soundtrack.rewind()
            soundtrack.pause()
    else:       
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], [450,250], 0)
         
    
    # show lives and scores
    canvas.draw_text("Lives: " + str(lives), (10, 35), 25, 'White')
    canvas.draw_text("Score: " + str(score), (160, 35), 25, 'White')
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    
    #set limit of number of rocks
    if(len(rock_group) == 10): 
        return;
    
    ini_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    ini_vel = [(float)(random.randrange(0, 100)) / 100.0, (float)(random.randrange(0, 100))/100.0]
    ini_angel = random.randrange(0, 6)
    if random.randrange(0, 2) == 1:
        ini_angel_vel = (float)(random.randrange(0, 1000)) / 5000.0
    else:
        ini_angel_vel = -1 * (float)(random.randrange(0, 1000)) / 5000.0
    
    a_rock = Sprite(ini_pos, ini_vel, ini_angel, ini_angel_vel, asteroid_image, asteroid_info)
    if not a_rock.collide(my_ship):
        rock_group.add(a_rock)

def key_down_handler(key):
    global my_ship
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_ship_state('UP', True)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.set_ship_state('RIGHT', True)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.set_ship_state('LEFT', True)
    elif chr(key) == ' ':
        my_ship.shoot();
        
def key_up_handler(key):
    global my_ship
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_ship_state('UP', False)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.set_ship_state('RIGHT', False)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.set_ship_state('LEFT', False)
    
def mouse_handler(position):
    global is_started
    is_started = True
    soundtrack.play()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([]);
missile_group = set([]);
explosion_group = set([]);
is_started = False

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
