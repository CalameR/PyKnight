from KPyObject import KPyObject as KPy
from PricingEngine import PricingEngine as GenEngine

class Instrument(KPyObject):
    def __init__(self):
        self.fNPV_ = 0
        self.fErrEstim = 0
        self.fEvalDate = 0
        
