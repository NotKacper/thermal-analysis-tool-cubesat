#####################################################################################################
# UoS Artemis^3 - 1, CubeSat Thermal Modelling Python Script Draft, by Kacper Lubczynski 31/10/23
#####################################################################################################

import csv
from ThermalSimulation import ThermalSimulation
import json

CONSTANTS = {}

with open('constants.json') as file:
    CONSTANTS = json.load(file)

initialConstants = {}
initialConstants.update(CONSTANTS)


def getIterationsFromUser():
    try:
        iterations = int(input(
            "for how many iterations would you like to simulate this scenario? (integer input) "))
    except:
        print("Error: Non-integer provided, please try again")
        iterations = getIterationsFromUser()
    return iterations


iterations = getIterationsFromUser()
print("Note: To interrupt the simulation at any time press CRTL + C OR CMD + C, however results will not be created")
dataPoints = [[], [], []]
for i in range(45):
    CONSTANTS["beta_angle"] += i*4
    sim = ThermalSimulation(CONSTANTS)
    temp = sim.simulate(iterations)
    dataPoints[0] += temp["time"]
    dataPoints[1] += temp["beta_angle"]
    dataPoints[2] += temp["average_temperature"]
    CONSTANTS.update(initialConstants)
print("Simulation complete : raw data available in output.csv")

# writes all data outputted in .csv file - rawdata
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time", "beta_angle", "average_temperature"])
    for i in range(len(dataPoints[0])):
        writer.writerow([str(dataPoints[0][i]), str(
            dataPoints[1][i]), str(dataPoints[2][i])])
