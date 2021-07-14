import math

class Vessel:

    def __init__(self, n_vessel, list_points, node_initial, node_final):

        self.n_vessel = n_vessel
        self.list_points = list_points
        self.node_initial = node_initial
        self.node_final = node_final
        self.length = len(list_points)

        self.radius = 0
        self.volume = 0
        self.resistance = 0
        self.viscosity = 0

        self.pressure = None


    def findPoint(self, point1):
        n = False

        if (len(self.list_points) == 1):
            point2 = self.list_points[0]
            if (point1[0] == point2[0]) and (point1[1] == point2[1]) and (point1[2] == point2[2]):
                n = True
        
        elif (len(self.list_points) >= 2):
            for i in range(0, len(self.list_points)):
                point2 = self.list_points[i]
                if (point1[0] == point2[0]) and (point1[1] == point2[1]) and (point1[2] == point2[2]):
                    n = True
            
        return n
    
    def update_volume(self):
        self.volume = self.volume + 1

    def set_others(self):
        self.radius = math.sqrt(self.volume/(math.pi * self.length))
        self.viscosity = 2
        self.resistance = (8 * self.viscosity * self.length)/(math.pi * math.pow(self.radius, 4))
    












