import numpy as np
import math

global agentsList
agentsList = []

G = 6.67428e-11  # Gravitational costant
tick = 25000


class Agent:
    radius = 0
    mass = 0
    position = np.array([0.0, 0.0, 0.0])
    speed = np.array([0.0, 0.0, 0.0])
    color = (0, 0, 0)
    name = "NO_NAME_IP"

    def __init__(self, name, mass, radius, position, speed):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = position
        self.speed = speed
        agentsList.append(self)

    def getPosition(self):
        """
        Returns 2d rounded position to use in pygame simulation
        """
        return (round(self.position[0]),
                round(self.position[1]))

    def _computeTotalForce(self):
        """
        Compute force in the time t+tick for the agent 
        """
        # Initialize a force vector of zeros
        finalForce = np.array([np.float128(0.0), np.float128(
            0.0), np.float128(0.0)], dtype=np.float128)

        # Update force using gravitational law to compute
        #  attraction force between the current agent and all the other agents
        for agent in agentsList:
            if agent != self:
                force = _computeForce(self, agent)
                finalForce = finalForce + force

        return finalForce

    def updateSpeed(self):
        self.speed = self.speed + tick*self._computeTotalForce()

    @staticmethod
    def newPosition():
        """
        Compute the speed of each agent and then update the position of
        the agents using the computed speed
        """

        for agent in agentsList:
            agent.updateSpeed()
        for agent in agentsList:
            agent.position = agent.position + tick*agent.speed


def _computeForce(agent1, agent2):
    """
    Compute force using the gravitational universal law
    """
    tmpPos = np.float128(agent2.position - agent1.position)
    tmpPos = np.square(tmpPos)
    norm = tmpPos[0]+tmpPos[1]+tmpPos[2]

    forceDir = np.float128(agent2.position - agent1.position)
    forceDir = forceDir / np.linalg.norm(forceDir)

    f = G*forceDir*(agent1.mass*agent2.mass)/(norm)

    return f/agent1.mass
