import numpy as np


class ViewFactorMatrix:
    def __init__(self):
        self.matrix = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]

    def _find_eclipse_fraction(self, variables: dict[str, float]) -> float:
        if abs(np.radians(variables["beta_angle"])) < np.radians(variables["beta_angle"]):
            return 1/np.pi * np.arccos(np.sqrt(variables["altitude"]**2 + 2 * variables["radius_earth"] * variables["altitude"])/(variables["altitude"] + variables["radius_earth"] * np.cos(np.radians(variables["beta_angle"]))))
        return 0

    # determines the view factor of the north and south sides of the CubeSat
    def _find_view_factor_NS(self, eclipse_fraction: float, variables: dict[str, float]) -> float:
        if ((variables["orbital_period"] / 2) * (1 - eclipse_fraction) > variables["time"]) and ((variables["orbital_period"] / 2) * (1 + eclipse_fraction) < variables["time"]):
            return np.sin(np.radians(variables["beta_angle"]))
        return 0

    def _find_view_factor_v_pos(self, sin_value: float, cos_beta: float, eclipse_fraction: float, variables: dict[str, float]) -> float:
        if (variables["time"] > (variables["orbital_period"] / 2) * (1 + eclipse_fraction)):
            return -sin_value*cos_beta
        return 0

    def _find_view_factor_v_neg(self, sin_value: float, cos_beta: float, eclipse_fraction: float, variables: dict[str, float]) -> float:
        if (variables["time"] > (variables["orbital_period"] / 2) * (1 - eclipse_fraction)):
            return sin_value*cos_beta
        return 0

    def _find_view_factor_nadir(self, cos_value: float, cos_beta: float, eclipse_fraction: float, variables: dict[str, float]) -> float:
        if (variables["orbital_period"] / 4 < variables["time"] and variables["orbital_period"] / 2 * (1 - eclipse_fraction)) or (variables["orbital_period"] / 2 * (1 + eclipse_fraction) < variables["time"] and variables["time"] < 3 * np.pi / 4):
            return -cos_value * cos_beta
        return 0

    def _find_view_factor_zenith(self, cos_value: float, cos_beta: float, variables: dict[str, float]) -> float:
        if (variables["orbital_period"] / 4 > variables["time"]) and (variables["time"] > 3 * variables["orbital_period"] / 4):
            return cos_value*cos_beta
        return 0

    def update_factors(self, variables: dict[str, float]) -> None:
        # finding the reused values
        cos_beta = np.cos(np.radians(variables["beta_angle"]))
        eclipse_fraction = self._find_eclipse_fraction(variables)
        sin_value = np.sin(
            2 * np.pi / variables["orbital_period"] * variables["time"])
        cos_value = np.cos(
            2 * np.pi / variables["orbital_period"] * variables["time"])
        # updating matrix
        self.matrix[0][0] = self.matrix[0][1] = self._find_view_factor_NS(
            eclipse_fraction, variables)
        self.matrix[1][0] = self._find_view_factor_v_pos(
            sin_value, cos_beta, eclipse_fraction, variables)
        self.matrix[1][1] = self._find_view_factor_v_neg(
            sin_value, cos_beta, eclipse_fraction, variables)
        self.matrix[2][0] = self._find_view_factor_nadir(
            cos_value, cos_beta, eclipse_fraction, variables)
        self.matrix[2][1] = self._find_view_factor_zenith(
            cos_value, cos_beta, variables)
