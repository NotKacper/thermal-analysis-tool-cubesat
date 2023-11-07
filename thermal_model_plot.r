library(plotly)
# require(plot3D)

thermalData <- read.csv("output.csv")

BetaAngle <- unique(thermalData$beta_angle)

Time <- unique(thermalData$time)

Temperature <- matrix(
  thermalData$average_temperature,
  
  nrow = length(Time),
  ncol = length(BetaAngle),
  byrow = TRUE
)

# persp3D(x=Time, y=BetaAngle, z=Temperature, theta=120)



# Need to get Temperature readings into form A[i][j] = Temperature[time][beta_angle]

figure <- plot_ly() %>% add_surface(x=~Time, y=~BetaAngle, z=~Temperature)

figure