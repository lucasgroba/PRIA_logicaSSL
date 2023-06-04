#!/usr/bin/env python3
import threading
from threading import Thread
import time

class Arbitrator:
    def __init__(self, behavior_list, return_when_inactive=False):
        self._minusOne = -1
        self._behavior = behavior_list
        self._highestPriority = self._minusOne
        self._returnWhenInactive = return_when_inactive
        self._active = self._minusOne
        self.keepRunning = True
        self.monitor = self.Monitor(self)
        self.monitor.setDaemon(True)
        print("Arbitrator createda")

    def go(self):
        self.monitor.start()
        while self._highestPriority == self._minusOne:
            time.sleep(0.25)

        while True:
            with self.monitor.lock:
                if self._highestPriority > self._minusOne:
                    self._active = self._highestPriority
                else:
                    if self._returnWhenInactive:
                        self.monitor.more = False
                        return
            if self._active != self._minusOne:
                self._behavior[self._active].action()
                self._active = self._minusOne

            time.sleep(0.25)

    def stop(self):
        self.keepRunning = False
    class Monitor(Thread):

        def __init__(self, arby):
            super().__init__()
            self.more = True
            self.arby = arby
            self.maxPriority = len(arby._behavior) - 1

        def run(self):

          while (self.arby.keepRunning):

            #FIND HIGHEST PRIORITY BEHAVIOR THAT WANTS CONTROL
            with threading.Lock():

                self.arby._highestPriority = self.arby._minusOne # -1
                for i in range(self.maxPriority, self.arby._active, -1):# only behaviors with higher priority are interesting

                    if self.arby._behavior[i].takeControl():

                        self.arby._highestPriority = i
                        break


                active = self.arby._active #local copy in case _active is set to NONE by the primary thread
                if self.arby._active != -1 and self.arby._highestPriority > self.arby._active:
                    self.arby._behavior[active].suppress()

            # end synchronize block - main thread can run now
            time.sleep(0)

