from Model import Model as Mod
from Securities import Securities as Secu
from NumericalMethod import NumericalMethod as NumMeth
import numpy as np
import scipy.stats as ss 
import scipy.optimize as spo
import matplotlib.pyplot as pplot
#import math as math
import Utils as use

class BlackScholes(Mod):
    
    def d1(S0, K, r, sigma, T):
        m = S0/(K*np.exp(-r*T))
        return np.log(m) * (1/(sigma*np.sqrt(T))) + sigma * np.sqrt(T) / 2

    def d2(S0, K, r, sigma, T):
        return BlackScholes.d1(S0,K,r,sigma,T) - sigma * np.sqrt(T)
    
    def CallPrice(S0, K, r, sigma, T):
        if T==0:
            return np.maximum(S0 - K,0)
        else:
            return S0 * ss.norm.cdf(BlackScholes.d1(S0, K, r, sigma, T)) - K * np.exp(-r * T) * ss.norm.cdf(BlackScholes.d2(S0, K, r, sigma, T))
        
    def PutPrice(S0, K, r, sigma, T):
        if T==0:
            return np.maximum(K-S0,0)
        else:
            return K * np.exp(-r * T) * ss.norm.cdf(-BlackScholes.d2(S0, K, r, sigma, T)) - S0 * ss.norm.cdf(-BlackScholes.d1(S0, K, r, sigma, T))
    
    
    def DeltaCall(S0,K,r,sigma,T):
        if T==0:
            if S0>K:
                return 1
            else:
                return 0
        else:
            return ss.norm.cdf(BlackScholes.d1(S0,K,r,sigma,T))
    
    def DeltaPut(S0,K,r,sigma,T):
        return 1-BlackScholes.DeltaCall(S0,K,r,sigma,T)
    
    def IVol(Mkt,S0,K,r,T,Type="C",vol0=0.1):
        def f(vol,Mkt_,S0_,K_,r_,T_,type_): 
            if Type=="C":
                return (BlackScholes.CallPrice(S0_,K_,r_,vol,T_)-Mkt)**2 
            else:
                return (BlackScholes.PutPrice(S0_,K_,r_,vol,T_)-Mkt)**2 
        return spo.minimize(f,vol0,args=(Mkt,S0,K,r,T,Type),tol=1.0e-10).x

    def IVolTCurve(vectP,vectK,S0,r,T,vectType):
        y=np.zeros(len(vectK)) 
        i=0
        for K in vectK:
            y[i] = BlackScholes.IVol(vectP[i],S0,K,r,T,vectType[i])
            i = i+1
        pplot.plot(vectK,y)
        pplot.show()
    
    def __init__(self,ModelName,ModelParams=(0.01,0.1)):
        Mod.__init__(self,"{0}_{1}".format("BlackScholes",ModelName),ModelParams)
    
    def GetParamPos(self,ParamName):
        if (ParamName == "r" or "R" or "rate" or "RATE" or "taux" or "TAUX"):
            return 0
        elif (ParamName == "vol" or "VOL" or "volatility" or "VOLATILITY" or "sigma" or "SIGMA"):
            return 1

    def TestParams(self,ModelParams):
        return Mod.MsgParams(ModelParams[self.GetParamPos("r")]>0 and ModelParams[self.GetParamPos("sigma")]>0)

    def SimulatePath(self,S0,T,nbstep=1):
        G=np.random.randn(nbstep)
        S=np.zeros(nbstep+1)
        dt=T/nbstep
        S[0]=S0
        r=self.ModelParams[self.GetParamPos("r")]
        sigma=self.ModelParams[self.GetParamPos("sigma")]
        for i in range(1,nbstep+1):
            S[i]=S[i-1]*np.exp((r-sigma**2/2)*dt+sigma*np.sqrt(dt)*G[i-1])
        return S
    
    def Price(self,S0,T,MySecurities,MyNumericalMethod=()):
        Mod.Price(self,S0,T,MySecurities,MyNumericalMethod)
        if !isinstance(MyNumericalMethod,NumMeth):
            #TO BE COMPLETED
            #return

    def FuncPrice(T,S0,K,ModelParams):
        return Price(S0,K,ModelParams[0],ModelParams[1],T)

    def FuncDelta(T,S0,K,ModelParams):
        return Delta(S0,K,ModelParams[0],ModelParams[1],T)

    def ReturnZC(T,r):
        return np.exp(r*T)

    def FuncReturnZC(T,ModelParams):
        return ReturnZC(T,ModelParams[0])

    


