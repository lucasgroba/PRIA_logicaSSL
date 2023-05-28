#!/usr/bin/env python3


class Player:




    def __init__(self,team,id):
        self.team = team
        self.position = {'x':0, 'y':0}
        self.angle = 0
        self.id = id
        self.publisher = None
        self.ball_possession = False
        self.active = False


    def getPosition(self):
        return self.position
    
    def getAngle(self):
        return self.angle
    
    def getId(self):
        return self.id
    
    def getPublisher(self):
        return self.publisher
    
    def getBallPossession(self):
        return self.ball_possession
    
    def getActive(self):
        return self.active
    


    def setPosition(self,x,y):
        self.position['x'] = x
        self.position['y'] = y
    
    def setAngle(self, angle):
        self.angle = angle
    
    def setId(self,id):
        self.id = id
    
    def setPublisher(self, publisher):
        self.publisher = publisher
    
    def setBallPossession(self, possession):
        self.ball_possession = possession
    
    def setActive(self, active):
        self.active = active
    

    



    
