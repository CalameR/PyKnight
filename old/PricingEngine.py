import Observer

class PricingEngine(Observer.Observer,Observer.Observable):
    def __init__(self,arguments,results):
        Observer.Observable.__init__(self)
        self.arguments = arguments
        self.results = results
    
    def reset(self):
        return self.results.reset()
    
    def update(self):
        return self.notifyObservers()

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
    
    
    