#!/usr/bin/env python3
from threading import Thread
import time



class Arbitrator:   
    def __init__(self,behaviorList,returnWhenInactive):
        self._behavior = behaviorList
        self._returnWhenInactive = returnWhenInactive
        self._highestPriority= None
        self._active=None
        self.keepRunning=True
        self.monitor = self.Monitor()
        self.monitor.setDaemon(True)
        print("Arbitrator created")

    
class Monitor(Thread):
    
    def __init__(self,behaviorList,returnWhenInactive):
        self.more = True
        self.maxPriority = len(self._behavior) - 1
    
    def run(self):
    
      while (self.keepRunning):
      
        #FIND HIGHEST PRIORITY BEHAVIOR THAT WANTS CONTROL
        with self.lock:

            self._highestPriority = None; # -1
            for i in range(self.maxPriority, self._active, -1):# only behaviors with higher priority are interesting
          
                if self._behavior[i].takeControl():
                
                    self._highestPriority = i
                    break
                
          
            active = self._active; #local copy in case _active is set to NONE by the primary thread
            if self._active != None and self._highestPriority > self._active:
          
                self._behavior[active].suppress()
          
        # end synchronize block - main thread can run now
        time.sleep(0)
      
