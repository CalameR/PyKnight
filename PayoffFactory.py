import QuantLib as ql
import Factory as Base

class PayoffFactory(Base.Factory):
    def __init__(self,name,params):
        Base.Factory.__init__(self,name,params)
    
    # IN THEORY NO "CALIBRATION" FOR PAYOFF --> UPDATING PARAMS := SETTING PARAMS #
    def UpdateParams(self,**data):
        self.SetParams(**data)

class TypePayoffFactory(PayoffFactory):
    def __init__(self,name,params,OptionType=ql.Option.Call):
        Base.Factory.__init__(self,name,params)
        self._OptionType = OptionType
    
    def GetParams(self):
        return dict(list(self._params.items())+[('OptionType',self._OptionType)])
    
    def GetParamNames(self):
        names = list(self._params.keys())
        names.append('OptionType')
        return names
    
    def SetParams(self,**params):
        for (key,val) in self._params.items():
            self._params[key] = params.get(key,val)
    
    def SetOptionType(self,OptionType):
        self._OptionType = OptionType
    
class FloatingTypePayoffFactory(TypePayoffFactory):
    def __init__(self,name,params,OptionType=ql.Option.Call):
        Base.Factory.__init__(self,name,params)
        self._OptionType = OptionType