class Instrument(object):
    def __init__(self):
        self._NPV = 0
        self._ErrorEstimate = 0
        self._ValuationDate = 0
        self._AdditionalResults = 0
        self._Engine = 0
        self._Calculated = False
        self._QLInstrument = 0
    
    def setPricingEngine(self,engine):
        self._Engine = engine
    
    def setupArguments(self,arguments):
        pass
    
    def fetchResults(self,results):
        self._NPV = results.Value
        self._ErrorEstimate = results.ErrorEstimate
        self._ValuationDate = results.ValuationDate
        self._AdditionalResults = results.AdditionalResults
    
    def _setupExpired(self):
        self._NPV, self._ErrorEstimate = 0
        self._ValuationDate = 0
        self._AdditionalResults.clear()
        self._IsCalculated = False
        
    def _calculate(self):
        if not(self._Calculated):
            self._performCalculations()
            self._Calculated = True
    
    def _performCalculations(self):
        self._Engine.reset()
        self.setupArguments(self._Engine.getArguments())
        if (self._Engine.getArguments().validate()):
            self._Engine.calculate()
            self.fetchResults(self._Engine.getResults())
    
    def NPV(self):
        self._calculate()
        return self._NPV
    
    def ErrorEstimate(self):
        self._calculate()
        return self._ErrorEstimate
    
    def ValuationDate(self):
        self._calculate()
        return self._ValuationDate
    
    def result(self,tag):
        self._calculate()
        return self._AdditionalResults.get(tag)
