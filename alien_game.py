import pygame
import random
import math
from pygame import mixer

pygame.init()
screen=pygame.display.set_mode((1550,800))   #set the width and the height of the screen
logo=pygame.image.load("galaxy.png")        #load the icon  image of the display
pygame.display.set_icon(logo)               #set the icon
pygame.display.set_caption("Alien Invasion") #set the game title

background_load=pygame.image.load("background.jpg")     #load the background image
background=pygame.transform.scale(background_load,(1550,800))   #resize of the background image

#ally settings#
ally_initial=pygame.image.load("spaceship.png")         #load the spaceship image
ally=pygame.transform.scale(ally_initial,(70,70))       #resize  the spaceship image
ally_X=775                                              # X coordinate of the spaceship 
ally_Y=700                                              # Y coordinate of the spaceship 
ally_move_X=0                                           # movement in the X coordinate (set to 0 beacuse the spacecraft will be moved only by K_LEFT and K_RIGHT. The movement is not continuing)

def ally_limit(x):                                      # this function is made for setting the movement limit of the spaceship along the X axis
    if x>=1460:
        x=1460
    elif x<=10:
        x=10
    return x
def ally_blit(x,y):                                    # this function is made to draw the spaceship on the screen
    screen.blit(ally,(x,y))
#enemies settings#
enemy_initial=pygame.image.load("enemies.png")                       #load the alien image
enemy_scale=pygame.transform.scale(enemy_initial,(70,70))            # resize the alien image  
enemy_rotation=pygame.transform.flip(enemy_scale,False,True)         #flip the alien image on the X axis
enemy=[]                                                             # an empty list that will contains the enemies miniatures
enemy_X=[]                                                           # an empty list that will contains the enemies X coordinates
enemy_Y=[]                                                           # an empty list that will contains the enemies Y coordinates
enemy_move_X=[]                                                      # an empty list that will contains the enemies movement along the X axis
enemy_move_Y=[]                                                      # an empty list that will contains the enemies movement along the X axis
enemy_number=8                                                       # total enemies number

for i in range(enemy_number):                                       
    enemy.append(enemy_rotation)                                    # append the image of the alien into the specific list
    enemy_X.append(random.randint(15,1460))                         # append a random integer between 15 to 1460 into the specific list
    enemy_Y.append(random.randint(20,500))                          # append a random integer between 20 to 500 into the specific list
    enemy_move_X.append(0.8)                                        # append the value of the movement along the X axis into the specific list
    enemy_move_Y.append(10)                                         # append the value of the movement along the Y axis into the specific list

def enemy_blit(x,y,i):                                              # this function is made to draw the enemy on the screen
    screen.blit(enemy[i],(x,y))

def enemy_direction(position_X,position_Y,move_x,move_y):           # this function is made for setting the movement of the alien along the X and the Y axis
    if position_X>=1460:                                            #if the alien X value is >= to 1460, the alien's movement will be shifted in the opposite direction on the X axis and its value on the Y axis will be increased
        move_x=-0.8                                                     
        position_Y+=move_y                                          

    elif position_X<=15:                                            #if the alien X value is <= to 15, the alien's movement will be shifted in the opposite direction on the X axis and its value on the Y axis will be increased
        move_x=0.8
        position_Y+=move_y                                          
    return move_x,position_Y

#bullet settings#
bullet_initial=pygame.image.load("bullet.png")                     #load the bullet image   
bullet=pygame.transform.scale(bullet_initial,(30,30))              # resize of the bullet image
bullet_X=0                                                         # bullet X coordinate will be set to 0
bullet_Y=0                                                         # bullet Y coordinate will be set to 0
bullet_move_Y=5                                                    # bullet movement along the Y axis
bullet_status="ready"                                              # bullet default status (the bullet status will change from 'ready' to 'fire' over the course of the game)

def bullet_blit(x,y):                                              # this function is made to draw the bullet on the screen
    global bullet_status
    bullet_status="fire"
    screen.blit(bullet,(x+20,y+15))                                # the values added to the X axis and to the Y axis are such that the bullet image will be draw at the center of the spacecraft


#score settings#
score_value=0                                                      # set the starting score value
score_X=15                                                         # set the position of the score object
score_Y=15
font=pygame.font.SysFont("tahoma",25)                              # create the font object with a size of 32 pixel
def score_blit(x,y):                                               # this function is made to draw the score on the screen
    score=font.render("Your score is: " + str(score_value),True, (255, 215, 0))              # making the score text Surface
    screen.blit(score,(x,y))                                                                  #draw the score text on the screen
#calculate distance#
def distance(a_X,a_Y,b_X,b_Y):                                     # calculate the distance between the bullet and the enemies
    dist=math.sqrt((math.pow(a_X-b_X,2))+(math.pow(a_Y-b_Y,2)))
    if dist<=27:                                                    #if the distance is lower than 27 px, the function return True
        return True
    else:
        return False
#music background settings#
mixer.music.load("background.wav")                                  # load the background music
mixer.music.play(-1)                                                # play the background music, '-1' for an infinite loop until the program ends
running=True

while running:                                                      
    screen.fill((0,0,0))                                           # fill the screen with a black color in every loop iteration 
    screen.blit(background,(0,0))                                  # draw the background image on the screen
    for event in pygame.event.get():                              
        if event.type==pygame.QUIT:                                # if the player exits the game, the loop  will be interrupted 
            running=False
        if event.type==pygame.KEYDOWN:                             # if a key has been pressed on the keyboard 
            if event.key==pygame.K_LEFT:                           # if the key is the left arrow 
                ally_move_X=-0.8
            if event.key==pygame.K_RIGHT:                          # if the key is the right arrow
                ally_move_X=0.8
            if event.key==pygame.K_SPACE:                          #if the key is the spacebar
                if bullet_status is "ready":                       # this if statement draws the bullet on the screen and plays a laser sound
                    fire=mixer.Sound("laser.wav")               
                    fire.play()
                    bullet_X=ally_X                                #the bullet coordinates are equals to the ally coordinates
                    bullet_Y=ally_Y
                    bullet_status="fire"                           # the bullet status is changed to 'fire'
        if event.type==pygame.KEYUP:                              # if a key has been released on the keyboard 
            ally_move_X=0

    ally_X+=ally_move_X                                           # the value of ally_move_X is added to the ally x coordinate in every loop iteration
    ally_X=ally_limit(ally_X)                                     # the value of ally_X is returned by the function that is made for setting the limit for the spacecraft along the x-axis
    ally_blit(ally_X,ally_Y)

    for i in range(enemy_number):                                # this for iteration sets, for every enemy, the movement along the x-axis and the y-axis, draws the enemy on the screen and calculates the distance
        enemy_X[i]+=enemy_move_X[i]
        enemy_move_X[i],enemy_Y[i]=enemy_direction(enemy_X[i],enemy_Y[i],enemy_move_X[i],enemy_move_Y[i])
        enemy_blit(enemy_X[i],enemy_Y[i],i)
        dist=distance(bullet_X,bullet_Y,enemy_X[i],enemy_Y[i])
        if dist:                                                       # if the distance is lower than 27 pixels, will be load a sound, the score value will be increased and will be created a new enemy with new coordinates
            bullet_status="ready"
            enemy_hit=mixer.Sound("explosion.wav")
            enemy_hit.play()
            score_value+=1
            enemy_X[i]=random.randint(15,1460)
            enemy_Y[i]=random.randint(20,500)

    if bullet_status is "fire":                                       # if the bullet is displayed on the screen, its status is 'fire' 
        bullet_Y-=bullet_move_Y
        bullet_blit(bullet_X,bullet_Y)
        if bullet_Y<=15:                                               # if the bullet's postion along the y-axis is lower than 15 pixels, the status will be changed to 'ready' and the bullet will disappears from the screen'.Now, when the player presses the spacebar, a new bullet will be displayed on the screen 
            bullet_status="ready"
    score_blit(score_X,score_Y)
    pygame.display.update()                                                   # this command updates the display to reflect any changes detected in the current loop. 