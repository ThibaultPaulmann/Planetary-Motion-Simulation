import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from SolarSystemBody import SolarSystemBody, Satellite
from Vector2D import Vector2D

# Solar System
class SolarSystem(object):
    
    GRAVITATIONAL_CONSTANT = 6.67408e-11 # Gravitational Constant (m3 kg-1 s-2)
    SECONDS_IN_DAY = 86400 # Number of seconds in a day
    
    TIME_STEP = 3600   # Time-step (seconds)
    NUM_ITERATIONS = 10000 # Total number of iterations running the simulation
    
    def __init__(self):
        self.bodies = []
        self.time = 0
    
    # Adds a SolarSystemBody object to the array of bodies
    def addBody(self, body):
        self.bodies.append(body)
    
    # Removes a SolarSystemBody object from the array of bodies
    def removeBody(self, body):
        self.bodies.remove(body)
     
    # Method that calculates the acceleration exerted by the other SolarSystemBodys in the system on given SolarSystemBody  
    def calculateAcceleration(self, body: SolarSystemBody):
        # Temporary variable that tracks the sum of gravitational forces
        gForcesFromBodies = Vector2D(0,0)
        
        # Loops through all SolarSystemBody's that are not the given SolarSystemBody and are not Satellites
        for otherBody in (otherBody for otherBody in self.bodies if otherBody != body and not isinstance(otherBody, Satellite)):
            m1 = body.mass
            m2 = otherBody.mass
            # Displacement vector between the two bodies
            r = otherBody.pos - body.pos
            distance = r.getMagnitude()
            # Newton's law of universal gravitation
            gForce = r.normalize() * (((m1 * m2) / pow(distance, 2)) * self.GRAVITATIONAL_CONSTANT)
            # Add force to sum
            gForcesFromBodies += gForce
        
        # Newton's second law
        acceleration = gForcesFromBodies / body.mass
        
        # Deals with the case where there is only one body and acceleration gets cast to an int instead of a Vector2D
        if acceleration == 0:
            return Vector2D(0,0)
        else:
            return acceleration
        
    # Method that calculates the Total Energy of the System (J) and prints result to output file  
    def calculateSystemEnergy(self):
        # List of Kinetic Energy for each SolarSystemBody
        kEnergyBodies = []
        pEnergyBodies = []
        
        for body in self.bodies:
            pEnergy = 0
            
            # Calculate kinetic energy of the body
            kEnergy = 0.5 * body.mass * (body.vel.getMagnitude() ** 2)
            kEnergyBodies.append(kEnergy)
            
            # Calculate sum of gravitational potential energy with other bodies 
            for otherBody in (otherBody for otherBody in self.bodies if otherBody != body):
                m1 = body.mass
                m2 = otherBody.mass
                distance = (otherBody.pos - body.pos).getMagnitude()
                pEnergy += -0.5 * (self.GRAVITATIONAL_CONSTANT * m1 * m2 / distance)
            
            pEnergyBodies.append(pEnergy)
        
        totalEnergy = sum(kEnergyBodies) + sum(pEnergyBodies)
        
        # Stores the Total Energy(J) and Time(days) in arrays used to display the Energy-Time graph
        self.energyTimeX.append(self.time / self.SECONDS_IN_DAY)
        self.energyTimeY.append(totalEnergy)
        # Prints the result to the output file
        self.outputFile.write("Time = " + str(self.time) + "s; Total Energy = " + str(totalEnergy) + "J\n")
    
    # Resets variables, reads the input data and initiates variables so that runSimulation can run
    def setupSimulation(self):
        # Reset the time and arrays that store data
        self.time = 0
        self.bodies = []
        self.energyTimeX = []
        self.energyTimeY = []
        
        # Setup the output file
        outputData = open("out.txt", "w")
        outputData.write("Output File Containing Total Output Of The System \n")
        outputData.close()
        
        # Read and parse the input file
        simulationData = open("inputData.txt", "r").read().split("\n")
        
        # Create instances of SolarSystemBody using the input data
        for bodyData in simulationData:
            bodyParams = bodyData.split(',')
            # Create instances of SolarSystemBody using the input data
            body = SolarSystemBody(bodyParams[0], # Body name
                                   bodyParams[1], # Body mass
                                   bodyParams[2], # Orbit perihelion
                                   bodyParams[3], # Maximum orbit speed
                                   bodyParams[4], # Display color
                                   bodyParams[5]) # Display size
            self.addBody(body)
        
        # Read and parse the satellite file
        satelliteData = open("satellites.txt", "r").read().split("\n")
        
        for data in satelliteData:
            satelliteParams = data.split(",")
            # Create instances of Satellite using the input data
            satellite = Satellite(satelliteParams[0], # Satellite name
                                  satelliteParams[1], # Satellite mass
                                  self.bodies[int(float(satelliteParams[2]))], # Satellite origin
                                  self.bodies[int(float(satelliteParams[3]))], # Satellite destination
                                  Vector2D(int(float(satelliteParams[4])), int(float(satelliteParams[5])))) # Launch velocity
            self.addBody(satellite)
        
        for body in self.bodies:
            # Calculate initial acceleration
            body.a0  = self.calculateAcceleration(body)
            
            # Calculate current timestep velocity with the initial acceleration
            newVel = body.vel + (body.a2 * self.TIME_STEP)
            body.updateVelocity(newVel)
            
            # Calculate current timestep position with current velocity
            newPos = body.pos + (newVel * self.TIME_STEP)
            body.updatePosition(newPos)
            
            # Calculate current timestep acceleration with current position
            body.a1 = self.calculateAcceleration(body)
      
        # Update time
        self.time += self.TIME_STEP
    
    # Main method of the class that takes care of setting up the simulation, running it and dislaying the results
    def runSimulation(self):
        self.setupSimulation()
        
        # Open the output file ready to append data to it
        self.outputFile = open("out.txt", "a")
        
        # Loop for the number of iterations stated in the constant at the start of the file
        for i in range(self.NUM_ITERATIONS):
            # run Beeman's method on all bodies in the system
            for body in self.bodies:
                # Predict position at next timestep using current and previous acceleration
                newPos = body.pos + (body.vel * self.TIME_STEP) + (((( body.a1 * 4) - body.a0) * pow(self.TIME_STEP, 2)) / 6)
                body.updatePosition(newPos)
                
                # Calculate new acceleration using predicted position
                body.a2 = self.calculateAcceleration(body)
                
                # Predict new velocity
                newVel = body.vel + ((body.a2 * 2) + (body.a1 * 5) - body.a0) * self.TIME_STEP / 6
                body.updateVelocity(newVel)
                
                # Prepare variables for next iteration
                body.a0 = body.a1
                body.a1 = body.a2
                
                # Checks if SolarSystemBody which is not a Satellite has completed half of its orbit
                if not isinstance(body, Satellite):
                    # When body first passes the halfway orbit point, it saves the current time * 2
                    if body.pos[1] < 0 and body.orbitalPeriod == 0:
                        body.orbitalPeriod = self.time * 2
                # Checks if Satellite is closer to it's destination. If it is, saves the distance and the current time
                else:
                    distance = (body.destination.pos - body.pos).getMagnitude() / 1000
                    if distance < body.minDistToDest:    
                        body.minDistToDest = distance
                        body.minDistTime = self.time
            
            # Calculates Total Energy of System and outputs to file
            self.calculateSystemEnergy()
            
            # Update time
            self.time += self.TIME_STEP
        
        # Prints how close each satellite got to its destination (km) and the point in time it reached it (Earth days)
        for body in self.bodies:
            if isinstance(body, Satellite):
                print(body.name + " reached a minumum distance of "+ str(round(body.minDistToDest)) + " km to " + body.destination.name)
                print("It reached this point in " + str(round(body.minDistTime / self.SECONDS_IN_DAY, 2)) + " earth days")
        # Close the output file, not needed anymore    
        self.outputFile.close()
        
        # Prints the simulated orbital period for the bodies that aren't the sun or satellites
        for body in self.bodies[1:]:
            if not isinstance(body, Satellite):
                print(body.name + " orbital period: " + str(round((body.orbitalPeriod / self.SECONDS_IN_DAY), 2)) + " earth days")
        
        # Displays the Total Energy of system over time graphic
        self.displayEnergyTime()
        
        # Displays the graphical representation of the motion of the SolarSystemBodies over time
        self.displaySimulation()
    
    # Creates and displays a graph of the Total Energy of system (J) over time (Earth days)
    def displayEnergyTime(self):
        plt.plot(self.energyTimeX, self.energyTimeY)
        plt.xlabel("Time (Earth days)")
        plt.ylabel("Total Energy of System (J)")
        plt.title("Total Energy of System over time", pad = 20)
        plt.show()
    
    # Creates an animation that displays the movement of the SolarSystemBodies according to the simulation
    def displaySimulation(self):
        fig = plt.figure()
        ax = plt.axes()
        self.patches = []
        
        # Create a circle for each body at their starting position
        for body in self.bodies:
            self.patches.append(plt.Circle((body.listOfPosition[0][0], 0), 0.05e11 * body.size, color = body.color, animated = True))
        
        for i in range(0, len(self.patches)):
            ax.add_patch(self.patches[i])
        
        # Find the maximum absolute value in the x or y direction. Set the window size to 105% of this value
        # If none found create a 100x100 grid. The grid will always be a square.
        try:
            maxX = max( max(abs(pt[0]) for pt in body.listOfPosition) for body in self.bodies)
        except ValueError:
            maxX = 100
        try:
            maxY = max( max(abs(pt[1]) for pt in body.listOfPosition) for body in self.bodies)
        except ValueError:
            maxY = 100
        windowSize = max(maxX, maxY) * 1.05
        
        # Decorate the graph and label the title and axis
        fig.set_facecolor("grey")
        fig.suptitle("Solar System Representation", fontsize = 20)
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.axis("square")
        ax.set_facecolor("black")
        
        # Set the axis limits. The axis format is set to square. 
        ax.set_xlim(-windowSize, windowSize)
        ax.set_ylim(-windowSize, windowSize)
        
        # Setup the animation
        self.anim = FuncAnimation(fig, 
                            self.animate, 
                            init_func = self.init, 
                            frames = self.NUM_ITERATIONS, 
                            repeat = False, 
                            interval = 0, 
                            blit = True)
        
        plt.show()
        
    # Init for the animation. Required for blit = True
    def init(self):
        return self.patches
    
    # Animation iterates through the bodies and the array of positions created by the simulation        
    def animate(self, iteration):
        patch = 0
        for body in self.bodies:
            self.patches[patch].center = (body.listOfPosition[iteration][0], body.listOfPosition[iteration][1])
            patch += 1
        return self.patches
    
   