import math

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"{self.x}i + {self.y}j"
    
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("maximum of 2 elements in a Vector2D")
            
    def __add__(self, other): 
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if isinstance(other, Vector2D):  # Vector dot product
            return (self.x * other.x + self.y * other.y)
        elif isinstance(other, (int, float)):  # Scalar multiplication
            return Vector2D(self.x * other, self.y * other)
        else:
            raise TypeError("operand must be Vector2D, int, or float")
            
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector2D(self.x / other, self.y / other)
        else:
            raise TypeError("operand must be int or float")
            
    def getMagnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        magnitude = self.getMagnitude()
        return Vector2D(self.x / magnitude, self.y / magnitude)