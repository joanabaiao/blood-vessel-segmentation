import numpy as np
import load_write as lw

##################################### THINNING ###################################### 

# Article: A 3D 6-subiteration thinning algorithm for extracting medial lines
# Authors of the article: Kalman Palagyi and Attila Kuba

##################################### OPEN FILE #####################################

filename_input = "cubo.vti"
filename_output = "test.vti"

array3D = lw.load_file_vti(filename_input)
deleted_points = []

dimensions = np.shape(array3D)
nx = dimensions[0]
ny = dimensions[1]
nz = dimensions[2]

####################################### MASKS ####################################### 
 
# black point: 1 (image)
# white point: 0 (background) 
# potential black x: 2 
# don't care point: 3

# MASK 1
M1 = np.zeros((3, 3, 3), dtype=int)

M1[0, 0, 0] = 0
M1[0, 0, 1] = 0
M1[0, 0, 2] = 0
M1[0, 1, 0] = 0
M1[0, 1, 1] = 0
M1[0, 1, 2] = 0
M1[0, 2, 0] = 0
M1[0, 2, 1] = 0
M1[0, 2, 2] = 0

M1[1, 0, 0] = 2
M1[1, 0, 1] = 2
M1[1, 0, 2] = 2
M1[1, 1, 0] = 2
M1[1, 1, 1] = 1
M1[1, 1, 2] = 2
M1[1, 2, 0] = 2
M1[1, 2, 1] = 2
M1[1, 2, 2] = 2

M1[2, 0, 0] = 2
M1[2, 0, 1] = 2
M1[2, 0, 2] = 2
M1[2, 1, 0] = 2
M1[2, 1, 1] = 1
M1[2, 1, 2] = 2
M1[2, 2, 0] = 2
M1[2, 2, 1] = 2
M1[2, 2, 2] = 2

# MASK 2
M2 = np.zeros((3, 3, 3), dtype=int)

M2[0, 0, 0] = 0
M2[0, 0, 1] = 0
M2[0, 0, 2] = 3
M2[0, 1, 0] = 0
M2[0, 1, 1] = 0
M2[0, 1, 2] = 3
M2[0, 2, 0] = 0
M2[0, 2, 1] = 0
M2[0, 2, 2] = 3

M2[1, 0, 0] = 3
M2[1, 0, 1] = 3
M2[1, 0, 2] = 3
M2[1, 1, 0] = 3
M2[1, 1, 1] = 1
M2[1, 1, 2] = 1
M2[1, 2, 0] = 3
M2[1, 2, 1] = 3
M2[1, 2, 2] = 3

M2[2, 0, 0] = 3
M2[2, 0, 1] = 3
M2[2, 0, 2] = 3
M2[2, 1, 0] = 3
M2[2, 1, 1] = 1
M2[2, 1, 2] = 3
M2[2, 2, 0] = 3
M2[2, 2, 1] = 3
M2[2, 2, 2] = 3


# MASK 3
M3 = np.zeros((3, 3, 3), dtype=int)

M3[0, 0, 0] = 0
M3[0, 0, 1] = 0
M3[0, 0, 2] = 3
M3[0, 1, 0] = 0
M3[0, 1, 1] = 0
M3[0, 1, 2] = 3
M3[0, 2, 0] = 3
M3[0, 2, 1] = 3
M3[0, 2, 2] = 3

M3[1, 0, 0] = 3
M3[1, 0, 1] = 3
M3[1, 0, 2] = 3
M3[1, 1, 0] = 3
M3[1, 1, 1] = 1
M3[1, 1, 2] = 1
M3[1, 2, 0] = 3
M3[1, 2, 1] = 1
M3[1, 2, 2] = 3

M3[2, 0, 0] = 3
M3[2, 0, 1] = 3
M3[2, 0, 2] = 3
M3[2, 1, 0] = 3
M3[2, 1, 1] = 1
M3[2, 1, 2] = 3
M3[2, 2, 0] = 3
M3[2, 2, 1] = 3
M3[2, 2, 2] = 3

# MASK 4
M4 = np.zeros((3, 3, 3), dtype=int)

M4[0, 0, 0] = 0
M4[0, 0, 1] = 0
M4[0, 0, 2] = 0
M4[0, 1, 0] = 0
M4[0, 1, 1] = 0
M4[0, 1, 2] = 0
M4[0, 2, 0] = 0
M4[0, 2, 1] = 0
M4[0, 2, 2] = 1

M4[1, 0, 0] = 3
M4[1, 0, 1] = 3
M4[1, 0, 2] = 3
M4[1, 1, 0] = 3
M4[1, 1, 1] = 1
M4[1, 1, 2] = 3
M4[1, 2, 0] = 3
M4[1, 2, 1] = 3
M4[1, 2, 2] = 1

M4[2, 0, 0] = 3
M4[2, 0, 1] = 3
M4[2, 0, 2] = 3
M4[2, 1, 0] = 3
M4[2, 1, 1] = 1
M4[2, 1, 2] = 3
M4[2, 2, 0] = 3
M4[2, 2, 1] = 3
M4[2, 2, 2] = 3

# MASK 5
M5 = np.zeros((3, 3, 3), dtype=int)

M5[0, 0, 0] = 0
M5[0, 0, 1] = 0
M5[0, 0, 2] = 0
M5[0, 1, 0] = 0
M5[0, 1, 1] = 0
M5[0, 1, 2] = 0
M5[0, 2, 0] = 0
M5[0, 2, 1] = 0
M5[0, 2, 2] = 0

M5[1, 0, 0] = 0
M5[1, 0, 1] = 2
M5[1, 0, 2] = 2
M5[1, 1, 0] = 0
M5[1, 1, 1] = 1
M5[1, 1, 2] = 2
M5[1, 2, 0] = 0
M5[1, 2, 1] = 2
M5[1, 2, 2] = 2

M5[2, 0, 0] = 0
M5[2, 0, 1] = 2
M5[2, 0, 2] = 2
M5[2, 1, 0] = 0
M5[2, 1, 1] = 0
M5[2, 1, 2] = 1
M5[2, 2, 0] = 0
M5[2, 2, 1] = 2
M5[2, 2, 2] = 2


# MASK 6
M6 = np.zeros((3, 3, 3), dtype=int)

M6[0, 0, 0] = 0
M6[0, 0, 1] = 0
M6[0, 0, 2] = 0
M6[0, 1, 0] = 0
M6[0, 1, 1] = 0
M6[0, 1, 2] = 0
M6[0, 2, 0] = 0
M6[0, 2, 1] = 0
M6[0, 2, 2] = 0

M6[1, 0, 0] = 0
M6[1, 0, 1] = 0
M6[1, 0, 2] = 3
M6[1, 1, 0] = 0
M6[1, 1, 1] = 1
M6[1, 1, 2] = 3
M6[1, 2, 0] = 3
M6[1, 2, 1] = 3
M6[1, 2, 2] = 3

M6[2, 0, 0] = 0
M6[2, 0, 1] = 0
M6[2, 0, 2] = 3
M6[2, 1, 0] = 0
M6[2, 1, 1] = 0
M6[2, 1, 2] = 1
M6[2, 2, 0] = 3
M6[2, 2, 1] = 1
M6[2, 2, 2] = 3

##################################### FUNCTIONS #####################################

# Axis:
# x -> 0; y -> 1; z -> 2
# The 'axes' define the plane where the rotation occurs

def rotation_vertical(matrix, angle, direction):
  
    M = matrix

    if direction == "U" or direction == "D":
        if angle == 90:
            M = np.rot90(M, k=1, axes= (1,2))
        elif angle == 180:
            M = np.rot90(M, k=2, axes=(1,2))
        elif angle == 270:
            M = np.rot90(M, k=3, axes=(1,2))
    
    elif direction == "N" or direction == "S":
        if angle == 90:
            M = np.rot90(M, k=1, axes= (1,0))
        elif angle == 180:
            M = np.rot90(M, k=2, axes=(1,0))
        elif angle == 270:
            M = np.rot90(M, k=3, axes=(1,0))

    elif direction == "W" or direction == "E":
        if angle == 90:
            M = np.rot90(M, k=1, axes= (2,0))
        elif angle == 180:
            M = np.rot90(M, k=2, axes=(2,0))
        elif angle == 270:
            M = np.rot90(M, k=3, axes=(2,0))
    
    return M


def rotation_direction(matrix, direction):

    M = matrix

    if direction == "D":
        M = np.rot90(M, k=2, axes=(0,2))
    
    elif direction == "N":
        M = np.rot90(M, k=1, axes=(2,0))
    
    elif direction == "S":
        M = np.rot90(M, k=1, axes=(0,2)) 
    
    elif direction == "E":
        M = np.rot90(M, k=1, axes=(1,0))

    elif direction == "W":
        M = np.rot90(M, k=1, axes=(0,1))
    
    return M

##################################### THINNING ###################################### 

def mask_application(mask, mask_name, direction):

    print(mask_name, direction)
    M_auxiliar = np.zeros((3, 3, 3), dtype=int)

    for k in range(1, nz-1):
        for j in range(1, ny-1): 
            for i in range(1, nx-1): 
                
                if array3D[i, j, k] == 1:
                    
                    cicle = False
                    angle = 0

                    if (direction == "U" or direction == "D") and (array3D[i, j, k] + array3D[i+1, j, k] + array3D[i-1, j, k] < 3):
                        cicle = True
                    
                    elif (direction == "N" or direction == "S") and (array3D[i, j, k] + array3D[i, j, k+1] + array3D[i, j, k-1] < 3):
                        cicle = True
                    
                    elif (direction == "W" or direction == "E") and (array3D[i, j, k] + array3D[i, j+1, k] + array3D[i, j-1, k] < 3):
                        cicle = True

                    while (cicle == True and angle < 360): # pára quando se muda o ponto ou se analisa com os ângulos na vertical

                        M_auxiliar = array3D[i-1:i+2, j-1:j+2, k-1:k+2] # Matriz que percorre o array3D
                        M = rotation_vertical(mask, angle, direction)

                        stop1 = False # pára o ciclo quando verifica todos os pontos
                        stop2 = False # verificar os 0 e 1 
                        valid = 0 # verificar os 2 ("pelo menos um ponto x é preto")

                        while (stop1 == False and stop2 == False):
                            
                            for z in range(0,3): # z           
                                    for y in range(0,3): # y            
                                            for x in range(0,3): # x 

                                                if (M[x,y,z] == 0 and M_auxiliar[x,y,z] != 0):
                                                    stop2 = True # se um ponto não coincidir pára 
                                                     
                                                elif (M[x,y,z] == 1 and M_auxiliar[x,y,z] != 1):
                                                    stop2 = True # se um ponto não coincidir pára 
                                                
                                                if (mask_name == "M1" or mask_name == "M5"):
                                                    if (M[x,y,z] == 2 and M_auxiliar[x,y,z] == 1):
                                                        valid = valid + 1 
                                                        
                                                else:
                                                    valid = 1

                                                if (x == 2 and y == 2 and z == 2):
                                                    stop1 = True
                               
                        if (stop2 == False and valid > 0):
                            deleted_points.append([i,j,k])
                            cicle = False

                        else: # quando o ponto não é eliminado a máscara roda na vertical e tentamos com outro ângulo
                            angle = angle + 90
    
    for s in range(len(deleted_points)):
        i = deleted_points[s][0]
        j = deleted_points[s][1]
        k = deleted_points[s][2]
        array3D[i,j,k] = 0

    size = len(deleted_points) 
    deleted_points.clear()

    return size


skeleton = False
list_cicle = []
n_cicle = 1

while (skeleton == False):
    print("\n--------------- CICLE:", n_cicle, "---------------\n")

    list_cicle.append(mask_application(M1, "M1", "U"))
    list_cicle.append(mask_application(M2, "M2", "U"))
    list_cicle.append(mask_application(M3, "M3", "U"))
    list_cicle.append(mask_application(M4, "M4", "U"))
    list_cicle.append(mask_application(M5, "M5", "U"))
    list_cicle.append(mask_application(M6, "M6", "U"))

    list_cicle.append(mask_application(rotation_direction (M1, "D"), "M1", "D"))
    list_cicle.append(mask_application(rotation_direction (M2, "D"), "M2", "D"))
    list_cicle.append(mask_application(rotation_direction (M3, "D"), "M3", "D"))
    list_cicle.append(mask_application(rotation_direction (M4, "D"), "M4", "D"))
    list_cicle.append(mask_application(rotation_direction (M5, "D"), "M5", "D"))
    list_cicle.append(mask_application(rotation_direction (M6, "D"), "M6", "D"))

    list_cicle.append(mask_application(rotation_direction (M1, "N"), "M1", "N"))
    list_cicle.append(mask_application(rotation_direction (M2, "N"), "M2", "N"))
    list_cicle.append(mask_application(rotation_direction (M3, "N"), "M3", "N"))
    list_cicle.append(mask_application(rotation_direction (M4, "N"), "M4", "N"))
    list_cicle.append(mask_application(rotation_direction (M5, "N"), "M5", "N"))
    list_cicle.append(mask_application(rotation_direction (M6, "N"), "M6", "N"))

    list_cicle.append(mask_application(rotation_direction (M1, "S"), "M1", "S"))
    list_cicle.append(mask_application(rotation_direction (M2, "S"), "M2", "S"))
    list_cicle.append(mask_application(rotation_direction (M3, "S"), "M3", "S"))
    list_cicle.append(mask_application(rotation_direction (M4, "S"), "M4", "S"))
    list_cicle.append(mask_application(rotation_direction (M5, "S"), "M5", "S"))
    list_cicle.append(mask_application(rotation_direction (M6, "S"), "M6", "S"))

    list_cicle.append(mask_application(rotation_direction (M1, "E"), "M1", "E"))
    list_cicle.append(mask_application(rotation_direction (M2, "E"), "M2", "E"))
    list_cicle.append(mask_application(rotation_direction (M3, "E"), "M3", "E"))
    list_cicle.append(mask_application(rotation_direction (M4, "E"), "M4", "E"))
    list_cicle.append(mask_application(rotation_direction (M5, "E"), "M5", "E"))
    list_cicle.append(mask_application(rotation_direction (M6, "E"), "M6", "E"))

    list_cicle.append(mask_application(rotation_direction (M1, "W"), "M1", "W"))
    list_cicle.append(mask_application(rotation_direction (M2, "W"), "M2", "W"))
    list_cicle.append(mask_application(rotation_direction (M3, "W"), "M3", "W"))
    list_cicle.append(mask_application(rotation_direction (M4, "W"), "M4", "W"))
    list_cicle.append(mask_application(rotation_direction (M5, "W"), "M5", "W"))
    list_cicle.append(mask_application(rotation_direction (M6, "W"), "M6", "W"))

    print("\nChanged points:", sum(list_cicle))

    if sum(list_cicle) == 0:
        skeleton = True
    
    n_cicle = n_cicle + 1
    list_cicle.clear()


#################################### WRITE FILE ##################################### 

lw.write_vti(filename_output, array3D)

