class MyTest(object):
    def __init__(self,val1):
        self.val1 = val1
    
    def getVal2(self):
        return self._val2
    
    def setVal2(self,val2):
        self._val2 = val2

if __name__=="__main__":
    x = MyTest(1)
    x.setVal2(2)
    print(x.getVal2())
