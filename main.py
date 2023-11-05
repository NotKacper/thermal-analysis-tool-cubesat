#####################################################################################################
# UoS Artemis^3 - 1, CubeSat Thermal Modelling Python Script Draft, by Kacper Lubczynski 31/10/23
#####################################################################################################

import numpy as np
from Matrices.ViewFactorMatrix import ViewFactorMatrix
from Matrices.HeatFluxMatrix import HeatFluxMatrix
from Matrices.TemperatureMatrix import TemperatureMatrix

# CONSTANTS
HEAT_FLUX_FROM_SUN = 1414  # for hot scenarios it is 1414, for cold scenarios use 1322
# this can be chosen to be anything, chosen as 400 by the .pdf
CONTACT_CONDUCTANCE_COEFFICIENT = 400 # Watts per metre squared per kelvin
RADIUS_EARTH = 6371  # km
ALTITUDE = 500  # km (typically 350 - 700km)
# DELTA_TIME
#  must satisfy condition: sum of change in temperatue from next iteration is less than or equal to 1.
DELTA_TIME = 0.1  # s
ORBITAL_PERIOD = 100000  # s, find out the orbital period (this is moot for most of the simulation anyway)
SPECIFIC_HEAT_CAPACITY = 900 # Joules per kg per degree kelvin
MASS = 12 # kg (default is 12 which is the standard for 6U cubesats)

# Dimensions of cubesat (default is 6U CubeSat dimensions)
WIDTH = 0.2 # metres
LENGTH = 0.3405 # metres
HEIGHT = 0.1 # metres
INITIAL_TEMPERATURE = 273.15 # kelvin

# INTERNAL HEAT FLUX:
# this is the heat flux that the electronic components of the cubesat will be producing
# assumed to be the heat flux experienced by each node (not total heat flux)
# likely an average which is assumed to be constant.
INTERNAL_HEAT_FLUX = 0  # Watts per metre squared, 
                        

# logical class which will be implemented with a GUI eventually
# contains all maths that goes on to implement the simulation


class ThermalSimulation:
    def __init__(self):
        # [[north, south],[v+,v-],[nadir,zenith]] for each matrix
        self.view_factors = ViewFactorMatrix([[0,0],[0,0],[0,0]])
        self.heat_flux = HeatFluxMatrix([[0,0],[0,0],[0,0]])
        self.areas = [LENGTH*HEIGHT, WIDTH*LENGTH, WIDTH*HEIGHT]
        self.temperatures = TemperatureMatrix([[INITIAL_TEMPERATURE,INITIAL_TEMPERATURE],[INITIAL_TEMPERATURE,INITIAL_TEMPERATURE],[INITIAL_TEMPERATURE,INITIAL_TEMPERATURE]])
        self.absorption = 0.95
        self.emissivity_matrix = [[0.85, 0.85], [0.85, 0.85], [0.85, 0.85]]
        # beta angle will be varied through [-90, +90] (degrees), [-pi/2, +pi/2]
        self.variables = {"time": 0, "beta_angle": (np.pi/3), "critical_beta": np.arcsin(RADIUS_EARTH/(RADIUS_EARTH + ALTITUDE)),
                          "altitude": ALTITUDE, "orbital_period": ORBITAL_PERIOD, "radius": RADIUS_EARTH, "albedo": 0,
                          "heat_flux_sun": HEAT_FLUX_FROM_SUN, "contact_conductance_coefficient": CONTACT_CONDUCTANCE_COEFFICIENT,
                          "heat_flux_ir": 0, "stefan_boltzmann": 5.670374419e-8, "internal_heat_flux": INTERNAL_HEAT_FLUX}

    def update_heat_flux_ir(self):
        if self.variables["beta_angle"] < (np.pi/6):
            self.variables["heat_flux_ir"] = 228
        elif self.variables["beta_angle"] >= np.pi/6:
            self.variables["heat_flux_ir"] = 218

    def updateAlbedo(self):
        if self.variables["beta_angle"] < (np.pi/6):
            self.variables["albedo"] = 0.14
        elif self.variables["beta_angle"] >= (np.pi/6):
            self.variables["albedo"] = 0.19

    def outputStateOfMatrices(self):
        print(f"View Factor Matrix: \n {self.view_factors.matrix}")
        print(f"Heat Flux Matrix: \n {self.heat_flux.matrix}")
        print(f"Temperature Matrix: \n {self.temperatures.matrix}")

    # update all values for next iteration of euler's method
    def update(self):
        self.updateAlbedo()
        self.update_heat_flux_ir()
        self.variables["time"] += DELTA_TIME
        self.view_factors.update_factors(self.variables)
        self.heat_flux.update_heat_transfer(
            self.variables, self.view_factors.matrix, self.areas, self.temperatures.matrix, self.absorption, self.emissivity_matrix)
        self.temperatures.update_matrix(MASS, SPECIFIC_HEAT_CAPACITY, self.heat_flux.matrix, DELTA_TIME)
        self.outputStateOfMatrices()
        

sim = ThermalSimulation()
for i in range(10000):
    sim.update()
