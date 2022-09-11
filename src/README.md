
# Solar System Simulation

This project aims to simulate the motion of the planets in two-dimensions and to predict launch conditions for satellites to successfully reach planets.

To run the simulation, open and run the Simulation.py script

To edit the SolarSystemBody's used in the program, edit the inputData.txt file.
  - The data for each new body needs to be written on a new line
  - values are comma-seperated with no spaces
  - Parameters are in this order (Parameter type):\
    Name(String),mass(int),perihelion(int),maximumOrbitalSpeed(int),displayedColour(HTMLColorNames), displayedSize(float)
  - SI units are used for all quantities: mass(kg), speed(m/s), distance(m)

To change the Satellites used in the program edit, the satellites.txt file.
  - The data for each new Satellite needs to be written on a new line
  - values are comma-seperated with no spaces
  - Parameters are in this order (Parameter type):\
    Name(String),mass(int),indexOfOriginBody(int),indexOfDestinationObject(int),horizontalLaunchVelocity(int),verticalLaunchVelocity(int)
  - SI units are used for all quantities: mass(kg), speed(m/s), distance(m)
  - For clarification on the index of bodies, if you want to launch a satellite from Earth, and Earth is the 3rd planet in the inputData.txt file (you don't count the sun), you'd use index 3 for Earth 

