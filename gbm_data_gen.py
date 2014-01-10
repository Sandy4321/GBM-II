# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 16:29:16 2014

@author: Florian
"""

import numpy as np
from scipy import ndimage as ndi


class petroSim(object):
    
    def __init__(self, fieldInfo, uStartCondition, vStartCondition):
        
        self.xRange = fieldInfo[0]        
        self.dx     = fieldInfo[1]
                
        self.xlen   = round(self.xRange / self.dx)
        
        self.arrU = np.zeros((self.xlen, self.xlen))
        self.arrV = np.zeros((self.xlen, self.xlen)) 
                
        for x in range(round((uStartCondition[1] + 1) / self.dx), round(uStartCondition[2] / self.dx)):
            for y in range(round((uStartCondition[3] + 1) / self.dx), round(uStartCondition[4] / self.dx)):
                self.arrU[x][y] = uStartCondition[0]
        
        for x in range(round((vStartCondition[1] + 1) / self.dx), round(vStartCondition[2] / self.dx)):
            for y in range(round((vStartCondition[3] + 1) / self.dx), round(vStartCondition[4] / self.dx)):
                self.arrV[x][y] = vStartCondition[0]

    
    
    def step(self, dt, kernelU, kernelV, simParam):
        #Diffusion
        self.arrU = ndi.convolve(self.arrU, kernelU)
        self.arrV = ndi.convolve(self.arrV, kernelV)
        
        #Reaktion
        hollingII = dt * self.arrU * self.arrV / (1 + simParam[0] * self.arrU)
        arrUTemp = dt * simParam[2] * self.arrU * (self.arrU - simParam[1]) * (1 - self.arrU) - hollingII
        
        self.arrV += hollingII - dt * simParam[3] * self.arrV
        self.arrU += arrUTemp
    
        
    def solve(self, simParam, simTime):
        
        a = simTime[1] / self.dx**2
        kernelU = np.array(((0, a, 0), 
                            (a, 1 - 4 * a, a),
                            (0, a, 0)))
        
        a *= simParam[4]
        kernelV = np.array(((0, a, 0), 
                            (a, 1 - 4 * a, a),
                            (0, a, 0)))
               
        exportTime = 1 / simTime[1]
		
        for t in range(round(simTime[0] / simTime[1])):        
            self.step(simTime[1], kernelU, kernelV, simParam)
            if t % exportTime == (exportTime - 1):
                print(round((t + 1) / exportTime))
                self.exportData(round((t + 1) / exportTime))
            
        return (self.arrU, self.arrV)
    
    
    def exportData(self, t):
        
        filePath = "data/paramSet01/gbm"
        
        fileNameU = filePath + "_u_" + str(t) + ".dat"
        fileNameV = filePath + "_v_" + str(t) + ".dat"
        
        fileU = open(fileNameU, "w")
        fileV = open(fileNameV, "w")
        
        for x in range(0, self.xlen):
            for y in range(0, self.xlen):    
                _x = x * self.dx
                _y = y * self.dx
                _IndexString = str(_x) + " " + str(_y)                
                _UString = _IndexString + " " + str(self.arrU[x][y]) + "\n"
                _VString = _IndexString + " " + str(self.arrV[x][y]) + "\n"              
                
                fileU.write(_UString)
                fileV.write(_VString)
               
            fileU.write("\n")
            fileV.write("\n")
        
        fileU.close()
        fileV.close()
        

      
def simulate(fieldInfo, uStartCondition, vStartCondition, simParam, simTime):
    """
        Simulation Config
        @param fieldInfo: (xRange, dx)
        @param uStartCondition: (u0, x11, x12, y11, y12)
        @param vStartCondition: (v0, x21, x22, y21, y22)
        
        Simulation Parameter
        @param simParam: (alpha, beta, gamma, delta, epsilon)
        
        Simulation Time
        @param simTime: (tEnd, dt)
    """      
    
    #Setup Simulation
    sim = petroSim(fieldInfo, uStartCondition, vStartCondition)    
    
    #Run Simulation
    sim.solve(simParam, simTime)
             
    
if __name__ == '__main__':
    
    fieldInfo = (200, 1)
    simTime   = ( 10, 0.1)
    
    uStartCondition = (1.2, 85, 105, 100, 105)
    vStartCondition = (0.2, 85,  95,  95, 115)

    
    paramSet01 = (0.1, 0.2, 3.9, 0.5, 1.0)
    paramSet02 = (0.1, 0.2, 3.9, 0.37, 1.0)
    
    simulate(fieldInfo, uStartCondition, vStartCondition, paramSet01, simTime)