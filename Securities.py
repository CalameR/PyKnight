import numpy as np

class Securities(object):
    def __init__(self,SecuritiesName,SecuritiesParams=()):
        self.Name = SecuritiesName
        self.Params = SecuritiesParams
        
    def __str__(self):
        return "{0} with params {1}".format(self.Name,self.Params)
    
    def payoff(self,data=()):
        print("{0} payoff function is not implemented".format(self.Name))
        return 0
    