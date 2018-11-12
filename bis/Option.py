import Instrument as Base

class Option(Base.Instrument):
    def __init__(self,payoff,exercise):
        Base.Instrument.__init__(self)
        self._Payoff = payoff
        self._Exercise = exercise
        
    def Payoff(self):
        return self._Payoff
    
    def Exercise(self):
        return self._Exercise
    

        
    

