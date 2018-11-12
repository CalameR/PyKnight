import Factory as Base
import QuantLib as ql

class UniformRandomSequenceGeneratorFactory(Base.Factory):
    def __init__(self,dimension):
        params={'dimension':dimension}
        Base.Factory.__init__(self,"UniformRandomSequenceGenerator",params)
    
    def _QLBuild(self):
        self._QLFactory = ql.UniformRandomSequenceGenerator(self._params.get('dimension'),ql.UniformRandomGenerator())
        
    def _UpdateParams(self,**data):
        Base.Factory._SetParams(self,**data)
    
    def _UpdateData(self,**data):
        return 0

class GaussianRandomSequenceGeneratorFactory(Base.Factory):
    def __init__(self,dimension):
        Base.Factory.__init__(self,"GaussianRandomSequenceGenerator")
        self._UniformRandomSequenceGenerator = UniformRandomSequenceGeneratorFactory(dimension)
    
    def GetParams(self):
        return self._UniformRandomSequenceGenerator.GetParams()
    
    def GetParamNames(self):
        return self._UniformRandomSequenceGenerator.GetParamNames()
    
    def _QLBuild(self):
        self._QLFactory = ql.GaussianRandomSequenceGenerator(self._UniformRandomSequenceGenerator())
    
    def _UpdateParams(self,**data):
        return 0
    
    def _UpdateData(self,**data):
        return 0
    
    def Update(self,**data):
        self._UniformRandomSequenceGenerator.Update(**data)
        Base.Factory.Update(self,**data)