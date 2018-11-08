from Observer import Observer, Observable

class KPyObject(Observer,Observable):
    def __init__(self):
        self.calculated = False
        self.frozen = False
        self.alwaysForward = False
    
    def update(self):
        if (self.calculated or self.alwaysForward):
            self.calculated = False
            if not(self.frozen):
                self.notifyObservers()
                
    def performCalculations(self):
        pass
    
    def calculate(self):
        if not(self.calculated) and not(self.frozen):
           self.calculated = True
           try:
               self.performCalculations()
           except:
               self.calculated = False
               raise
    
    def recalculate(self):
        wasFrozen = self.frozen
        self.calculated, self.frozen = False
        try:
            self.calculate()
        except:
            self.frozen = wasFrozen
            self.notifyObservers()
    
    
    def freeze(self):
        self.frozen = True
    
    def unfreeze(self):
        if (self.frozen):
            self.frozen = False
            self.notifyObservers()
            
            
        
