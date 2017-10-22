from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from math import ceil
import random
from colorsys import rgb_to_hsv, hsv_to_rgb

precision = 12

def listToHSV(listaRGB):
    listHSV = []
    for pixel in listaRGB:
        listHSV.append(rgb_to_hsv(pixel[0], pixel[1], pixel[2]))
    return listHSV

def listToRGB(listaHSV):
    listRGB = []
    for pixel in listaHSV:
        listRGB.append(hsv_to_rgb(pixel[0], pixel[1], pixel[2]))
    return listRGB

def leerImg(img):
    listHSV = listToHSV(list(img.getdata()))
    listHSV.sort(key=lambda x: x[0], reverse=True)
    listRGB = listToRGB(listHSV)
    for pixel in listRGB:
        yield colorK(pixel[0], pixel[1], pixel[2])

class colorK:
    def __init__(self, R = 255, G = 255, B = 255):
        self.R = R
        self.G = G
        self.B = B
        self.modificado = False
    
    def acercarA(self, punto, divisor):
        self.R=self.R+(punto.R-self.R)/divisor
        self.G=self.G+(punto.G-self.G)/divisor
        self.B=self.B+(punto.B-self.B)/divisor
        if not self.modificado:
            self.modificado = True
    
    def distancia(self, punto):
        return abs(punto.R-self.R)+abs(punto.G-self.G)+abs(punto.B-self.B)

    def centroideMasCercano(self, centroides):
        centroide = centroides[0]
        for c in centroides:
            if (self.distancia(c) < self.distancia(centroide)):
                 centroide = c
        return centroide

    def reemplazarColor(self, c):
        self.R = c.R
        self.G = c.G
        self.B = c.B

    def __str__(self):
        return ("("+str(self.R)+", "+str(self.G)+", "+str(self.B)+")")

def colorKToList(c):
    return (int(c.R), int(c.G), int(c.B))

def listToColorK(l):
    return colorK(l[0], l[1], l[2])

def guardarCentroides(centroides):
    f = open('centroides.txt', 'w')
    for i in centroides:
        f.write(str(i))
    f.close()

def kohonen(puntos, centroides):
    for i in range(2, precision):
        for p in puntos:
            centroide = centroides[0]
            for c in centroides:
                if (p.distancia(c) < p.distancia(centroide)):
                    centroide = c
            centroide.acercarA(p, i)
    eliminaCentroides(centroides)

def test_img(img):
    temp = None
    for pixel in list(img.getdata()):
        if temp!=pixel:
            temp = pixel
            print(pixel)
            #raw_input()

def eliminaCentroides(centroides):
    centroides[:] = [c for c in centroides if c.modificado]

def crearModelo3D(img, centroides):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('R Label')
    ax.set_ylabel('G Label')
    ax.set_zlabel('B Label')
    for p in leerImg(img):
        ax.scatter(p.R, p.G, p.B, c="r", marker='o')
    for c in centroides:
        ax.scatter(c.R, c.G, c.B, c="b", marker='o')
    
    plt.savefig('graphic3D.png')
    plt.show()

def dibujaCentroides(old_img, centroides):
    old_size = old_img.size
    new_size = (old_size[0], old_size[1]+100)
    new_im = Image.new("RGB", new_size, (255,255,255))
    new_im.paste(old_img, (0,0))
    d = ImageDraw.Draw(new_im)
    for count, c in enumerate(centroides):
        d.rectangle([(20*count,old_size[1]+10),(20*count+10,old_size[1]+20)], fill=(int(c.R), int(c.G), int(c.B)))
    new_im.save('colores.png')
    new_im.show()

def creaCentroides(cant):
    divisor = ceil(cant ** (1.0/3))
    centroides = [colorK() for i in range(cant)]
    rango = 254/divisor
    
    for n in range(3):
        for i, c in enumerate(centroides):
            if n==0:
                c.R = int(random.random()*rango)+((i+n)%divisor)*rango
            elif n==1:
                c.G = int(random.random()*rango)+((i+n)%divisor)*rango
            else:
                c.B = int(random.random()*rango)+((i+n)%divisor)*rango

    return centroides

def reemplazaPixeles(img, centroides):
    pixelMap = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixelMap[i,j] = colorKToList(listToColorK(pixelMap[i,j]).centroideMasCercano(centroides))
    return img

if __name__ == '__main__':
    img = Image.open(sys.argv[1])
    puntos = leerImg(img)
    centroides = creaCentroides(2)
    kohonen(puntos, centroides)
    #crearModelo3D(img, centroides)
    dibujaCentroides(img, centroides)
    guardarCentroides(centroides)
    img = reemplazaPixeles(img, centroides)
    img.save("kohonen.png")
    img.show()