
import pygame
import sys
import numpy as np
from pygame.locals import *
from agent import agentsList, Agent, max_dims

global screen
global width, height
width = 10**9.18
height = 10**9.18

AU = (149.6e6 * 1000)

global MaxKm
MaxKm = 10000000


def rescalePosition(position):
    rescaledPosition = (
        800 + round(position[0]/width), 400 + round(position[1]/height))
    return rescaledPosition


def drowAndUpdate():
    Agent.newPosition()
    screen.fill((0, 0, 0))
    for agent in agentsList:
        pos = rescalePosition(agent.getPosition())
        pygame.draw.circle(
            screen,
            agent.color,
            pos,
            agent.radius)

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            pos,
            agent.radius, 2)

        textsurface = myfont.render(agent.name, False, (255, 255, 255))
        screen.blit(textsurface, (pos[0]-agent.radius, pos[1]+agent.radius))

        pos = rescalePosition(agent.getPosition())
        print(agent.name+": "+str(pos))

# ================
# PLANETS CREATION
#================#


saturn = Agent("Saturn", np.float128(5.6834 * 10**26), 20, np.array(
    [10.539*AU, AU, 0.1]), np.array([0.0, - 9.68 * 1000, 0.0], dtype=np.float128))


jupiter = Agent("Jupiter", np.float128(1.8982 * 10**27), 20, np.array(
    [6.203*AU, AU, 0.1]), np.array([0.0, - 13.07 * 1000, 0.0], dtype=np.float128))


mars = Agent("Mars", np.float128(6.4171 * 10**23), 12, np.array(
    [2.524*AU, AU, 0.1]), np.array([0.0, - 24.077 * 1000, 0.0], dtype=np.float128))


earth = Agent("Earth", np.float128(5.97237 * 10**24), 14, np.array(
    [2*AU, AU, 0.1]), np.array([0.0, - 29.783 * 1000, 0.00], dtype=np.float128))

moon = Agent("Moon", np.float128(7.342 * 10**22), 5, np.array(
    [(2 + 0.002569)*AU, AU, 0.1]), np.array([0.0, (-1.022 - 29.783)*1000, 0.00], dtype=np.float128))


venus = Agent("Venus", np.float128(4.8685 * 10**24), 8, np.array(
    [1.723*AU, AU, 0.1]), np.array([0.0, -35.02 * 1000, 0.0], dtype=np.float128))


mercury = Agent("Mercury", np.float128(3.3011*10**23), 10, np.array(
    [1.39*AU, AU, 0.1]), np.array([0.0, - 47.36 * 1000, 0.0], dtype=np.float128))


sun = Agent("Sun", np.float128(1.9885 * 10**30), 24, np.array(
    [AU, AU, 0.1]), np.array([0.0, 0.0, 0.0], dtype=np.float128))


earth.color = (102, 255, 255)
sun.color = (255, 255, 0)
mercury.color = (160, 160, 160)
mars.color = (255, 30, 30)
venus.color = (255, 130, 130)
jupiter.color = (135, 94, 19)
saturn.color = (120, 80, 80)
moon.color = (255, 255, 255)

MaxKm = max_dims


pygame.init()
screen = pygame.display.set_mode(
    (round(MaxKm[0]/width), round(MaxKm[1]/height)), 0, 32)
pygame.display.set_caption("Universe")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)

bigFont = pygame.font.SysFont('Comic Sans MS', 20)


auto = False

while True:
    for event in pygame.event.get():

        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.K_SPACE:
                auto = not auto

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            tmp = False
            for agent in agentsList:
                agentPos = rescalePosition(agent.getPosition())
                if (not auto and mousePos[0] - agentPos[0])**2 + (mousePos[1] - agentPos[1])**2 < agent.radius**2:
                    drowAndUpdate()
                    textToShow = agent.name+":       "+"Mass: "+str(agent.weight)+"      Speed: x:"+str(round(agent.speed[0],10))+" y:"+str(round(agent.speed[1],10))+" z:"+str(round(agent.speed[2],10))
                    textsurface = bigFont.render(textToShow, False, (255, 255, 255))
                    screen.blit(textsurface, (100,900))
                    pygame.display.update()

    if auto:
        drowAndUpdate()
        pygame.display.update()
