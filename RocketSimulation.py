
import sys
import pygame
import numpy as np
from pygame.locals import *
import preflightpy as pre
import pandas as pd

from data import *
from agent import agentsList, Agent

global screenSize
screenSize = [1920, 1080]


def run_simulation(burn_time):
    params = pre.Parameters("RocketSimulationData/info.json")
    env = pre.Environment(params.env_variables)
    s = pre.System(params, env, burn_time)
    s.launch()


def renderAgents(screen, res, ratio):
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (0, 0, 255), (0, 1080-108, 1920, 108))

    pos = screenSize[1]-158 - res["altitude"]*ratio
    #print("altitude: "+str(res["altitude"])+", pos: "+str(pos))

    pygame.draw.rect(screen, (255, 255, 255), (940, pos, 20, 50))

    pygame.display.update()


def simulateRocket(screen):

    run_simulation(150)

    df = pd.read_csv('RocketSimulationData/Flight.csv')
    result = df.to_dict("index")

    ratio = screenSize[1]/1000000

    interestingPoint = None

    for res in result:
        #print("time: "+str(result[res]["t"])+" Altitude: "+str(result[res]["altitude"]))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        renderAgents(screen, result[res], ratio)
        if result[res]["altitude"] < 800000:
            interestingPoint = result[res]
        pygame.display.update()
    return interestingPoint
