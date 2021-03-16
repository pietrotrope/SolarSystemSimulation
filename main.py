
import sys
import pygame
import numpy as np
from pygame.locals import *

from data import *
from agent import agentsList, Agent

global screen
global width, height
width = 10**9.18
height = 10**9.18

cameraPosition = (0, 0)

scaleFactor = 1


global screenSize
screenSize = [1920, 1080]

background = pygame.image.load("Images/Background.jpg")
imagerect = background.get_rect()


# ===============
# Support methods
# ===============

def rescalePosition(position):
    rescaledPosition = (
        round(screenSize[0]/2) + round(position[0]/width) + cameraPosition[0],
        round(screenSize[1]/2) + round(position[1]/height) + cameraPosition[1])
    return rescaledPosition


def renderAgents(agentToInfo=None):
    screen.fill((0, 0, 0))
    screen.blit(background, imagerect)

    for agent in agentsList:
        pos = rescalePosition(agent.getPosition())
        pygame.draw.circle(
            screen,
            agent.color,
            pos,
            round(agent.radius*scaleFactor))

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            pos,
            round(agent.radius*scaleFactor), 2)

        textsurface = myfont.render(agent.name, False, (255, 255, 255))
        screen.blit(
            textsurface, (pos[0]-round(agent.radius*scaleFactor),
                          pos[1]+round(agent.radius*scaleFactor)))

        pos = rescalePosition(agent.getPosition())
        print(agent.name+": "+str(pos))

    if (agentToInfo != None):
        textToShow = agentToInfo.name+":       "+"Mass: "+str(agentToInfo.mass)+"      Speed: x:"+str(round(
            agentToInfo.speed[0], 10))+" y:"+str(round(agentToInfo.speed[1], 10))+" z:"+str(round(agentToInfo.speed[2], 10))
        textsurface = bigFont.render(
            textToShow, False, (255, 255, 255))
        screen.blit(textsurface, (100, 900))
    pygame.display.update()


# ===============================================
# IMPORT DATA (planets, satellites, asteroids...)
# ===============================================
for name in data:
    agent = Agent(name,
                  data[name]["mass"],
                  data[name]["radius"],
                  np.array(data[name]["initialPosition"]),
                  np.array(data[name]["initialVelocity"]))
    agent.color = data[name]["color"]


# ================
# Start simulation
# ================

pygame.init()
screen = pygame.display.set_mode(
    (screenSize[0], screenSize[1]), 0, 32)
pygame.display.set_caption("Universe")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)

bigFont = pygame.font.SysFont('Comic Sans MS', 20)


auto = True
selectedAgent = None
change = False

oldPos = pygame.mouse.get_pos()

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
            found = False
            for agent in agentsList:
                agentPos = rescalePosition(agent.getPosition())
                if (mousePos[0] - agentPos[0])**2 + (mousePos[1] - agentPos[1])**2 < round(agent.radius*scaleFactor)**2:
                    selectedAgent = agent
                    found = True
            if not found:
                selectedAgent = None

            if event.button == 1:
                change = True

            if event.button == 4:
                width = width - 10**7
                height = height - 10**7
                scaleFactor = scaleFactor + 0.01

            if event.button == 5:
                width = width + 10**7
                height = height + 10**7
                scaleFactor = scaleFactor - 0.01
        
        if event.type == pygame.locals.MOUSEBUTTONUP:
            if event.button == 1:
                change = False


    if auto:
        Agent.newPosition()

    if change:
        mousePos = pygame.mouse.get_pos()
        x = oldPos[0] - mousePos[0]
        y = oldPos[1] - mousePos[1]
        if x != 0 or y != 0:
            cameraPosition = (cameraPosition[0] - x,
                              cameraPosition[1] - y)

    renderAgents(selectedAgent)
    pygame.display.update()
    oldPos = pygame.mouse.get_pos()
