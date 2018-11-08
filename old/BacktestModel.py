import numpy as np
import matplotlib.pyplot as pplot

def PricePath(n,T,S0,K,FuncSimulatePath,FuncModelPrice,ModelParams):
    vectS = FuncSimulatePath(n,T,S0,ModelParams)
    vectP = np.zeros(n+1)
    for i in range(0,n+1):
        vectP[i] = FuncModelPrice(T*(1-i/n),vectS[i],K,ModelParams)
    return vectP

def DeltaHedgeMod(n,T,S0,K,FuncSimulatePath,FuncModelPrice,FuncModelDelta,FuncReturnZC,ModelParams):
    vectS = FuncSimulatePath(n,T,S0,ModelParams)
    vectC = np.zeros(n+1)
    vectDelta = np.zeros(n+1)
    vectP = np.zeros(n+1)
    
    for i in range(0,n+1):
        vectC[i] = FuncModelPrice(T*(1-i/n),vectS[i],K,ModelParams)
        vectDelta[i] = FuncModelDelta(T*(1-i/n),vectS[i],K,ModelParams)
        if i == 0:
            vectP[i] = vectC[0]
        else:
            vectP[i] = vectP[i-1] + (FuncReturnZC(T/n,ModelParams)-1) * (vectP[i-1]-vectDelta[i-1]*vectS[i-1]) + vectDelta[i-1] * (vectS[i]-vectS[i-1])        
            
    vectTime = [x * T/n for x in range(0, n+1, 1)]
    pplot.plot(vectTime,vectP)
    pplot.plot(vectTime,vectC)
    pplot.show()
    
def DeltaHedgeMis(n,T,S0,K,FuncSimulatePath,FuncModelPrice,FuncModelDelta,FuncReturnZC,ModelSimuParams,ModelPriceParams):
    vectS = FuncSimulatePath(n,T,S0,ModelSimuParams)
    vectC = np.zeros(n+1)
    vectDelta = np.zeros(n+1)
    vectP = np.zeros(n+1)
    
    for i in range(0,n+1):
        vectC[i] = FuncModelPrice(T*(1-i/n),vectS[i],K,ModelPriceParams)
        vectDelta[i] = FuncModelDelta(T*(1-i/n),vectS[i],K,ModelPriceParams)
        if i == 0:
            vectP[i] = vectC[0]
        else:
            vectP[i] = vectP[i-1] + (FuncReturnZC(T/n,ModelPriceParams)-1) * (vectP[i-1]-vectDelta[i-1]*vectS[i-1]) + vectDelta[i-1] * (vectS[i]-vectS[i-1])        
            
    vectTime = [x * T/n for x in range(0, n+1, 1)]
    pplot.plot(vectTime,vectP)
    pplot.plot(vectTime,vectC)
    pplot.show()