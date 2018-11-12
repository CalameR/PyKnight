import Factory as Base
import ProcessFactory as Process
import PathFactory as Path
import QuantLib as ql

class BlackScholesProcessFactory(Process.ProcessFactory):
    def __init__(self,r,q,s0,sigma):
        params={'r':r,'q':q,'s0':s0,'sigma':sigma}
        Process.ProcessFactory.__init__(self,"Heston_Process",params,1,1)
        self._data = {'DayCount':0,'AsOfDate':0,'Calendar':0}
        
    def _QLBuild(self):
        DayCount = self._data.get('DayCount')
        AsOfDate = self._data.get('AsOfDate')
        Calendar = self._data.get('Calendar')
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self._params.get('s0')))
        rate_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate, self._params.get('r'), DayCount))
        div_curve_handle = ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate, self._params.get('q'), DayCount))
        vol_curve_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(AsOfDate, Calendar, self._params.get('sigma'), DayCount))
        self._QLFactory = ql.BlackScholesMertonProcess(spot_handle,rate_curve_handle,div_curve_handle,vol_curve_handle)
    
    def GetFactorName(self,pos):
        if pos==0:
            return 's'
    
    def _UpdateData(self,**data):
        self._data['DayCount']=data.get('DayCount',self._data.get('DayCount'))
        self._data['AsOfDate']=data.get('AsOfDate',self._data.get('AsOfDate'))
        self._data['Calendar']=data.get('Calendar',self._data.get('Calendar'))

    ###################################################################################
    ## NO RECALIBRATION OF SIGMA: DO A CHILD CLASS IF YOU WANT TO DO ANOTHER UPDATE 
    ###################################################################################
    def _UpdateParams(self,**data):
        self._params['s0']=data.get('s',self._params.get('s0'))
        
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
        
class BlackScholesPathGenerator(Path.GaussianPathGeneratorFactory):
    def __init__(self,r,q,s0,sigma,length,timestep,brownianBridge=False):
        BlackScholesProcess = BlackScholesProcessFactory(r,q,s0,sigma)
        Path.GaussianPathGeneratorFactory.__init__(self,"BlackScholes_PathGenerator",BlackScholesProcess,length,timestep,brownianBridge)


