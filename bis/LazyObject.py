from Observer import Observer, Observable

class LazyObject(Observer,Observable):
    def __init__(self):
        self._Calculated = False
        self._Frozen = False
        self._AlwaysForward = False
    
    def update(self):
        if (self._Calculated or self._AlwaysForward):
            self._Calculated = False
            if not(self._Frozen):
                self.notifyObservers()
                
    def _performCalculations(self):
        pass
    
    def _calculate(self):
        if not(self._Calculated) and not(self._Frozen):
           self._Calculated = True
           try:
               self._performCalculations()
           except:
               self._Calculated = False
               raise
    
    #def recalculate(self):
        #wasFrozen = self._Frozen
        #self._Calculated, self._Frozen = False
        #try:
            #self._Calculate()
        #except:
            #self._Frozen = wasFrozen
            #self.notifyObservers()
    
    
    def freeze(self):
        self._Frozen = True
    
    def unfreeze(self):
        if (self._Frozen):
            self._Frozen = False
            self.notifyObservers()
            
            
        
