import KPyObject
import PricingEngine

class Instrument(KPyObject.KPyObject):
    def __init__(self):
        self.NPV = 0
        self.errorEstimate = 0
        self.valuationDate = 0
        self.additionalResults = 0
        self.engine = 0
    
    def setPricingEngine(self,engine):
        if self.engine != 0:
            self.deleteObserver(self.engine)
        self.engine = engine
        if (self.engine != 0):
            self.addObserver(self.engine)
        self.update()
    
    def setupArguments(self,arguments):
        pass
    
    def isExpired(self):
        pass
    
    def setupExpired(self):
        self.value, self.errorEstimate = 0
        self.valuationDate = 0
        self.additionalResults.clear()
        
    def calculate(self):
        if self.isExpired():
            self.setupExpired()
            self.calculated = True
        else:
            KPyObject.KPyObject.calculate()
    
    def fetchResults(self,results):
        #CHECK NOT DONE ON RESULTS
        #if (results != Null):
        self.NPV = results.value
        self.errorEstimate = results.errorEstimate
        self.valuationDate = results.valuationDate
        self.additionalResults = results.additionalResults
    
    def performCalculations(self):
        self.engine.reset()
        self.setupArguments(self.engine.arguments)
        self.engine.arguments.validate()
        self.engine.calculate()
        self.fetchResults(self.engine.results)
    
    
    def fNPV(self):
        self.calculate()
        #CHECK NOT DONE ON NPV
        #if (NPV != Null<Real>):
        return self.NPV
    
    def fErrorEstimate(self):
        self.calculate()
        #CHECK NOT DONE ON errorEstimate
        #if (errorEstimate != Null<Real>):
        return self.errorEstimate
    
    def fValuationDate(self):
        self.calculate()
        #CHECK NOT DONE ON ValuationDate
        #if (ValuationDate != Null<Date>):
        return self.valuationDate
    
    def result(self,tag):
        #CHECK on additionalResults structure NOT DONE
        return self.additionalResults.get(tag)
            
class Results(PricingEngine.Results):
    def __init__(self):
        self.value = 0
        self.errorEstimate = 0
        self.valuationDate = 0
        self.additionalResults = 0
    
    def reset(self):
        self.value, self.errorEstimate = 0
        self.valuationDate = 0
        self.additionalResults.clear()
    
        
        
    
