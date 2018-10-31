import numpy as np
#import scipy.stats as ss 
#import scipy.optimize as spo
#import matplotlib.pyplot as pplot
#import math as math
import Utils as use

def PrintModelParamsNames():
    print("ModelParams[0] := r")
    print("ModelParams[1] := v0")
    print("ModelParams[2] := kappa")
    print("ModelParams[3] := theta")
    print("ModelParams[4] := xi")
    print("ModelParams[5] := rho")

def TestParams(ModelParams):
    r = ModelParams[0]
    v0 = ModelParams[1]
    kappa = ModelParams[2]
    theta = ModelParams[3]
    xi = ModelParams[4]
    rho = ModelParams[5]
    return use.MsgParams((r>0)and(v0>0)and(2*kappa*theta > xi**2)and(xi>0)and(rho <= 1)and(rho>=-1))

def SimulatePath(n,S0,r,v0,kappa,theta,xi,rho,T):
    G = np.random.multivariate_normal([0,0],[[1,rho],[rho,1]],n)
    S=np.zeros(n+1)
    dt = T/n
    S[0]=S0
    v=v0
    for i in range(1,n+1):
        S[i]=S[i-1]*(1+r*dt+np.sqrt(v*dt)*G[i-1,0])
        v=v+kappa*(theta-v)*dt+xi*np.sqrt(v*dt)*G[i-1,1]
    return S

def FuncSimulatePath(n,T,S0,ModelParams):
    if TestParams(ModelParams)==False:
        return 0
    else:
        return SimulatePath(n,S0,ModelParams[0],ModelParams[1],ModelParams[2],ModelParams[3],ModelParams[4],ModelParams[5],T)

