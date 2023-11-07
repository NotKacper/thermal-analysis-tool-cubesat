#####################################################################################################
# UoS Artemis^3 - 1, CubeSat Thermal Modelling Python Script Draft, by Kacper Lubczynski 31/10/23
#####################################################################################################

import csv
from ThermalSimulation import ThermalSimulation
import numpy as np
import json

CONSTANTS = {}

with open('constants.json') as file:
    CONSTANTS = json.load(file)

# initial beta angle parameter
BETA_ANGLE = np.pi/2

CONSTANTS["beta_angle"] = BETA_ANGLE


def getIterationsFromUser():
    try:
        iterations = int(input(
            "for how many iterations would you like to simulate this scenario? (integer input)"))
    except:
        iterations = getIterationsFromUser()
    return iterations


iterations = getIterationsFromUser()
sim = ThermalSimulation(CONSTANTS)
dataPoints = sim.simulate(iterations)

# writes all data outputted in .csv file - rawdata
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time", "beta_angle", "average_temperature"])
    for i in range(len(dataPoints["time"])):
        writer.writerow([str(dataPoints["time"][i]), str(
            dataPoints["beta_angle"][i]), str(dataPoints["average_temperature"][i])])
