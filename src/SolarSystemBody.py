from Vector2D import Vector2D

# Class defining a Body within the Solar System
class SolarSystemBody():
  
    def __init__(self, name, mass, perihelion = 0, speed = 0, color = "white", size = 1):
        self.name = name
        self.mass = int(float(mass))
        self.listOfVelocity = [Vector2D(0, int(float(speed)))]
        self.listOfPosition = [Vector2D(int(float(perihelion)), 0)] 
        self.vel = Vector2D(0, int(float(speed)))   # starts with velocity only in the y axis direction
        self.pos = Vector2D(int(float(perihelion)), 0) # starts on the x-axis at 
        self.color = color
        self.size = float(size)
        
        self.a0 = Vector2D(0,0) # Previous timestep acceleration
        self.a1 = Vector2D(0,0) # Current timestep acceleration
        self.a2 = Vector2D(0,0) # Next timestep acceleration
        self.orbitalPeriod = 0 
    
    # Updates position of body and adds it to array of positions
    def updatePosition(self, newPos):
        self.listOfPosition.append(newPos)
        self.pos = newPos
        
    # Updates velocity of body and adds it to array of positions
    def updateVelocity(self, newVel):
        self.listOfVelocity.append(newVel)
        self.vel = newVel
        
# Class defining a Satellite, which is a child of the SolarSystemBody class
class Satellite(SolarSystemBody):
    def __init__(self, name, mass, origin: SolarSystemBody, destination: SolarSystemBody, launchVelocity: Vector2D):
        self.name = name
        self.mass = int(float(mass))
        self.destination = destination # SolarSystemBody which is the designated destiantion of the satellite
        self.vel = origin.vel + launchVelocity # Initial velocity = velocity of origin body + launch velocity
        self.pos = origin.pos + Vector2D(6e6, 0) # Assumes you start on the surface of the Earth (radius ~6,000 km)
        self.listOfVelocity = [self.vel]
        self.listOfPosition = [self.pos]
        self.color = "white"
        self.size = 0.2
        self.minDistToDest = (self.pos - self.destination.pos).getMagnitude() # Tracks the distance to the destination Body
        self.minDistTIme = 0
        
        self.a0 = Vector2D(0,0) # Previous timestep acceleration
        self.a1 = Vector2D(0,0) # Current timestep acceleration
        self.a2 = Vector2D(0,0) # Next timestep acceleration