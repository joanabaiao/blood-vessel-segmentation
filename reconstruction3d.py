from PIL import Image
import numpy as np
import cv2 
import os 
import glob 

x = 292
y = 451
z = 350

array3d = np.zeros((x,y,z))

lista = []
m = 0
for i in range(0,345,6): 
    print(m)
    img_dir = "/Users/joana/Documents/Biologia computacional/Imagens/Planos/" + str(m) + ".png"
    img = Image.open(img_dir)
    array = np.array(img)
    print(array.shape)
    array3d[:,50:451,i] = array[:,50:451,0]
    array3d[:,50:451,i+1] = array[:,50:451,0]
    array3d[:,50:451,i+2] = array[:,50:451,0]
    array3d[:,50:451,i+3] = array[:,50:451,0]
    array3d[:,50:451,i+4] = array[:,50:451,0]
    array3d[:,50:451,i+5] = array[:,50:451,0]

    m = m + 1


# CONVERTER MATRIZ PARA FORMATO VTI 

lista1 = [] # criação de uma lista com os valores do array 3D 'phi'

for iz in range(z):
    for iy in range(y):
        for ix in range(x):
            a = array3d[ix,iy,iz]
            if (a < 200):
                lista1.append(0)
            else:
                lista1.append(1)

string1 = "    ".join([str(_) for _ in lista1]) # criação de uma string com os valores da lista

with open("novo2.vti", "w" ) as new_file:
    new_file.write('<?xml version="1.0"?>')
    new_file.write('<VTKFile type="ImageData" version="0.1" byte_order="LittleEndian">\n')
    new_file.write('  <ImageData WholeExtent="0 292 0 451 0 350" Origin="0 0 0" Spacing ="1 1 1">\n')
    new_file.write('    <Piece Extent="0 292 0 451 0 350">\n') # dimensão da matriz x1 x2 y1 y2 z1 z2
    new_file.write('     <CellData>\n')
    new_file.write('     <DataArray Name="scalar_data" type="Float64" format="ascii">\n')
    new_file.write('     ')
    new_file.write(string1)
    new_file.write('\n         </DataArray>\n')
    new_file.write('      </CellData>\n')
    new_file.write('    </Piece>\n')
    new_file.write('</ImageData>\n')
    new_file.write('</VTKFile>\n')
    new_file.close() # fecha o ficheiro

