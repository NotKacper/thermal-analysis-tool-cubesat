thermalData <- read.csv("output.csv")

plot(thermalData$time, thermalData$average_temperature, xlab="Time (s)", ylab="Average Tempreature (K)")

