import sys
import csv
import json
import math
import pygame
import numpy as np
from pygame.locals import *
import pandas as pd

from data import *
from agent import agentsList, Agent

global screenSize
screenSize = [1920, 1080]


def load_parameters(path):
    package = []
    file = open(path, 'r')
    j = json.load(file)

    for subgroup in j.values():
        package.append([cast(x) for x in subgroup.values()])

    env_variables = package.pop(4)
    file.close()
    return (package, env_variables)


def cast(x):
    try:
        return float(x)
    except Exception:
        return str(x)


class Environment:

    def __init__(self, vars):
        # Environmental Constants
        self.elev, self.t, self.g, self.M_air, self.R, self.gamma, self.P_zero = vars  # noqa
        self.g_zero = self.g
        self.Re = 6356766
        # Layer base altitudes
        self.hb = [0, 11000, 20000, 32000, 47000, 51000, 71000]
        # Layer base pressures
        self.Pb = [101325, 22632.1, 5474.89,
                   868.019, 110.906, 66.9389, 3.95642]
        # Layer base temperatures
        self.Tb = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65]
        # Layer lapse rates
        self.Lm = [-0.0065, 0.0, 0.001, 0.0028, 0.0, -0.0028, -0.002]

    def get_geopotential_altitude(self, z: float) -> float:
        return self.Re*z / (self.Re+z)

    def atmo_heterosphere_equ(self, z: float, a, b, c, d, e):
        z_km = z/1000
        return math.exp(a * z_km**4 + b * z_km**3 + c * z_km**2 + d * z_km + e)  # noqa

    def get_gravity(self, z: float) -> float:
        return self.g_zero * (self.Re / (self.Re + z))**2

    def get_temp(self, z: float, h: float) -> float:
        if h <= 84852:
            for i in range(len(self.hb)-1):
                if self.hb[i] <= h <= self.hb[i+1]:
                    return (self.Tb[i] + self.Lm[i]*(h-self.hb[i]), i)
            return (self.Tb[i+1] + self.Lm[i+1]*(h-self.hb[i+1]), i+1)
        elif 86000 < z <= 91000:
            return (186.87, 7)
        elif 91000 < z <= 110000:
            if 91000 < z <= 100000:
                layer = 8
            elif 100000 < z <= 110000:
                layer = 9
            return (
                263.1905 - 76.3232 * math.sqrt(1 - ((z - 91000) / -19942.9)**2),  # noqa
                layer
                )
        elif 110000 < z <= 120000:
            return (240 + 0.012 * (z - 110000), 10)
        elif 120000 < z <= 1000000:
            if 120000 < z <= 150000:
                layer = 11
            elif 150000 < z <= 200000:
                layer = 12
            elif 200000 < z <= 300000:
                layer = 13
            elif 300000 < z <= 500000:
                layer = 14
            elif 500000 < z <= 750000:
                layer = 15
            elif 750000 < z <= 1000000:
                layer = 16
            xi = (z - 120000) * (6356766 + 120000) / (6356766 + z)
            return (1000 - 640 * math.exp(-0.00001875 * xi), layer)

    def get_pressure(self, z: float, h: float, T: float, b: int) -> float:

        if b <= 6:
            if self.Lm[b] != 0:
                return self.Pb[b] * (self.Tb[b]/T)**(self.g_zero*self.M_air/(self.R*self.Lm[b]))  # noqa
            else:
                return self.Pb[b] * math.exp(-self.g_zero * self.M_air * (h-self.hb[b]) / (self.R*self.Tb[b]))  # noqa
        elif b == 7:
            return self.atmo_heterosphere_equ(
                z, 0.000000, 2.159582e-6, -4.836957e-4, -0.1425192, 13.47530)
        elif b == 8:
            return self.atmo_heterosphere_equ(
                z, 0.000000, 3.304895e-5, -0.009062730, 0.6516698, -11.03037)
        elif b == 9:
            return self.atmo_heterosphere_equ(
                z, 0.000000, 6.693926e-5, -0.01945388, 1.719080, -47.75030)
        elif b == 10:
            return self.atmo_heterosphere_equ(
                z, 0.000000, -6.539316e-5, 0.02485568, -3.223620, 135.9355)
        elif b == 11:
            return self.atmo_heterosphere_equ(
                z, 2.283506e-7, -1.343221e-4, 0.02999016, -3.055446, 113.5764)
        elif b == 12:
            return self.atmo_heterosphere_equ(
                z, 1.209434e-8, -9.692458e-6, 0.003002041, -0.4523015, 19.19151)
        elif b == 13:
            return self.atmo_heterosphere_equ(
                z, 8.113942e-10, -9.822568e-7, 4.687616e-4, -0.1231710, 3.067409)
        elif b == 14:
            return self.atmo_heterosphere_equ(
                z, 9.814674e-11, -1.654439e-7, 1.148115e-4, -0.05431334, -2.011365)
        elif b == 15:
            return self.atmo_heterosphere_equ(
                z, -7.835161e-11, 1.964589e-7, -1.657213e-4, 0.04305869, -14.77132)
        elif b == 16:
            return self.atmo_heterosphere_equ(
                z, 2.813255e-11, -1.120689e-7, 1.695568e-4, -0.1188941, 14.56718)

    def get_density(self, z: float, P: float, T: float, b) -> float:
        if b <= 6:
            return (P * self.M_air)/(self.R * T)
        elif b == 7:
            return self.atmo_heterosphere_equ(
                z, 0.000000, -3.322622E-06, 9.111460E-04, -0.2609971, 5.944694)
        elif b == 8:
            return self.atmo_heterosphere_equ(
                z, 0.000000, 2.873405e-05, -0.008492037, 0.6541179, -23.62010)
        elif b == 9:
            return self.atmo_heterosphere_equ(
                z, -1.240774e-05, 0.005162063, -0.8048342, 55.55996, -1443.338)
        elif b == 10:
            return self.atmo_heterosphere_equ(
                z, 0.00000, -8.854164e-05, 0.03373254, -4.390837, 176.5294)
        elif b == 11:
            return self.atmo_heterosphere_equ(
                z, 3.661771e-07, -2.154344e-04, 0.04809214, -4.884744, 172.3597)
        elif b == 12:
            return self.atmo_heterosphere_equ(
                z, 1.906032e-08, -1.527799E-05, 0.004724294, -0.6992340, 20.50921)
        elif b == 13:
            return self.atmo_heterosphere_equ(
                z, 1.199282e-09, -1.451051e-06, 6.910474e-04, -0.1736220, -5.321644)
        elif b == 14:
            return self.atmo_heterosphere_equ(
                z, 1.140564e-10, -2.130756e-07, 1.570762e-04, -0.07029296, -12.89844)
        elif b == 15:
            return self.atmo_heterosphere_equ(
                z, 8.105631e-12, -2.358417e-09, -2.635110e-06, -0.01562608, -20.02246)
        elif b == 16:
            return self.atmo_heterosphere_equ(
                z, -3.701195e-12, -8.608611e-09, 5.118829e-05, -0.06600998, -6.137674)

    def get_c(self, T: float) -> float:
        return math.sqrt((self.gamma * self.R * T) / self.M_air)

    def get_status(self, z: float):
        h = round(self.get_geopotential_altitude(z), 0)
        self.g = self.get_gravity(z)
        self.T, b = self.get_temp(z, h)
        self.P = self.get_pressure(z, h, self.T, b)
        self.Rho = self.get_density(z, self.P, self.T, b)
        self.c = self.get_c(self.T)


class System:
    def __init__(self, params, env, burn_time: float):
        package = params
        print(package)

        # Environment
        self.env = env

        # Burn time
        self.num_steps = int(burn_time // self.env.t)
        self.burn_time = self.num_steps * self.env.t

        # Engine specs
        self.etype = package[0][0]
        package[0].pop(0)
        if self.etype == "Liquid":
            self.isp, self.thrust = package[0]
        elif self.etype == "Solid":
            self.isp, self.avg_thrust, path = package[0]  # noqa
            with(open(path)) as f:
                csv_reader = csv.reader(f)
                self.thrust_curve = {}
                for row in csv_reader:
                    self.thrust_curve.update({
                        float(row[0]): float(row[1])
                    })
                f.close()

        # Fuel Specs
        if self.etype == "Liquid":
            self.OFratio, self.Reserve = package[1]
        elif self.etype == "Solid":
            self.OFratio = 0
            self.Reserve = package[1][0]
        # Flow Rate
        if self.etype == "Liquid":
            self.w = (self.thrust/self.env.g_zero)/self.isp
        elif self.etype == "Solid":
            self.w = (self.avg_thrust/self.env.g_zero)/self.isp
        self.dF = self.w * (1 / (self.OFratio + 1))
        self.dOx = (self.w - self.dF)

        # Fuel & Oxidizer
        self.F = (self.dF * self.burn_time)/(1 - self.Reserve/100)
        self.Ox = (self.dOx * self.burn_time)/(1 - self.Reserve/100)

        # Mass
        self.dry_mass = package[2][0]

        # Aerodynamics
        self.Cd, self.cross_section = package[3]

        # Output
        self.csvout = package[4][0]

        self.field_names = ["t", "thrust", "drag", "m", "v", "mach", "a", "altitude",
                            "asl", "twr", "max_v", "max_mach", "max_acc", "min_acc", "max_g", "min_g"]
        with open(self.csvout, "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(self.field_names)
            f.close()

# Flight
    def launch(self):
        """Runs a simulation within the given parameters."""
        # Variables setup
        self.t = 0
        self.altitude = 0
        self.asl = self.altitude + self.env.elev
        self.calc_mass()
        self.env.get_status(self.asl)
        self.calc_thrust()
        self.calc_twr()
        self.drag = 0
        self.v = 0
        self.max_v = 0
        self.mach = 0
        self.max_mach = 0
        self.max_acc = 0
        self.max_g = 0
        self.min_acc = 0
        self.min_g = 0
        self.a = 0
        self.j = 0
        self.s = 0

        # Used by matplotlib
        self.data = [[], [], [], [], [], [], [], [], [], [], []]

        # Accelaration phase
        for i in range(self.num_steps):
            # Output management
            self.add_data()
            # Environment-related
            self.update_env()
            # Thrust-related
            self.calc_thrust()
            # Accelaration/derivative-related
            self.calc_acc()
            self.calc_additional_derivatives()
            # Position-related
            self.set_altitude()
            # Velocity-related
            self.calc_velocity()
            # Force-related
            self.calc_drag()
            self.calc_twr()
            # Mass-related
            self.calc_propellant()
            self.calc_mass()
            # Time-related
            self.t += self.env.t

            if self.a > self.max_acc:
                self.max_acc = self.a
                self.max_g = self.max_acc/self.env.g

            if self.v > self.max_v:
                self.max_v = self.v
                self.max_mach = self.mach

        self.thrust = 0

        # Deceleration phase
        while self.v > 0:
            # Output management
            self.add_data()
            # Environment-related
            self.update_env()
            # Accelaration/derivative-related
            self.calc_acc()
            self.calc_additional_derivatives()
            # Position-related
            self.set_altitude()
            # Velocity-related
            self.calc_velocity()
            # Force-related
            self.calc_drag()
            self.calc_twr()
            # Mass-related
            self.calc_mass()
            # Time-related
            self.t += self.env.t

            if self.a < self.min_acc:
                self.min_acc = self.a
                self.min_g = self.min_acc/self.env.g

        self.output("max_v", "max_mach", "max_acc",
                    "min_acc", "max_g", "min_g")

    def suicide_burn(self):
        """Run a suicide burn simulation, will affct ascent simulation."""
        self.Vt = math.sqrt((2 * self.m * self.env.g) / (self.env.Rho * self.cross_section * self.Cd))  # noqa

# Mass
    def calc_mass(self):
        self.propellant_mass = (self.Ox + self.F)
        self.m = self.propellant_mass + self.dry_mass

    def calc_propellant(self):
        if self.etype == "Liquid":
            self.w = (self.thrust/self.env.g_zero)/self.isp
        elif self.etype == "Solid":
            self.w = (self.avg_thrust/self.env.g_zero)/self.isp
        self.dF = self.w * (1/(self.OFratio+1))
        self.dOx = (self.w - self.dF)
        self.Ox -= self.dOx * self.env.t
        self.F -= self.dF * self.env.t

# Position
    def set_altitude(self):
        self.altitude += self.v * self.env.t + (self.a * self.env.t**2)/2  # noqa
        self.asl = self.altitude + self.env.elev

# Derivatives of position
    def calc_velocity(self):
        self.v += self.a * self.env.t
        self.mach = self.v/self.env.c

    def calc_acc(self):
        self.a = (self.thrust - (self.m * self.env.g + self.drag)) / self.m

    def calc_additional_derivatives(self):
        self.j = (self.a - self.data[4][-1]) / self.env.t
        self.s = (self.j - self.data[5][-1]) / self.env.t

# Forces
    def calc_thrust(self):
        if self.etype == "Liquid":
            pass
        elif self.etype == "Solid":
            self.thrust = self.thrust_curve[round(self.t, 3)]

    def calc_drag(self):
        self.drag = 0.5 * (self.env.Rho * self.v**2 * self.Cd * self.cross_section)  # noqa

    def calc_twr(self):
        self.twr = self.thrust / (self.m * self.env.g)

# Environment
    def update_env(self):
        self.env.get_status(self.asl)

# Ouput
    def output(self, *args):
        values = []
        for field in self.field_names:
            value = str(round(eval(field, self.__dict__), 5))
            values.append(value)

        with open(self.csvout, "a", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(values)
            f.close()

    def add_data(self):
        self.data[0].append(self.t)
        self.data[1].append(self.altitude)
        self.data[2].append(self.v)
        self.data[3].append(self.env.c)
        self.data[4].append(self.a)
        self.data[5].append(self.j)
        self.data[6].append(self.s)
        self.data[7].append(self.drag)
        self.output("t", "thrust", "drag", "m", "v",
                    "mach", "a", "altitude", "asl", "twr")


def run_simulation(burn_time):
    params = load_parameters("RocketSimulationData/info.json")
    env = Environment(params[1])
    s = System(params[0], env, burn_time)
    s.launch()


def renderAgents(screen, res, ratio):
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (0, 0, 255), (0, 1080-108, 1920, 108))

    pos = screenSize[1]-158 - res["altitude"]*ratio
    # print("altitude: "+str(res["altitude"])+", pos: "+str(pos))

    pygame.draw.rect(screen, (255, 255, 255), (940, pos, 20, 50))

    pygame.display.update()


def simulateRocket(screen):

    run_simulation(150)

    df = pd.read_csv('RocketSimulationData/Flight.csv')
    result = df.to_dict("index")

    ratio = screenSize[1]/1000000

    interestingPoint = None

    for res in result:
        # print("time: "+str(result[res]["t"])+" Altitude: "+str(result[res]["altitude"]))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        renderAgents(screen, result[res], ratio)
        if result[res]["altitude"] < 800000:
            interestingPoint = result[res]
        pygame.display.update()
    return interestingPoint
