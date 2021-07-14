import numpy as np
import load_write as lw
import random
import math
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Node import Node
from Vessel import Vessel

################################# FIND BIFURCATIONS ################################# 

filename_skeleton = "teste_thinning2.vti"
filename_volume = "teste_volume2.vti"
filename_bifurcations = "bifurcations.vti"
filename_output = "final.vti"

skeleton = lw.load_file_vti(filename_skeleton)
volume = lw.load_file_vti(filename_volume)

dimensions = np.shape(skeleton)
x = dimensions[0]
y = dimensions[1]
z = dimensions[2]

skeleton[:,90:,:] = 0

new_array = np.zeros((x,y,z))
points_bifurcations = {}
points_endpoints = {}
points_total = {}
points_volume = []
points_skeleton = []

print("\nFinding bifurcations, centerlines and endpoints...")
total1 = 0
total2 = 0
total3 = 0
for k in range(1, z-1):
        for j in range(1, y-1): 
            for i in range(1, x-1):               
                if skeleton[i, j, k] == 1:

                    points_total[total2] = (i, j, k)
                    total2 = total2+1

                    M_auxiliar = skeleton[i-1:i+2, j-1:j+2, k-1:k+2]
     
                    if (np.sum(M_auxiliar) > 3): # bifurcation
                        new_array[i, j, k] = 2 
                        points_bifurcations[total1] = (i, j, k)
                        total1 = total1 + 1
                    
                    elif (np.sum(M_auxiliar) < 3): # endpoint
                        new_array[i, j, k] = 3
                        points_endpoints[total3] = (i, j, k)
                        total3 = total3 + 1

                    else:
                        points_skeleton.append((i, j, k))
                        new_array[i,j,k] = 1 # centerline
                
                if volume[i, j, k] == 1:
                    points_volume.append((i, j, k))


print("Complete!")

##################################### CLUSTERING #################################### 

def getkey(dictionary, value):
    
    key = " "   
    list_items = dictionary.items()
    
    for item in list_items:
        for i in range(len(item[1])):
            if item[1][i] == value:
                key = item[0]

    return key

def getvalues(dictionary, key):

    values = []
    list_items = dictionary.items()
    
    for item in list_items:
        if key == item[0]:
            values = item[1]

    return values

def findvalue(dictionary, value):
    
    valid = False  
    list_items = dictionary.items()
    
    for item in list_items:
        for i in range(len(item[1])):
            if item[1][i] == value:
                valid = True

    return valid


print("\nClustering...")
clusters = {}
c = 1
cutoff = 1.5
for key1,val1 in points_bifurcations.items():
    for key2,val2 in points_bifurcations.items():

        x1 = val1[0]
        x2 = val2[0]
        y1 = val1[1]
        y2 = val2[1]
        z1 = val1[2]
        z2 = val2[2]

        d = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

        if (d != 0):

            if (d < cutoff):

                if (findvalue(clusters,key1) == True) and (findvalue(clusters,key2) == True):
                    if (getkey(clusters, key1) != getkey(clusters, key2)): # diferent clusters

                        key_1 = getkey(clusters, key1)
                        key_2 = getkey(clusters, key2)
                        values = getvalues(clusters, key_2)

                        for i in range(len(values)):
                            clusters[key_1].append(values[i]) # join
                        
                        del clusters[key_2] # delete

                        key_3 = list(clusters.keys())[-1]
                        clusters[key_2] = clusters.pop(key_3) # change the key from the last one to the one that was changed

                        clusters = dict(sorted(clusters.items()))
                
                elif (findvalue(clusters,key1) == True) and (findvalue(clusters,key2) == False): 
                    clusters[getkey(clusters, key1)].append(key2) # add point 2 to the cluster with point 1
                
                elif (findvalue(clusters,key1) == False) and (findvalue(clusters,key2) == True):
                    clusters[getkey(clusters, key2)].append(key1) # add point 1 to the cluster with point 2
                
                else: # create new cluster and add the two points
                    clusters[c] = [key1]
                    clusters[c].append(key2)
                    c = c + 1
                
            else:
                if (findvalue(clusters,key1) == True) and (findvalue(clusters,key2) == False): # create a new cluster with point 2
                    clusters[c] = [key2]
                    c = c + 1
                
                elif (findvalue(clusters,key1) == False) and (findvalue(clusters,key2) == True): # create a new cluster with point 1
                    clusters[c] = [key1]
                    c = c + 1
                
                elif (findvalue(clusters,key1) == False) and (findvalue(clusters,key2) == False): # add the 2 points to different clusters
                    clusters[c] = [key1]
                    c = c + 1
                    clusters[c] = [key2]
                    c = c + 1

print("Complete!")

print("\nNUMBER OF BIFURCATIONS:", len(clusters))
print("\nNUMBER OF ENDPOINTS:", len(points_endpoints))


print("\nDefining nodes...")

nodes = []
n_nodes = 1
for item in points_endpoints.items():
    list_points = [item[1]]
    new_node = Node("endpoint", n_nodes, list_points)
    nodes.append(new_node)
    n_nodes = n_nodes + 1

for item in clusters.items():
    list_points = item[1]
    list_coord = []
    for i in range(0,len(list_points)):
        point = list_points[i]
        coord = getvalues(points_bifurcations, point) # coordinates
        list_coord.append(coord)

    new_node = Node("bifurcation", n_nodes, list_coord)
    nodes.append(new_node)
    n_nodes = n_nodes + 1

print("Complete!")
print(len(nodes))

################################ Nº OF BLOOD VESSELS ################################

def find_points(matriz):

    coord_point = []
    coord_bif = []
    paths = 0
    for k in range(0, 3):
        for j in range(0, 3): 
            for i in range(0, 3):               
                if (matriz[i, j, k] == 1):
                    coord_point = [i, j, k]
                    paths = paths + 1
                elif (matriz[i, j, k] == 2 or matriz[i, j, k] == 5):
                    coord_bif = [i, j, k]
    
    return [coord_point, coord_bif, paths]


def find_node(node_point):
    print(node_point)

    node = None
    position = -1 

    while (position < len(nodes) and node == None):
        position = position + 1  
        n = nodes[position]  
        p = n.findPoint(node_point)
        if p != None:
            node = n
        
    return node


print("\nCounting the number of blood vessels and their size...")

n_vessel = 1
vessels = []
for node in nodes:

    if (node.category == "endpoint"):

        end = False
        initial_point = node.list_points[0]
        i = initial_point[0]
        j = initial_point[1]
        k = initial_point[2]
        new_array[i,j,k] = 6
        initial_node = node
        #points_vessel = []
        points_vessel = [initial_point]

        while (end == False):

            M = new_array[i-1:i+2, j-1:j+2, k-1:k+2]
            coord_point = find_points(M)[0]
            coord_bif = find_points(M)[1]

            if (len(coord_point) > 0) and (len(coord_bif) == 0):
                i = i + coord_point[0] - 1
                j = j + coord_point[1] - 1
                k = k + coord_point[2] - 1
                new_array[i,j,k] = n_vessel + 6
                points_vessel.append((i, j, k))
            
            elif (len(coord_bif) > 0):

                final_point = (i+coord_bif[0]-1, j+coord_bif[1]-1, k+coord_bif[2]-1)
                points_vessel.append(final_point) 
                final_node = find_node(final_point)
                vessels.append(Vessel(n_vessel, points_vessel, initial_node, final_node))
                end = True
                n_vessel = n_vessel + 1  
                
                # somar vaso ao nodo inicial e final
            
            else:
                end = True

    elif (node.category == "bifurcation"):

        n_points = len(node.list_points) #-1
        
        for m in range(n_points):

            initial_point = node.list_points[m]
            i = initial_point[0]
            j = initial_point[1]
            k = initial_point[2]
            M = new_array[i-1:i+2, j-1:j+2, k-1:k+2]
            coord_point = find_points(M)[0]
            coord_bif = find_points(M)[1]
            n_paths = find_points(M)[2]
            new_array[i,j,k] = 5 
          
            if (len(coord_point) > 0):
                for n in range(n_paths):
                    i = initial_point[0]
                    j = initial_point[1]
                    k = initial_point[2]
                    initial_node = node
                    #points_vessel = []
                    points_vessel = [initial_point]
                    end = False
    
                    while (end == False):

                        M = new_array[i-1:i+2, j-1:j+2, k-1:k+2]
                        coord_point = find_points(M)[0]
                        coord_bif = find_points(M)[1]

                        if (len(coord_point) > 0):
                            i = i + coord_point[0] - 1
                            j = j + coord_point[1] - 1
                            k = k + coord_point[2] - 1
                            new_array[i,j,k] = n_vessel + 6
                            points_vessel.append((i, j, k))
                                                        
                        elif (len(coord_bif) > 0):
                            final_point = (i+coord_bif[0]-1, j+coord_bif[1]-1, k+coord_bif[2]-1)  
                            points_vessel.append(final_point) 
                            final_node = find_node(final_point)

                            vessels.append(Vessel(n_vessel, points_vessel, initial_node, final_node))
                            end = True
                            n_vessel = n_vessel + 1
                            
                            # somar vaso ao nodo inicial e final
                        
                        else:
                            end = True

n_vessel =  n_vessel - 1
print("Complete!")

print("\nNUMBER OF VESSELS:", n_vessel)  

print("\nCalculating the diameter of each vessel...")

for point1 in points_volume:
    p = None
    distance = 9999999999999
    for point2 in points_skeleton:
        pt_1 = np.array((point1[0], point1[1], point1[2]))
        pt_2 = np.array((point2[0], point2[1], point2[2]))
        d = np.linalg.norm(pt_1-pt_2)
        if d < distance:
            distance = d
            p = point2
  
    for vessel in vessels:
        if vessel.findPoint(p) == True:
            vessel.update_volume()
    
for vessel in vessels:
    vessel.set_others()
    #print(vessel.list_points)
    print("n", vessel.n_vessel, "Volume:", vessel.volume, "Radius:", vessel.radius)


#################################### BLOOD FLOW  ####################################

C = np.zeros((n_vessel, n_nodes)) # matriz de conectividade
S = np.zeros((n_nodes,1)) # vetor com as pressões






