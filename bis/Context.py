class Context(object):
    def GetItems(self):
        return self.__dict__.items()
    
    def __setattr__(self,name,value):
        self.__dict__[name] = value