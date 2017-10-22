#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from math import pi, cos, sin

class punto(object):
    def __init__(self, values=[0,0]): self.values = values

    def __getitem__(self, i): return self.values[i]

    def __iter__(self): 
        return iter(self.values)
            
    def __len__(self): return len(self.values)
    
    def __str__(self): return str(self.values)

    def distanciaA(self, p):
        distancia = 0
        for c, i in enumerate(p):
            distancia += abs(self.values[c] - i) 
        return distancia


#Verifica que sea una lista de puntos
def verificarListaPuntos(puntos):
    for i in puntos:
        if type(punto()) != type(i):
            return False
    return True

#Ésta función revisa que todos los puntos tengan las mismas dimensiones
def VerificarTamanos(puntos):
    if verificarListaPuntos(puntos):
        for i, p in enumerate(puntos):
            if len(p) != len(puntos[i-1]):
                return False
        return True
    return False

def calcularCentro(puntos):
    if VerificarTamanos(puntos):
        centro = punto([0.0] * len(puntos[0]))
        for p in puntos:
            for i in range(len(centro)):
                centro.values[i] += p[i]
        for i in range(len(centro)):
            centro.values[i] /= len(puntos)
        return centro
    return None

def calcularRadio(puntos, centro):
    cercano = puntos[0]
    lejano = puntos[-1]
    
    for p in puntos:
        if centro.distanciaA(p) < cercano:
            cercano = p
            
        elif centro.distanciaA(p) > lejano:
            lejano = p
    
    return cercano.distanciaA(lejano)/2
    return None

#Da las coordenadas a los centroides. Ésta función solo sirve para 2D
def ponerCentroides(centroides, centro, radio):
    tetha = 2*pi/len(centroides)
    for count, p in enumerate(centroides):
        p.values[0] = centro[0] + radio*cos(tetha*count)
        p.values[1] = centro[1] + radio*sin(tetha*count)
    return centroides

b = []
b.append(punto([1, 5]))
b.append(punto([5, 9]))


centro = calcularCentro(b)
print (centro)
print (calcularRadio(b, centro))
