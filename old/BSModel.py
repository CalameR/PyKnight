import numpy as np
import scipy.stats as ss 
import scipy.optimize as spo
import matplotlib.pyplot as pplot
import math as math
import Utils as use

def PrintModelParamsNames():
    print("ModelParams[0] := r")
    print("ModelParams[1] := sigma")

def TestParams(ModelParams):
    r=ModelParams[0]
    sigma=ModelParams[1]
    return use.MsgParams((r>0)and(sigma>0))

def SimulateT(S0,r,sigma,T):
    G = np.random.randn()
    return S0*np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*G)

def SimulatePath(n,S0,r,sigma,T):
    G = np.random.randn(n)
    S=np.zeros(n+1)
    dt = T/n
    S[0]=S0
    for i in range(1,n+1):
        S[i]=S[i-1]*np.exp((r-sigma**2/2)*dt+sigma*np.sqrt(dt)*G[i-1])
    return S

def FuncSimulatePath(n,T,S0,ModelParams):
    if TestParams(ModelParams)==False:
        return 0
    else:
        return SimulatePath(n,S0,ModelParams[0],ModelParams[1],T)

def d1(S0, K, r, sigma, T):
    m = S0/(K*np.exp(-r*T))
    return np.log(m) * (1/(sigma*np.sqrt(T))) + sigma * np.sqrt(T) / 2

def d2(S0, K, r, sigma, T):
    return d1(S0,K,r,sigma,T) - sigma * np.sqrt(T)
 
def Price(S0, K, r, sigma, T, type = "C"):
    if type=="C":
        if T==0:
            return np.maximum(S0 - K,0)
        else:
            return S0 * ss.norm.cdf(d1(S0, K, r, sigma, T)) - K * np.exp(-r * T) * ss.norm.cdf(d2(S0, K, r, sigma, T))
    else:
        if T==0:
            return np.maximum(K-S0,0)
        else:
            return K * np.exp(-r * T) * ss.norm.cdf(-d2(S0, K, r, sigma, T)) - S0 * ss.norm.cdf(-d1(S0, K, r, sigma, T))

def FuncPrice(T,S0,K,ModelParams):
    return Price(S0,K,ModelParams[0],ModelParams[1],T)

def Delta(S0,K,r,sigma,T):
    if T==0:
        if S0>K:
            return 1
        else:
            return 0
    else:
        return ss.norm.cdf(d1(S0,K,r,sigma,T))

def FuncDelta(T,S0,K,ModelParams):
    return Delta(S0,K,ModelParams[0],ModelParams[1],T)

def ReturnZC(T,r):
    return np.exp(r*T)

def FuncReturnZC(T,ModelParams):
    return ReturnZC(T,ModelParams[0])

def IVol(Mkt,S0,K,r,T,type="C",vol0=0.1):
    def f(vol,Mkt_,S0_,K_,r_,T_,type_): return (Price(S0_,K_,r_,vol,T_)-Mkt)**2
    return spo.minimize(f,vol0,args=(Mkt,S0,K,r,T,type),tol=1.0e-10).x

def IVolTCurve(vectP,vectK,S0,r,T):
    y=np.zeros(len(vectK)) 
    i=0
    for K in vectK:
        y[i] = IVol(vectP[i],S0,K,r,T)
        i = i+1
    pplot.plot(vectK,y)
    pplot.show()
