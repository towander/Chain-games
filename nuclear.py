import pygame
import math
import random
from pygame.locals import *

__author__ = 'wande'

# 2 Initialize the game
pygame.init()
width, height = 600, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]
arrows = []
timer = 100
timer1 = 0
nuclears = [[640, 100]]

# 3 Load images
player = pygame.image.load("resources/images/accelerate.png")
grass = pygame.image.load("resources/images/grass.png")
arrow = pygame.image.load("resources/images/neutrons2.png")
nuclearimg1 = pygame.image.load("resources/images/nuclear2.gif")
nuclearimg = nuclearimg1


# 4 keep looping through
while 1:
    timer -= 1
    indexLock = -1
    # 5 clear the screen before drawing it again
    screen.fill(0)

    # 6 draw the screen elements
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass, (x*100, y*100))
    # 6.1 Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32), position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    # 6.2 - Draw arrows
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*5
        vely=math.sin(bullet[0])*5
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    # 6.3 - Draw badgers
    if timer==0:
        nuclears.append([640, random.randint(50,430)])
        timer=100-(timer1*2)
        if timer1>=35:
            timer1=35
        else:
            timer1+=5
    index=0
    for nuclear in nuclears:
        if nuclear[0]<-64:
            nuclears.pop(index)
        nuclear[0]-=1
         # 6.3.1 - Attack castle
        rect=pygame.Rect(nuclearimg.get_rect())
        rect.top=nuclear[1]
        rect.left=nuclear[0]
        if rect.left<64:
            nuclears.pop(index)
        #6.3.2 - Check for collisions
        index1 = 0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if rect.colliderect(bullrect):
                # print(nuclears.pop(index))
                if indexLock!=index and arrows.pop(index1) and nuclears.pop(index):
                    print(index)
                    pos1 = bullrect
                    pos2 = rect
                    print(bullrect)
                    arrows.append([math.atan2(pos1[1]-pos2[1], pos1[0]-pos2[0]), pos1[0]+32, pos1[1]+32])
                    arrows.append([math.atan2((pos2[1]-pos1[1])*0.2, pos2[0]-pos1[0]), pos1[0]+32, pos1[1]+32])
                    arrows.append([math.atan2(pos2[1]-pos1[1], (pos2[0]-pos1[0])*0.2), pos1[0]+32, pos1[1]+32])
                    indexLock = index
            index1+=1
        # 6.3.3 - Next nuclear
        index+=1
    for nuclear in nuclears:
        screen.blit(nuclearimg, nuclear)

    # 7 update the screen
    pygame.display.flip()
    for event in pygame.event.get():
        # 8 check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            position=pygame.mouse.get_pos()
            indexLock = -1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
    # 9 Move player
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5

