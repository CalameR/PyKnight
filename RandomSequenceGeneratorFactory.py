import Factory as Base
import QuantLib as ql

class UniformRandomSequenceGeneratorFactory(Base.Factory):
    def __init__(self,dimension):
        params={'dimension':dimension}
        Base.Factory.__init__(self,"UniformRandomSequenceGenerator",params)
    
    def Make(self,**data):
        return ql.UniformRandomSequenceGenerator(self._params.get('dimension'),ql.UniformRandomGenerator())
        
    def UpdateParams(self,**data):
        Base.Factory.SetParams(self,**data)

class GaussianRandomSequenceGeneratorFactory(Base.Factory):
    def __init__(self,dimension):
        Base.Factory.__init__(self,"GaussianRandomSequenceGenerator")
        self._UniformRandomSequenceGenerator = UniformRandomSequenceGeneratorFactory(dimension)
    
    def GetParams(self):
        return self._UniformRandomSequenceGenerator.GetParams()
    
    def GetParamNames(self):
        return self._UniformRandomSequenceGenerator.GetParamNames()
    
    def SetParams(self,**params):
        self._UniformRandomSequenceGenerator.SetParams(**params)
    
    def Make(self,**data):
        return ql.GaussianRandomSequenceGenerator(self._UniformRandomSequenceGenerator.Make(**data))
    
    def UpdateParams(self,**data):
        self._UniformRandomSequenceGenerator.UpdateParams(**data) 