import numpy as np


class HeatFluxMatrix:
    def __init__(self, matrix: list[list[float]]):
        self.matrix = matrix

    def find_summation(self, row: int, column: int, areas: list[float], temp_matrix: list[list[float]]):
        sum = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if i != row:
                    sum += areas[i] * \
                        (temp_matrix[i][j]-temp_matrix[row][column])
        return sum

    def _get_heat_flow_general(self, row: int, column: int, variables: dict[str, float], view_factors_matrix: list[list[float]], areas: list[float], temp_matrix: list[list[float]], absorption: float, emissivity_matrix: list[list[float]]) -> float:
        part1 = view_factors_matrix[row][column]*areas[row] * \
            variables["heat_flux_sun"]*absorption
        sigma_notation = self.find_summation(
            row, column, areas, temp_matrix)
        part2 = variables["contact_conductance_coefficient"]*sigma_notation
        part3 = variables["stefan_boltzmann"]*areas[row] * \
            temp_matrix[row][column]**4*emissivity_matrix[row][column]
        return part1+part2-part3

    def _get_heat_flow_nadir(self, variables: dict[str, float], view_factor: float, areas: list[float], temp_matrix: list[list[float]], absorption: float, emissivity_matrix: list[list[float]]) -> float:
        part1 = (view_factor+variables["albedo"]) * \
            areas[2]*variables["heat_flux_sun"]*absorption
        part2 = variables["contact_conductance_coefficient"] * \
            self.find_summation(2, 1, areas, temp_matrix)
        part3 = variables["stefan_boltzmann"]*areas[2] * \
            temp_matrix[2][1]**4*emissivity_matrix[2][1]
        return part1+part2-part3

    def _get_heat_flow_south(self, variables: dict[str, float], areas: list[float], temp_matrix: list[list[float]], emissivity_matrix: list[list[float]]) -> float:
        part1 = variables["contact_conductance_coefficient"] * \
            self.find_summation(0, 1, areas, temp_matrix)
        part2 = variables["stefan_boltzmann"]*areas[0] * \
            temp_matrix[0][1]**4*emissivity_matrix[0][1]
        return part1 - part2

    def update_heat_transfer(self, variables: dict[str, float], view_factors_matrix: list[list[float]], areas: list[float], temp_matrix: list[list[float]], absorption: float, emissivity_matrix: list[list[float]]) -> None:
        self.matrix[0][0] = self._get_heat_flow_general(
            0, 0, variables, view_factors_matrix, areas, temp_matrix, absorption, emissivity_matrix) + variables["internal_heat_flux"]
        self.matrix[0][1] = self._get_heat_flow_south(
            variables, areas, temp_matrix, emissivity_matrix) + variables["internal_heat_flux"]
        self.matrix[1][0] = self._get_heat_flow_general(
            1, 0, variables, view_factors_matrix, areas, temp_matrix, absorption, emissivity_matrix) + variables["internal_heat_flux"]
        self.matrix[1][1] = self._get_heat_flow_general(
            1, 1, variables, view_factors_matrix, areas, temp_matrix, absorption, emissivity_matrix) + variables["internal_heat_flux"]
        self.matrix[2][0] = self._get_heat_flow_general(
            2, 0, variables, view_factors_matrix, areas, temp_matrix, absorption, emissivity_matrix) + variables["internal_heat_flux"]
        self.matrix[2][1] = self._get_heat_flow_nadir(
            variables, view_factors_matrix[2][1], areas, temp_matrix, absorption, emissivity_matrix) + variables["internal_heat_flux"]
