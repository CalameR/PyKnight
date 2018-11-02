# Util/Observer.py
# Class support for "observer" pattern.
import Synchronization as SyncFile

class Observer:
    def update(self):
        '''Called when the observed object is
        modified. You call an Observable object's
        notifyObservers method to notify all the
        object's observers of the change.'''
        pass

class Observable(SyncFile.Synchronization):
    def __init__(self):
        self.obs = []
        self.changed = 0
        SyncFile.Synchronization.__init__(self)

    def addObserver(self, observer):
        if observer not in self.obs:
            self.obs.append(observer)

    def deleteObserver(self, observer):
        self.obs.remove(observer)

    def notifyObservers(self):
        '''If 'changed' indicates that this object
        has changed, notify all its observers, then
        call clearChanged(). Each observer has its
        update() called with two arguments: this
        observable object and the generic 'arg'.'''

        self.mutex.acquire()
        try:
            if not self.changed: return
            # Make a local copy in case of synchronous
            # additions of observers:
            localArray = self.obs[:]
            self.clearChanged()
        finally:
            self.mutex.release()
        # Updating is not required to be synchronized:
        for observer in localArray:
            observer.update()

    def deleteObservers(self): self.obs = []
    def setChanged(self): self.changed = 1
    def clearChanged(self): self.changed = 0
    def hasChanged(self): return self.changed
    def countObservers(self): return len(self.obs)

SyncFile.synchronize(Observable,
 "addObserver deleteObserver deleteObservers " +
 "setChanged clearChanged hasChanged " +
  "countObservers")
    
#name = "addObserver"
#print(Observable.__dict__.items())
#myvar = 0
#my2var = 0
#for (name, val) in Observable.__dict__.items():    
#    if (callable(val) and name != '__init__'):
#        print("{0} is the name".format(name))
#        myvar = val
#        print(myvar)
#        setattr(Observable,name, synchronized(myvar))
        #print(Observable.__dict__[name])
        
#for (name, val) in klass.__dict__.items():    
    #    if callable(val) and name != '__init__' and \
     #     (names == None or name in names):
      #      # print("synchronizing", name)
       #     klass.__dict__[name] = synchronized(val)