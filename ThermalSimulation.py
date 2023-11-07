# logical class which will be implemented with a GUI eventually
# contains all maths that goes on to implement the simulation


from Matrices.HeatFluxMatrix import HeatFluxMatrix
from Matrices.TemperatureMatrix import TemperatureMatrix
from Matrices.ViewFactorMatrix import ViewFactorMatrix


import numpy as np


class ThermalSimulation:
    def __init__(self, constants: dict):
        # [[north, south],[v+,v-],[nadir,zenith]] for each matrix
        self.view_factors = ViewFactorMatrix()
        self.heat_flux = HeatFluxMatrix()
        self.areas = [constants["length"]*constants["height"], constants["width"]
                      * constants["length"], constants["width"]*constants["height"]]
        self.temperatures = TemperatureMatrix(constants["initial_temperature"])
        self.absorption = constants["absorption"]
        self.emissivity_matrix = [[constants["emissivity"], constants["emissivity"]], [
            constants["emissivity"], constants["emissivity"]], [constants["emissivity"], constants["emissivity"]]]
        self.increasingBeta = False
        self.delta_time = constants["delta_time"]
        self.mass = constants["mass"]
        # beta angle will be varied through [-90, +90] (degrees)
        self.variables = constants
        self.variables.update({"time": 0, "critical_beta": np.arcsin(constants["radius_earth"]/(
            constants["radius_earth"] + constants["altitude"])), "albedo": 0, "heat_flux_ir": 0})

    def update_heat_flux_ir(self) -> None:
        if self.variables["beta_angle"] < (np.pi/6):
            self.variables["heat_flux_ir"] = 228
        elif self.variables["beta_angle"] >= np.pi/6:
            self.variables["heat_flux_ir"] = 218

    def updateAlbedo(self) -> None:
        if self.variables["beta_angle"] < (np.pi/6):
            self.variables["albedo"] = 0.14
        elif self.variables["beta_angle"] >= (np.pi/6):
            self.variables["albedo"] = 0.19

    def outputStateOfMatrices(self) -> None:
        print(f"View Factor Matrix: \n {self.view_factors.matrix}")
        print(f"Heat Flux Matrix: \n {self.heat_flux.matrix}")
        print(f"Temperature Matrix: \n {self.temperatures.matrix}")
        print(str(self.variables["time"]) + " s")

    # update all values for next iteration of euler's method
    def update(self) -> dict:
        self.updateAlbedo()
        self.update_heat_flux_ir()
        self.view_factors.update_factors(self.variables)
        self.heat_flux.update_heat_transfer(
            self.variables, self.view_factors.matrix, self.areas, self.temperatures.matrix, self.absorption, self.emissivity_matrix)
        self.temperatures.update_matrix(
            self.mass, self.variables["specific_heat_capacity"], self.heat_flux.matrix, self.delta_time)
        self.variables["time"] += self.delta_time
        # self.outputStateOfMatrices()
        return {"time": self.variables["time"], "beta_angle": self.variables["beta_angle"], "average_temperature": self.temperatures.getAverageTemperature()}

    def simulate(self, iterations: int) -> dict[str, list[float]]:
        dataPoints = {"time": [self.variables["time"]], "beta_angle": [self.variables["beta_angle"]], "average_temperature": [self.variables["initial_temperature"]]}
        print()
        for i in range(iterations):
            print ("\033[A                             \033[A")
            print(f"Iteration {i + 1}")
            newData = self.update()
            dataPoints["time"].append(newData["time"])
            dataPoints["beta_angle"].append(newData["beta_angle"])
            dataPoints["average_temperature"].append(
                newData["average_temperature"])
        print ("\033[A                             \033[A")
        print("Simulation complete : raw data available in output.csv")
        return dataPoints
