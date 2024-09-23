from enum import Enum

class Color(Enum):
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4
    

class Object:
    def __init__(self, object_id, size, color):
        self.object_id = object_id  # ID of the object
        self.size = size  # Size of the object
        self.color = color  # Color of the object 

