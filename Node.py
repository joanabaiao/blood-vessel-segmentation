class Node:

    def __init__(self, category, n_node, list_points):
        self.category = category # bifurcation or endpoint
        self.n_node = n_node # id
        self.list_points = list_points
        self.list_vessels = []

    def findPoint(self, point1):
        n = None

        if (len(self.list_points) == 1):
            point2 = self.list_points[0]
            if (point1[0] == point2[0]) and (point1[1] == point2[1]) and (point1[2] == point2[2]):
                n = self.n_node
        
        elif (len(self.list_points) >= 2):
            for i in range(0, len(self.list_points)-1):
                point2 = self.list_points[i]
                if (point1[0] == point2[0]) and (point1[1] == point2[1]) and (point1[2] == point2[2]):
                    n = self.n_node
            
        return n
    
    def add_vessel(self, vessel):
        self.list_vessels = self.list_vessels.append[vessel]


