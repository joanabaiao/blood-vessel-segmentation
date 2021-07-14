import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy

##################################### OPEN FILE ##################################### 

# Função para abrir um ficheiro VTK 
def load_file_vtk(filename_input):

    print("\nLoading file...")
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(filename_input)
    reader.Update()
    data = reader.GetOutput()
    dimensions = data.GetDimensions()
    array = vtk_to_numpy(data.GetPointData().GetScalars())

    x = dimensions[0]
    y = dimensions[1]
    z = dimensions[2]

    array3D = np.empty((x, y, z)) 

    n = 0
    for k in range(z): # z
        for j in range(y): # y 
            for i in range(x): # x
                m = int(float(array[n])) # converter string para número
                if (m > 60):
                    array3D[i,j,k] = 1
                else:
                    array3D[i,j,k] = 0
                n = n + 1
    
    print("Complete!")
    
    return array3D

# Função para abrir um ficheiro VTI
def load_file_vti (filename_input):

    print("\nLoading file - VTI")  
    new_file =  open(filename_input, "r")
    lines =  new_file.readlines() 
    data = lines[5]
    array = data.split()

    dimensions_string = lines[2]
    dimensions = [int(s) for s in dimensions_string.split() if s.isdigit()]

    x = dimensions[1]
    y = dimensions[3]
    z = dimensions[5]

    array3D = np.empty((x, y, z)) 

    n = 0
    for k in range(z): # z
        for j in range(y): # y 
            for i in range(x): # x
                m = int(float(array[n])) # converter string para número
                array3D[i,j,k] = m
                n = n + 1
    
    print("Complete!")
    
    return array3D


#################################### WRITE FILE ##################################### 

# Função para escrever um array num ficheiro VTI
def write_vti(filename_output, matrix):
    
    print("\nWriting file...")

    dimensions = np.shape(matrix)
    x = dimensions[0]
    y = dimensions[1]
    z = dimensions[2]

    new_list = [] # criação de uma lista com os valores do array 3D 'phi'
    for k in range(z):
        for j in range(y):
            for i in range(x):
                a = matrix[i,j,k]
                new_list.append(a)

    list_string = "    ".join([str(_) for _ in new_list]) # criação de uma string com os valores da lista

    size = " 0 " + str(x) + " 0 " + str(y) + " 0 " + str(z) + " 0 "
    s1 = '  <ImageData WholeExtent = "' + size + '" Origin = " 0 0 0 " Spacing = " 1 1 1 ">\n'
    s2 = '    <Piece Extent = "' + size + '" >\n'

    with open(filename_output, "w") as new_file:
        new_file.write('<?xml version="1.0"?>')
        new_file.write('<VTKFile type = "ImageData" version = "0.1" byte_order = "LittleEndian">\n')
        new_file.write(s1)
        new_file.write(s2)
        new_file.write('     <CellData>\n')
        new_file.write('     <DataArray Name = "scalar_data" type = "Float64" format = "ascii">\n')
        new_file.write('     ')
        new_file.write(list_string)
        new_file.write('\n         </DataArray>\n')
        new_file.write('      </CellData>\n')
        new_file.write('    </Piece>\n')
        new_file.write('</ImageData>\n')
        new_file.write('</VTKFile>\n')
        new_file.close()
    
    print("Complete!")
   
    return

