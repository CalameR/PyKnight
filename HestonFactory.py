import Factory as Base
import ProcessFactory as Process
import PathFactory as Path
import QuantLib as ql

class HestonProcessFactory(Process.ProcessFactory):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho):
        params={'r':r,'q':q,'s0':s0,'v0':v0,'kappa':kappa,'theta':theta,'sigma':sigma,'rho':rho}
        Process.ProcessFactory.__init__(self,"Heston_Process",params,2,1)
        
    def Make(self,**data):
        DayCount = data.get('DayCount')
        AsOfDate = data.get('AsOfDate')
        rate_curve_handle = ql.YieldTermStructureHandle(
                ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(self._params.get('r'))),DayCount))
        div_curve_handle = ql.YieldTermStructureHandle(
                ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(self._params.get('q'))),DayCount))
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self._params.get('s0')))
        return ql.HestonProcess(rate_curve_handle,div_curve_handle,spot_handle,
                                self._params.get('v0'),self._params.get('kappa'),self._params.get('theta'),
                                self._params.get('sigma'),self._params.get('rho'))
    
    def GetFactorName(self,pos):
        if pos==0:
            return 's'
        elif pos==1:
            return 'v'
        
    ###################################################################################
    ## NO RECALIBRATION: DO A CHILD CLASS IF YOU WANT TO DO ANOTHER UPDATE 
    ###################################################################################
    def UpdateParams(self,**data):
        self._params['s0']=data.get('s',self._params.get('s0'))
        self._params['v0']=data.get('v',self._params.get('v0'))
        
class HestonModelFactory(Base.Factory):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho):
        Base.Factory.__init__(self,"Heston_Model")
        self._HestonProcess = HestonProcessFactory(r,q,s0,v0,kappa,theta,sigma,rho)
        
    
    def GetParams(self):
        return self._HestonProcess.GetParams()
    
    def GetParamNames(self):
        return self._HestonProcess.GetParamNames()
    
    def SetParams(self,**params):
        self._HestonProcess.SetParams(**params)
    
    def Make(self,**data):
        return ql.HestonModel(self._HestonProcess.Make(**data))
    
    def UpdateParams(self,**data):
        self._HestonProcess.UpdateParams(**data)    

class HestonAnalyticEngineFactory(Base.Factory):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho,relTolerance=0.01,maxEval=1000):
        params = {'relTolerance':relTolerance,'maxEval':maxEval}
        Base.Factory.__init__(self,"Heston_AnalyticEngine",params)
        self._HestonModel = HestonModelFactory(r,q,s0,v0,kappa,theta,sigma,rho)
        
    def GetParams(self):
        params = dict(list(self._HestonModel.GetParams().items()) + 
                      list(Base.Factory.GetParams(self).items()))
        return params
    
    def GetParamNames(self):
        names = self._HestonModel.GetParamNames()
        names.extend(Base.Factory.GetParamNames(self))
        return names
    
    def SetParams(self,**params):
        self._HestonModel.SetParams(**params)
        Base.Factory.SetParams(self,**params)
        
    def Make(self,**data):
        return ql.AnalyticHestonEngine(self._HestonModel.Make(**data),self._params.get('relTolerance'),self._params.get('maxEval'))
    
    def UpdateParams(self,**data):
        self._HestonModel.UpdateParams(**data)
        Base.Factory.SetParams(self,**data)
        
class HestonPathGenerator(Path.GaussianMultiPathGeneratorFactory):
    def __init__(self,r,q,s0,v0,kappa,theta,sigma,rho,timeGrid,brownianBridge=False):
        HestonProcess = HestonProcessFactory(r,q,s0,v0,kappa,theta,sigma,rho)
        Path.GaussianMultiPathGeneratorFactory.__init__(self,"HestonPathGenerator",HestonProcess,timeGrid,brownianBridge)
        
    
