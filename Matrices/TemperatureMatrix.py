class TemperatureMatrix:
    def __init__(self, matrix : list[list]):
        self.matrix = matrix

    def update_matrix(self, mass : float, specific_heat_capacity : float, heat_flow_matrix : list[list[float]], delta_time : float) -> None:
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] += delta_time*heat_flow_matrix[i][j]/(mass*specific_heat_capacity)

    def getAverageTemperature(self) -> float: 
        sum = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                sum+=self.matrix[i][j]
        return sum / (len(self.matrix)*len(self.matrix[0]))
