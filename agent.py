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
    velocity = np.array([0.0, 0.0, 0.0])
    color = (0, 0, 0)
    name = "NO_NAME_IP"

    def __init__(self, name, mass, radius, position, velocity):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        agentsList.append(self)

    def getPosition(self):
        """
        Returns 2d rounded position to use in pygame simulation
        """
        return (round(self.position[0]),
                round(self.position[1]))

    def _computeTotalAcc(self):
        """
        Compute acceleration in the time t+tick for the agent 
        """
        # Initialize a acceleration vector of zeros
        finalAcc = np.array([np.float128(0.0), np.float128(
            0.0), np.float128(0.0)], dtype=np.float128)

        # Update acceleration using gravitational law to compute
        #  attraction force between the current agent and all the other agents
        for agent in agentsList:
            if agent != self:
                acc = _computeAcc(self, agent)
                finalAcc += acc
        return finalAcc

    def updateVelocity(self):
        self.velocity += tick*self._computeTotalAcc()

    @staticmethod
    def newPosition():
        """
        Compute the velocity of each agent and then update the position of
        the agents using the computed velocity
        """

        for agent in agentsList:
            agent.updateVelocity()
        for agent in agentsList:
            agent.position += tick*agent.velocity


def _computeAcc(agent1, agent2):
    """
    Compute force using the gravitational universal law
    """
    tmpPos = np.float128(agent2.position - agent1.position)
    tmpPos = np.square(tmpPos)
    norm = tmpPos[0]+tmpPos[1]+tmpPos[2]

    forceDir = np.float128(agent2.position - agent1.position)
    forceDir = forceDir / np.linalg.norm(forceDir)

    acc = G*forceDir*agent2.mass/norm

    return acc
