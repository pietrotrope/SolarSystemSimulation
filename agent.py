import numpy as np
import math
from decimal import *

global agentsList
agentsList = []

G = 6.67428e-11

global max_dims
max_dims = np.array([0.0,0.0,0.0])

class Agent:
    radius = 0
    weight = 0
    position = np.array([0.0, 0.0, 0.0])
    speed = np.array([0.0, 0.0, 0.0])
    color = (0, 0, 0)
    name = "NO_NAME_IP"
    

    def __init__(self, name, weight, radius, position, speed):
        self.name = name
        self.weight = weight
        self.radius = radius
        self.position = position
        self.speed = speed
        agentsList.append(self)
        if name == "sun":
            max_dims[0] = position*2

    def getPosition(self):
        return (round(self.position[0]),
                round(self.position[1]))

    def _computeAttraction(self):
        attraction = np.array([np.float128(0.0), np.float128(0.0), np.float128(0.0)], dtype=np.float128)
        for agent in agentsList:
            if agent != self:

                tmpPos = np.float128(agent.position - self.position)
                tmpPos = np.square(tmpPos)
                norm = tmpPos[0]+tmpPos[1]+tmpPos[2]

                forceDir = np.float128(agent.position - self.position)
                forceDir = forceDir / np.linalg.norm(forceDir)

                f = G*forceDir*(self.weight*agent.weight)/(norm)

                acc = f/self.weight

                if self.name == "Moon":
                    if agent.name == "Earth" or agent.name == "Sun":
                        print()
                        print("attracted to "+agent.name+" by: "+str(f))
                        print()

                attraction = attraction + acc

        return attraction

    def updateSpeed(self):
        self.speed = self.speed + 20000*self._computeAttraction()


    @staticmethod
    def newPosition():
        for agent in agentsList:
            agent.updateSpeed()
        for agent in agentsList:
            agent.position = agent.position + 20000*agent.speed
