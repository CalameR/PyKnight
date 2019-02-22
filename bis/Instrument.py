import Factory as Base
import Engine as Engine
import LazyObject as Laz

class Instrument(Base.Factory,Laz.LazyObject):
    def __init__(self,name,qlNPV=True,qlErrorEstimate=True):
        Base.Factory.__init__(self,name)
        Laz.LazyObject.__init__(self)
        self._NPV = None
        self._ErrorEstimate = None
        self._ValuationDate = None
        self._AdditionalResults = {}
        self._Engine = None
        self._IsQLNPV = qlNPV
        self._IsQLErrorEstimate = qlErrorEstimate
    
    def setPricingEngine(self,engine):
        self._Engine = engine    
        if (self._QLNPV or self._QLErrorEstimate):
            self._QLFactory.setPricingEngine(engine())
    
    def setupArguments(self,arguments):
        pass
    
    def fetchResults(self,results):
        self._NPV = results.Value
        self._ErrorEstimate = results.ErrorEstimate
        self._ValuationDate = results.ValuationDate
        self._AdditionalResults = results.AdditionalResults
    
    def _QLNPV(self):
        self._NPV = self._QLFactory.NPV()
        
    def _QLErrorEstimate(self):
        self._ErrorEstimate = self._QLFactory.errorEstimate()
    
    def _setupExpired(self):
        self._NPV, self._ErrorEstimate = None
        self._ValuationDate = None
        self._AdditionalResults.clear()
        self._IsCalculated = False    
    
    def _calculate(self):
        if not(self._Calculated):
            self._performCalculations()
            self._Calculated = True
    
    def _performCalculations(self):
        if (self._QLComputation):
            self._QLComputations()
        else:
            self._Engine.reset()
            self.setupArguments(self._Engine.getArguments())
            if (self._Engine.getArguments().validate()):
                self._Engine.calculate()
                self.fetchResults(self._Engine.getResults())
    
    def NPV(self):
        if (self._QLNPV):
            return self._QLFactory.NPV()
        else:
            self._calculate()
            return self._NPV
    
    def ErrorEstimate(self):
        if (self._QLFactory):
            return self._QLFactory.errorEstimate()
        else:
            self._calculate()
            return self._ErrorEstimate
    
    
    def ValuationDate(self):
        self._calculate()
        return self._ValuationDate
    
    def result(self,tag):
        self._calculate()
        return self._AdditionalResults.get(tag)

class Results(Engine.Results):
    def __init__(self):
        self.Value = None
        self.ErrorEstimate = None
        self.ValuationDate = None
        self.AdditionalResults = {}
    
    def reset(self):
        self.Value, self.ErrorEstimate = None
        self.ValuationDate = None
        self.AdditionalResults.clear()
    
    