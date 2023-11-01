class TemperatureMatrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def update_matrix(self, mass, specific_heat_capacity, heat_flow_matrix, delta_time):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] += delta_time*heat_flow_matrix[i][j]/(mass*specific_heat_capacity)
