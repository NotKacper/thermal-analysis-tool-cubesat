# UoS Artemis<sup>3</sup> - 1 Thermal Analysis Tool
Python-based tool using numerical ODE solving, basic matrix operations and pre-designed physical formulae to model the thermal operations of the Artemis<sup>3</sup> - 1 CubeSat probe.
# Ready for use
## How to use
1. Open constants.json and modify the different constants of the simulation to your liking
2. Run main.py
3. Using RStudio set working directory to this repository location.
4. now run thermal_model_plot.r using RStudio to produce a graph visualising the results (gets data from output.csv).
## Additional features to add
Tri-variable plots for beta angle variation
### References
Heavily borrowed from the documentation for the SatTherm, TSS and University of Georgia CubeSat mission Thermal Analysis:
###### University of Georgia CubeSat mission Thermal Analysis: <br>https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Preliminary_Thermal_Analysis_of_Small_Satellites.pdf
###### SatTherm Design Documentation Pages: <br>https://digitalcommons.usu.edu/smallsat/2009/all2009/45/ <br>https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=4615&context=etd_theses
###### TSS Documentation Page: <br> https://dergipark.org.tr/tr/download/article-file/572509<br>

By Kacper Lubczynski as part of UoS Artemis<sup>3</sup> - 1 mission - 2023