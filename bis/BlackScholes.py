import Factory as Base
import Process as SDE
import Path as Gen
import QuantLib as ql

class BlackScholesProcess(SDE.Process):
    def __init__(self,r,q,s0,sigma):
        SDE.Process.__init__(self,'BlackScholes_Process',1,1)
        self._R = r
        self._Q = q
        self._S0 = s0
        self._Sigma = sigma
        
    def _QLBuild(self):
        AsOfDate = self._Context.AsOfDate
        DayCount = self._Context.DayCount        
        Calendar = self._Context.Calendar
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self._S0))
        rate_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate, self._R, DayCount))
        div_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate, self._Q, DayCount))
        vol_curve_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(AsOfDate, Calendar, self._Sigma, DayCount))
        self._QLFactory = ql.BlackScholesMertonProcess(spot_handle,rate_curve_handle,div_curve_handle,vol_curve_handle)

    ###################################################################################
    ## NO RECALIBRATION OF SIGMA: DO A CHILD CLASS IF YOU WANT TO DO ANOTHER UPDATE 
    ###################################################################################
    def _UpdateParams(self,data):
        self._S0 = data[0]
        
class BlackScholesPathGenerator(Gen.GaussianPathGenerator):
    def __init__(self,r,q,s0,sigma,length,timestep,brownianBridge=False):
        blackScholesProcess = BlackScholesProcess(r,q,s0,sigma)
        Gen.GaussianPathGenerator.__init__(self,"BlackScholes_PathGenerator",blackScholesProcess,length,timestep,brownianBridge)


###############################################################
        #NOT DONE
class BlackScholesAnalyticEngineFactory(Base.Factory):
    def __init__(self,r,q,s0,sigma):
        Base.Factory.__init__(self,"BlackScholes_AnalyticEngine")
        self._BlackScholesProcess = BlackScholesProcessFactory(r,q,s0,sigma)
        
    def GetParams(self):
        return self._BlackScholesProcess.GetParams()
    
    def GetParamNames(self):
        return self._BlackScholesProcess.GetParamsNames()
    
    def SetParams(self,**params):
        self._BlackScholesProcess.SetParams(**params)
        
    def _QLBuild(self,**data):
        self._QLFactory = ql.AnalyticEuropeanEngine(self._BlackScholesProcess())
    
    def Update(self,**data):
        self._BlackScholesProcess.Update(**data)
        Base.Factory.Update(self,**data)
    
    def _UpdateParams(self,**data):
        return 0
    
    def _UpdateData(self,**data):
        return 0
        


