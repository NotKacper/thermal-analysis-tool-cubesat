#####################################################################################################
# UoS Artemis^3 - 1, CubeSat Thermal Modelling Python Script Draft, by Kacper Lubczynski 31/10/23
#####################################################################################################

import csv
from ThermalSimulation import ThermalSimulation
import numpy as np

# CONSTANTS
HEAT_FLUX_FROM_SUN = 1414  # for hot scenarios it is 1414, for cold scenarios use 1322
# this can be chosen to be anything, chosen as 400 by the .pdf
CONTACT_CONDUCTANCE_COEFFICIENT = 400  # Watts per metre squared per kelvin
RADIUS_EARTH = 6371  # km
ALTITUDE = 500  # km (typically 350 - 700km)


# DELTA_TIME
# must satisfy condition:
DELTA_TIME = 0.1  # s


# s, find out the orbital period (this is moot for most of the simulation anyway)
ORBITAL_PERIOD = 100000
SPECIFIC_HEAT_CAPACITY = 900  # Joules per kg per degree kelvin
MASS = 12  # kg (default is 12 which is the standard for 6U cubesats)

# Dimensions of cubesat (default is 6U CubeSat dimensions)
WIDTH = 0.2  # metres
LENGTH = 0.3405  # metres
HEIGHT = 0.1  # metres
INITIAL_TEMPERATURE = 273.15  # kelvin

# INTERNAL HEAT FLUX:
# this is the heat flux that the electronic components of the cubesat will be producing
# assumed to be the heat flux experienced by each node (not total heat flux)
# likely an average which is assumed to be constant.
INTERNAL_HEAT_FLUX = 0  # Watts per metre squared, Assume 15W

# BETA_ANGLE
BETA_ANGLE = np.pi/2

# The characteristics of the material used to create the 6U CubeSat (Assumed as Aluminum)
ABSORPTION = 0.95
EMISSIVITIY = 0.85


sim = ThermalSimulation(ABSORPTION, ALTITUDE, BETA_ANGLE, CONTACT_CONDUCTANCE_COEFFICIENT, DELTA_TIME, EMISSIVITIY, HEAT_FLUX_FROM_SUN,
                        HEIGHT, INITIAL_TEMPERATURE, INTERNAL_HEAT_FLUX, LENGTH, MASS, ORBITAL_PERIOD, RADIUS_EARTH, SPECIFIC_HEAT_CAPACITY, WIDTH)
dataPoints = sim.simulate(10000)

# writes all data outputted in .csv file - rawdata
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time", "beta_angle", "average_temperature"])
    for i in range(len(dataPoints["time"])):
        writer.writerow([str(dataPoints["time"][i]), str(
            dataPoints["beta_angle"][i]), str(dataPoints["average_temperature"][i])])
