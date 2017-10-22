#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import numpy.matlib
import math

N=3 #N: Number of input neurons (0≤i<N)
L=4 #L: Number of hidden neurons (0≤j<L)
M=N*L #M: Number of output neurons (0≤k<M)
Q = 6 #Q: Number of learning patterns (0≤p<Q)
alpha = 0.5

x = np.matlib.zeros((N, Q), dtype=np.int) #Inputs
wh = np.matlib.zeros((L, N), dtype=np.int)
yh = np.array(np.zeros((L,), dtype=np.float))
wo = np.matlib.zeros((M, L), dtype=np.int)
d = np.matlib.zeros((M, Q), dtype=np.int)
y = np.array(np.zeros((M,), dtype=np.float))
wh = np.matlib.zeros((L, N), dtype=np.int)
neth = np.array(np.zeros((L,), dtype=np.int))
deltao = np.array(np.zeros((M,), dtype=np.float))
deltah = np.array(np.zeros((L,), dtype=np.float))
error = 0

def multipercep():
	calc_neth()
	calc_yh()
	calc_neto()
	calc_y()
	calc_deltao()
	calc_deltah()
	calc_wo()
	calc_wh()
	calc_error()
	 

def calc_wo():
	for k in range(M):
		for j in range(L):
			wo[k][j]+=alpha*deltao[k]*yh[j]
					
def calc_wh():		
	for j in range(L):
		for i in range(L):
			wh[j][i]+=alpha*deltah[j]*x[i][p]
			
def calc_neth():
	for p in range(Q):
		for j in range(L):
			for i in range(N):
				neth[j]+=x[i][p]*wh[j][i]
	
def calc_neto():
	for k in range(M):
		for j in range(L):
			neto[k] += yh[j]*wo[k][j]

def calc_yh():
	neth = calc_neth()
	for j in range(L):
		y[j] = f(neth[j])
		
def calc_y():
	for k in range(M):
		y[k] = f(neto[k])
	
def f(x):
	 return 1/(1+math.exp(-x))
	
def calc_deltao():
	for k in range(M):
		for p in range(Q):
			deltao[k]=(d[k][p]-y[k])*y[k]*(1-y[k])
			
def calc_deltah():
	for j in range(L):
		temp = 0
		for k in range(M):
			temp += deltao[k]*wo[k][j]
		deltah[j]=yh[j]*(1-yh[j])*temp
	
def calc_error():
	for k in range(M):
		error += pow(deltao[k],2)
	
			
#if __name__ == '__main__':
	
 
		
