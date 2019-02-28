# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 13:37:06 2019

@author: RCalame
"""

import QuantLib as ql
import numpy as np
import scipy.stats as stats
import scipy.optimize as spo
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from random import sample
import sklearn.neural_network as sknn
import matplotlib.pyplot as plt
import time
from scipy.integrate import *
import cmath as cpx
import math as m

def d1(S0, K, r, sigma, T):
    m = S0/(K*np.exp(-r*T))
    return np.log(m)*(1/(sigma*np.sqrt(T)))+sigma*np.sqrt(T)/2

def d2(S0, K, r, sigma, T):
    return d1(S0,K,r,sigma,T)-sigma*np.sqrt(T)
 
def BS_CallPrice(S0,K,r,sigma,T):
    if T==0:
        return np.maximum(S0-K,0)
    else:
        return S0*stats.norm.cdf(d1(S0,K,r,sigma,T))-K*np.exp(-r*T)*stats.norm.cdf(d2(S0,K,r,sigma,T))

def Heston_CharacteristicFunctionLogPrice(t,omega,S0,v0,r,kappa,theta,ksi,rho):
    alpha = complex(-omega**2 / 2, -omega / 2)
    beta = complex(kappa,-rho*ksi*omega)
    gamma = ksi**2 / 2
    h = (beta**2-4*alpha*gamma)**0.5
    r_m = (beta-h) / ksi**2
    r_p = (beta+h) / ksi**2
    g = r_m / r_p
    C = kappa*(r_m*t-2*cpx.log((1-g*cpx.exp(-h*t))/(1-g))/ksi**2)
    D = r_m*((1-cpx.exp(-h*t))/(1-g*cpx.exp(-h*t)))
    return cpx.exp(complex(C*theta+D*v0,omega*np.log(S0*np.exp(r*t))))

def RPI1_HestonChFuncLnS(omega,K,t,S0,v0,r,kappa,theta,ksi,rho):
    num = Heston_CharacteristicFunctionLogPrice(t,omega-complex(0,1),S0,v0,r,kappa,theta,ksi,rho)*cpx.exp(complex(0,-omega*np.log(K)))
    denom = complex(0,omega*Heston_CharacteristicFunctionLogPrice(t,-complex(0,1),S0,v0,r,kappa,theta,ksi,rho))
    return (num / denom).real
def RPI2_HestonChFuncLnS(omega,K,t,S0,v0,r,kappa,theta,ksi,rho):
    num = Heston_CharacteristicFunctionLogPrice(t,omega,S0,v0,r,kappa,theta,ksi,rho)*cpx.exp(complex(0,-omega*np.log(K)))
    denom = complex(0,omega)
    return (num / denom).real
def Heston_CallPrice(K,S0,r,T,v0,kappa,theta,ksi,rho):
    Pi_1 = 1/2+1/np.pi*quad(RPI1_HestonChFuncLnS,0,np.inf,args=(K,T,S0,v0,r,kappa,theta,ksi,rho))[0]
    Pi_2 = 1/2+1/np.pi*quad(RPI2_HestonChFuncLnS,0,np.inf,args=(K,T,S0,v0,r,kappa,theta,ksi,rho))[0]
    return S0*Pi_1-K*np.exp(-r*T)*Pi_2

def IVol(Mkt,S0,K,r,T,vol0=0.1):
    def f(vol,Mkt_,S0_,K_,r_,T_,type_): return (BS_CallPrice(S0_,K_,r_,vol,T_)-Mkt)**2
    return spo.minimize(f,vol0,args=(Mkt,S0,K,r,T,type),tol=1.0e-10).x

print(IVol(5,100,100,0.01,0.1,1))

t = 1
omega = 1
S0 = 100
v0 = 0.1
r = 0.02
kappa = 1
theta = 0.2
ksi = 0.3
rho = -0.6
print(Heston_CharacteristicFunctionLogPrice(t,omega,S0,v0,r,kappa,theta,ksi,rho))

T = 1/4
S0 = 100
v0 = 0.02901993
r = 0.01
kappa = 0.78408106
theta = 0.06899448
xi = 0.30726073
rho = -0.96377951
K = 84.93848231191514
Price = Heston_CallPrice(K,S0,r,T,v0,kappa,theta,xi,rho)
print(Price)

def MakeUniformRandParams(ArrayMin,ArrayMax,nRand):
    if (len(ArrayMin)!=len(ArrayMax)):
        raise Exception('ArrayMax and ArrayMin must have the same size')
    else:
        nParams = len(ArrayMin)
        rand_seq = ql.UniformRandomSequenceGenerator(nParams*nRand,ql.UniformRandomGenerator())
        X = rand_seq.nextSequence().value()
        #X = [ArrayMin[j%nParams]+(ArrayMax[j%nParams]-ArrayMin[j%nParams])*X[j] for j in range(nParams*nRand)]
        res = np.zeros((nRand,nParams))
        LocalMax = 0
        res__ = 0
        res_ = 0
        for i in range(nRand):
            for j in range(nParams):
                AdjMax = ArrayMax[j]
                if j==2:
                    AdjMax = XiFellerAdjust(res__,res_,ArrayMax[j])
                res[i,j]=ArrayMin[j]+(AdjMax-ArrayMin[j])*X[i*nParams+j]
                res__ = res_
                res_ = res[i,j]
        #res = np.reshape(X,(nRand,nParams))
        return res

def CountNoFellerCondition(X):
    k=0
    for j in range(len(X)):
        if (X[j,2]>XiFellerMax(X[j,0],X[j,1])):
            k=k+1
    return k

def XiFellerMax(kappa,theta):
    return m.sqrt(2*kappa*theta)

def XiFellerAdjust(kappa,theta,xi_init):
    if (xi_init>XiFellerMax(kappa,theta)):
        return XiFellerMax(kappa,theta)
    return xi_init
    
ArrayMin = [0.1, 0.1,  0.01, -0.999, 0.1]
ArrayMax = [1.5, 1.5,  0.75,  0.999, 1.5]
nRand = 100000
start = time.time()
res=MakeUniformRandParams(ArrayMin,ArrayMax,nRand)
end = time.time()
print('Total computation time = ' + str(round(end-start,2)) + 's')
print('No Feller Condition ' + str(CountNoFellerCondition(res)))

# GLOBAL CONFIG #
AsOfDate = ql.Date(15,10,2018)
ql.Settings.instance().evaluationDate = AsOfDate
DayCount = ql.Actual365Fixed()
Calendar = ql.UnitedStates()


# EUROPEAN OPTION CONFIG #
MaturityDates = []
strikes = []
exercises = []
payoffs = []
option_type = ql.Option.Call
for k in range(8):
    MaturityDates.append(ql.Date(15,10,2018+k+1))
    exercises.append(ql.EuropeanExercise(MaturityDates[k]))
for k in range(11):
    strikes.append(50+k*10)
    payoffs.append(ql.PlainVanillaPayoff(option_type, strikes[k]))
print(MaturityDates)
print(strikes)
EuropeanOptions = []
for T in range(len(MaturityDates)):
    for K in range(len(strikes)):
        EuropeanOptions.append(ql.VanillaOption(payoffs[K], exercises[T]))
#print(EuropeanOptions)
        
# MARKET DATA
r=ql.SimpleQuote(0.01)
r_ts = ql.FlatForward(0,Calendar,ql.QuoteHandle(r),DayCount)
q=ql.SimpleQuote(0.0)
q_ts = ql.FlatForward(0,Calendar,ql.QuoteHandle(q),DayCount)
s0=ql.SimpleQuote(100)

# BLACK SCHOLES ENGINE ONLY USED FOR COMPUTING IMPLIED VOLATILITIES
vol_bs = ql.SimpleQuote(0.10)
vol_bs_ts = ql.BlackConstantVol(0,Calendar,ql.QuoteHandle(vol_bs),DayCount)
BSProcess = ql.BlackScholesMertonProcess(ql.QuoteHandle(s0),ql.YieldTermStructureHandle(r_ts),ql.YieldTermStructureHandle(q_ts),
                               ql.BlackVolTermStructureHandle(vol_bs_ts))

# HESTON ENGINE
v0 = 0.01
kappa=0.5
theta=0.01
sigma=0.0001
rho=-0.5
HestonParams = [theta,kappa,sigma,rho,v0]
relTolerance=0.01
maxEval=1000
HestonProcess = ql.HestonProcess(ql.YieldTermStructureHandle(r_ts),ql.YieldTermStructureHandle(q_ts),
                                 ql.QuoteHandle(s0),v0,kappa,theta,sigma,rho)
HestonModel = ql.HestonModel(HestonProcess)
HestonEngine = ql.AnalyticHestonEngine(HestonModel,relTolerance,maxEval)
for i in range(len(EuropeanOptions)):
    EuropeanOptions[i].setPricingEngine(HestonEngine)

# GENERATE DATAS
nRand = 1000
start = time.time()
MinParamsValues = [0.1, 0.01,  0.01, -0.999, 0.01]
MaxParamsValues = [1.0, 0.50,  0.50,  -0.1, 0.50]
local_start = 0
local_end = 0
ArrParams = MakeUniformRandParams(MinParamsValues,MaxParamsValues,nRand)
intermediary = time.time()

#npv = np.zeros(nRand)
#iv = np.zeros(nRand)
#for i in range(nRand):
#    HestonModel.setParams([ArrParams[i][k] for k in range(len(MinParamsValues))])
#    npv[i] = EuropeanOption.NPV()
#    iv[i] = EuropeanOption.impliedVolatility(npv[i],BSProcess,1.0e-4,200,1.0e-8,10)
#end = time.time()
#print('Random params simulation time = ' + str(round(intermediary-start,2)) + 's')
#print('Prices computation time = ' + str(round(end-intermediary,2)) + 's')
#print('Total computation time = ' + str(round(end-start,2)) + 's')

npv = np.zeros(nRand*len(EuropeanOptions))
iv = np.zeros(nRand*len(EuropeanOptions))
for i in range(nRand):
    HestonModel.setParams([ArrParams[i,k] for k in range(len(MinParamsValues))])
    for j in range(len(EuropeanOptions)):
        npv[i*len(EuropeanOptions)+j] = EuropeanOptions[j].NPV()
        #print(EuropeanOptions[j].NPV())
        #print(npv[i*len(EuropeanOptions)+j])
        #print('K = ' + str(strikes[j%len(strikes)]))
        #print('T = ' + str(MaturityDates[int(j/len(strikes))]))
        iv[i*len(EuropeanOptions)+j] = EuropeanOptions[j].impliedVolatility(npv[i*len(EuropeanOptions)+j],BSProcess,1.0e-4,200,1.0e-8,100)
end = time.time()
print('Random params simulation time = ' + str(round(intermediary-start,2)) + 's')
print('Prices computation time = ' + str(round(end-intermediary,2)) + 's')
print('Total computation time = ' + str(round(end-start,2)) + 's')

EO = ql.VanillaOption(ql.PlainVanillaPayoff(option_type, 100), ql.EuropeanExercise(ql.Date(15,10,2019)))