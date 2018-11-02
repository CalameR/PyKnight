from Observer import Observer, Observable

class KPyObject(Observer,Observable):
    def __init__(self):
        self.calculated_ = False
        self.frozen_ = False
        self.alwaysForward_ = False
    
    def update(self,observable):
        if (self.calculated_ or self.alwaysForward_):
            self.calculated_ = False
            if not(self.frozen_):
                self.notifyObservers(self)
                
    def performCalculations(self):
        pass
    
    def calculate(self):
        if not(self.calculated_) and not(self.frozen_):
           self.calculated_ = True
           try:
               self.performCalculations()
           except:
               self.calculated_ = False
               raise
    
    def recalculate(self):
        wasFrozen = self.frozen_
        self.calculated_, self.frozen_ = False
        try:
            self.calculate()
        except:
            self.frozen_ = wasFrozen
            self.notifyObservers(self)
    
    
    def freeze(self):
        self.frozen_ = True
    
    def unfreeze(self):
        if (self.frozen_):
            self.frozen_ = False
            self.notifyObservers(self)
            
            
        
