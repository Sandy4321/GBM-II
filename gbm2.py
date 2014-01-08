# coding: utf-8

'''
Created on 19.12.2013

@author: Samuel
'''


import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm


def pr(arr):
    for i in arr:
        for j in i:
            print(j, "; ")
        print()
    print()
    print()

class petroSim(object):
    
    def __init__(self, xRange, dx, u0, v0, x11, x12, y11, y12, x21, x22, y21, y22):
        
        self.dx = dx
        self.xRange = xRange
        
        self.xlen = xlen = round(xRange / dx)
        
        self.arrU = np.zeros((xlen, xlen)) #2d array
        self.arrV = np.zeros((xlen, xlen)) #2d array
           
        
        for x in range(round((x11+1)/dx), round(x12/dx)):
            for y in range(round((y11+1)/dx), round(y12/dx)):
                self.arrU[x, y] = u0
        
        for x in range(round((x21+1)/dx), round(x22/dx)):
            for y in range(round((y21+1)/dx), round(y22/dx)):
                self.arrV[x, y] = v0
                
    
    
    def step(self, dt, kernelU, kernelV, alpha, beta, gamma, delta):
        
        #Diffusion
        self.arrU = ndi.convolve(self.arrU, kernelU)
        self.arrV = ndi.convolve(self.arrV, kernelV)
        
        #Reaktion
        hollingII = dt * self.arrU * self.arrV / (1 + alpha * self.arrU)
        arrUTemp = dt * gamma * self.arrU * (self.arrU - beta) * (1 - self.arrU) - hollingII
        
        self.arrV += hollingII - dt * delta * self.arrV
        self.arrU += arrUTemp
    
        
    def solve(self, tend, dt, alpha, beta, gamma, delta, epsilon):
        
        a = dt / self.dx**2
        kernelU = np.array(((0, a, 0), 
                          (a, 1-4*a, a),
                          (0, a, 0)))
        
        a *= epsilon
        kernelV = np.array(((0, a, 0), 
                          (a, 1-4*a, a),
                          (0, a, 0)))
        
        for t in range(round(tend / dt)):
            self.step(dt, kernelU, kernelV, alpha, beta, gamma, delta)
          
        #print(tend / dt)
        #self.exportData(tend)
          
        return (self.arrU, self.arrV)
    
    
    def exportData(self, t):
        
        filePath = "data/gbm"
        
        fileNameU = filePath + "_u_" + str(t) + ".dat"
        fileNameV = filePath + "_v_" + str(t) + ".dat"
        
        fileU = open(fileNameU, "w")
        fileV = open(fileNameV, "w")
        
        for x in range(0, self.xlen):
            for y in range(0, self.xlen):    
                _IndexString = str(x) + " " + str(y)                
                _UString = _IndexString + " " + str(self.arrU[x][y]) + "\n"
                _VString = _IndexString + " " + str(self.arrV[x][y]) + "\n"              
                
                fileU.write(_UString)
                fileV.write(_VString)
               
            fileU.write("\n")
            fileV.write("\n")
        
        fileU.close()
        fileV.close()
    
   
        

def simulate(config, param, times, p3D = True):
    s = petroSim(*config)
    
    for i, t in enumerate(times):
        print(i)
        s.solve(*((t - (times[i-1] if i > 0 else 0), ) + param))
        s.exportData(i)
        
def sim1(p3D = True):
    
    liste = [1]
    for i in range(2, 202):
        liste.append(i)
        
    simulate((200, 1, 1.2, 0.2, 85, 105, 100, 105, 85, 95, 95, 115),
             (0.1, 0.1, 0.2, 3.9, 0.5, 1),
             liste, p3D)
    
def sim2(p3D = True):
    simulate((200, 1, 1.2, 0.2, 85, 105, 100, 105, 85, 95, 95, 115),
             (0.1, 0.1, 0.2, 3.9, 0.37, 1),
             (20, 40, 50, 70, 150, 240), p3D)
    
    
    

 
if __name__ == '__main__':
    sim1(True)