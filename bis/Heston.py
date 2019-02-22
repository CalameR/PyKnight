import Factory as Base
import Process as SDE
import Path as Gen
import QuantLib as ql
import Engine as Eng
import VanillaOption as Van

class HestonProcess(SDE.Process):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho):
        SDE.Process.__init__(self,'Heston_Process',2,1)
        self._R = r
        self._Q = q
        self._S0 = s0
        self._V0 = v0
        self._Kappa = kappa
        self._Theta = theta
        self._Sigma = sigma
        self._Rho = rho
        
    def _QLBuild(self):
        DayCount = self._Context.DayCount
        AsOfDate = self._Context.AsOfDate
        rate_curve_handle = ql.YieldTermStructureHandle(
                ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(self._R)),DayCount))
        div_curve_handle = ql.YieldTermStructureHandle(
                ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(self._Q)),DayCount))
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self._S0))
        self._QLFactory = ql.HestonProcess(rate_curve_handle,div_curve_handle,spot_handle,
                                self._V0,self._Kappa,self._Theta,
                                self._Sigma,self._Rho)

    
    ###################################################################################
    ## NO RECALIBRATION: DO A CHILD CLASS IF YOU WANT TO DO ANOTHER UPDATE 
    ###################################################################################
    def _UpdateParams(self,data):
        self._S0 = data[0]
        self._V0 = data[1]

class HestonPathGenerator(Gen.GaussianMultiPathGenerator):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho,timeGrid,brownianBridge=False):
        hestonProcess = HestonProcess(r,q,s0,v0,kappa,theta,sigma,rho)
        Gen.GaussianMultiPathGenerator.__init__(self,"HestonPathGenerator",hestonProcess,timeGrid,brownianBridge)
    
class HestonModel(Base.CalibFactory):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho):
        Base.Factory.__init__(self,"Heston_Model")
        self._HestonProcess = HestonProcess(r,q,s0,v0,kappa,theta,sigma,rho)
    
    def _QLBuild(self):
        self._QLFactory = ql.HestonModel(self._HestonProcess())
    
    def Update(self,data):
        self._HestonProcess.Update(data)
        Base.CalibFactory.Update(self,data)
        
    def _UpdateParams(self,data):
        return 0
    
    def SetContext(self,context):
        self._HestonProcess.SetContext(context)
    
class HestonAnalyticEngine(Eng.Engine):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho,relTolerance=0.01,maxEval=1000):
        Eng.Engine.__init__(self,'Heston_AnalyticEngine')
        self._HestonModel = HestonModel(r,q,s0,v0,kappa,theta,sigma,rho)
        self._RelTolerance = relTolerance
        self._MaxEval = maxEval
        self._Arguments = Van.Opt1D.Opt.Arguments()
        self._Results = Van.Opt1D.Results()
        
    def _QLBuild(self):
        self._QLFactory = ql.AnalyticHestonEngine(self._HestonModel(),self._RelTolerance,self._MaxEval)
    
    def Update(self,data):
        self._HestonModel.Update(data)
        Eng.Engine.Update(self,data)
    
    def _UpdateParams(self,**data):
        return 0
        
    def SetContext(self,context):
        self._HestonModel.SetContext(context)
    
    def calculate(self):
        self._QLFactory
    
    