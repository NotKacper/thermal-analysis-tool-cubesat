# logical class which will be implemented with a GUI eventually
# contains all maths that goes on to implement the simulation


from Matrices.HeatFluxMatrix import HeatFluxMatrix
from Matrices.TemperatureMatrix import TemperatureMatrix
from Matrices.ViewFactorMatrix import ViewFactorMatrix


import numpy as np


class ThermalSimulation:
    def __init__(self, ABSORPTION: float, ALTITUDE: float, BETA_ANGLE: float, CONTACT_CONDUCTANCE_COEFFICIENT: float, DELTA_TIME: float, EMISSIVITIY: float, HEAT_FLUX_FROM_SUN: float, HEIGHT: float, INITIAL_TEMPERATURE: float, INTERNAL_HEAT_FLUX: float, LENGTH: float, MASS: float, ORBITAL_PERIOD: float, RADIUS_EARTH: float, SPECIFIC_HEAT_CAPACITY: float, WIDTH: float):
        # [[north, south],[v+,v-],[nadir,zenith]] for each matrix
        self.view_factors = ViewFactorMatrix([[0, 0], [0, 0], [0, 0]])
        self.heat_flux = HeatFluxMatrix([[0, 0], [0, 0], [0, 0]])
        self.areas = [LENGTH*HEIGHT, WIDTH*LENGTH, WIDTH*HEIGHT]
        self.temperatures = TemperatureMatrix([[INITIAL_TEMPERATURE, INITIAL_TEMPERATURE], [
                                              INITIAL_TEMPERATURE, INITIAL_TEMPERATURE], [INITIAL_TEMPERATURE, INITIAL_TEMPERATURE]])
        self.absorption = ABSORPTION
        self.emissivity_matrix = [[EMISSIVITIY, EMISSIVITIY], [
            EMISSIVITIY, EMISSIVITIY], [EMISSIVITIY, EMISSIVITIY]]
        self.increasingBeta = False
        self.delta_time = DELTA_TIME
        self.mass = MASS
        # beta angle will be varied through [-90, +90] (degrees), [-pi/2, +pi/2]
        self.variables = {"time": 0, "beta_angle": BETA_ANGLE, "critical_beta": np.arcsin(RADIUS_EARTH/(RADIUS_EARTH + ALTITUDE)),
                          "altitude": ALTITUDE, "orbital_period": ORBITAL_PERIOD, "radius": RADIUS_EARTH, "albedo": 0,
                          "heat_flux_sun": HEAT_FLUX_FROM_SUN, "contact_conductance_coefficient": CONTACT_CONDUCTANCE_COEFFICIENT,
                          "heat_flux_ir": 0, "stefan_boltzmann": 5.670374419e-8, "internal_heat_flux": INTERNAL_HEAT_FLUX, "specific_heat_capacity": SPECIFIC_HEAT_CAPACITY}

    def vary_beta_angle(self) -> None:
        # increases beta angle by PI / 12 after one complete simulation
        if (self.increasingBeta):
            self.variables["beta_angle"] += np.pi/12
        else:
            self.variables["beta_angle"] -= np.pi/12
        # if the beta angle becomes greater than PI / 2 then the angle should decrease
        if (self.variables["beta_angle"] > np.pi/2):
            self.increasingBeta = False
         # if the beta angle becomes less than -PI / 2 then the angle should increase
        if (self.variables["beta_angle"] < -np.pi/2):
            self.increasingBeta = True

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
        self.variables["time"] += self.delta_time
        self.view_factors.update_factors(self.variables)
        self.heat_flux.update_heat_transfer(
            self.variables, self.view_factors.matrix, self.areas, self.temperatures.matrix, self.absorption, self.emissivity_matrix)
        self.temperatures.update_matrix(
            self.mass, self.variables["specific_heat_capacity"], self.heat_flux.matrix, self.delta_time)
        # self.outputStateOfMatrices()
        return {"time": self.variables["time"], "beta_angle": self.variables["beta_angle"], "average_temperature": self.temperatures.getAverageTemperature()}

    def simulate(self) -> dict[str, list[float]]:
        dataPoints = {"time": [], "beta_angle": [], "average_temperature": []}
        for i in range(10000):
            newData = self.update()
            dataPoints["time"].append(newData["time"])
            dataPoints["beta_angle"].append(newData["beta_angle"])
            dataPoints["average_temperature"].append(
                newData["average_temperature"])
        return dataPoints
