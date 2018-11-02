from Observer import Observer, Observable

class PricingEngine(Observer,Observable):
    def __init__(self,arguments,results):
        Observable.__init__(self)
        self.arguments_ = arguments
        self.results_ = results
    
    def reset(self):
        return self.results_.reset()
    
    def update(self,observable):
        return self.notifyObservers(self)
    

class Arguments(object):
    def __init__(self):
        pass
    
    def validate(self):
        pass
    
class Results(object):
    def __init__(self):
        pass
    
    def reset(self):
        pass
    
    
    