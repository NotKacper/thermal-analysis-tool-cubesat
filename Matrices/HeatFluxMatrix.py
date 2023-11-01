import numpy as np


class HeatFluxMatrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def find_summation(self, row, column, area_matrix, temp_matrix):
        sum = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if i != row:
                    sum += area_matrix[i][j] * \
                        (temp_matrix[i][j]-temp_matrix[row][column])
        return sum

    def _get_heat_flow_general(self, row, column, variables, view_factors_matrix, area_matrix, temp_matrix, absorption, emissivity_matrix):
        part1 = view_factors_matrix[row][column]*area_matrix[row][column] * \
            variables["heat_flux_sun"]*absorption
        sigma_notation = self.find_summation(
            row, column, area_matrix, temp_matrix)
        part2 = variables["contact_conductance_coefficient"]*sigma_notation
        part3 = variables["stefan_boltzmann"]*area_matrix[row][column] * \
            temp_matrix[row][column]**4*emissivity_matrix[row][column]
        return part1+part2-part3

    def _get_heat_flow_nadir(self, variables, view_factor, area_matrix, temp_matrix, absorption, emissivity_matrix):
        part1 = (view_factor+variables["albedo"]) * \
            area_matrix[2][1]*variables["heat_flux_sun"]*absorption
        part2 = variables["contact_conductance_coefficient"] * \
            self.find_summation(2, 1, area_matrix, temp_matrix)
        part3 = variables["stefan_boltzmann"]*area_matrix[2][1] * \
            temp_matrix[2][1]**4*emissivity_matrix[2][1]
        return part1+part2-part3

    def _get_heat_flow_south(self, variables, area_matrix, temp_matrix, emissivity_matrix):
        part1 = variables["contact_conductance_coefficient"] * \
            self.find_summation(0, 1, area_matrix, temp_matrix)
        part2 = variables["stefan_boltzmann"]*area_matrix[0][1] * \
            temp_matrix[0][1]**4*emissivity_matrix[0][1]
        return part1 - part2

    def update_heat_transfer(self, variables, view_factors_matrix, area_matrix, temp_matrix, absorption, emissivity_matrix):
        self.matrix[0][0] = self._get_heat_flow_general(
            0, 0, variables, view_factors_matrix, area_matrix, temp_matrix, absorption, emissivity_matrix)
        self.matrix[0][1] = self._get_heat_flow_south(
            variables, area_matrix, temp_matrix, emissivity_matrix)
        self.matrix[1][0] = self._get_heat_flow_general(
            1, 0, variables, view_factors_matrix, area_matrix, temp_matrix, absorption, emissivity_matrix)
        self.matrix[1][1] = self._get_heat_flow_general(
            1, 1, variables, view_factors_matrix, area_matrix, temp_matrix, absorption, emissivity_matrix)
        self.matrix[2][0] = self._get_heat_flow_general(
            2, 0, variables, view_factors_matrix, area_matrix, temp_matrix, absorption, emissivity_matrix)
        self.matrix[2][1] = self._get_heat_flow_nadir(
            variables, view_factors_matrix[2][1], area_matrix, temp_matrix, absorption, emissivity_matrix)
