#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from grsim_ros_bridge_msgs.msg import SSL
from krssg_ssl_msgs.msg import SSL_DetectionFrame, SSL_DetectionBall, SSL_DetectionRobot
import math
import utils

#Funciones lambda para facilitar la lectura del codigo
dist = lambda a,b: math.sqrt((a['x']-b['x'])**2+(a['y']-b['y'])**2)
pend = lambda a,b: math.atan2((a['y']-b['y']),(a['x']-b['x']))


class Player:

    def __init__(self, team, id, publisher,position_initial):
        self.team = team
        self.position = {'x': 0, 'y': 0}
        self.angle = 0
        self.id = id
        self.publisher = publisher
        self.ball_possession = False
        self.active = False
        self.topic = None
        self.position_initial = position_initial


    def getPosition(self):
        return self.position
    
    def getPositionInitial(self):
        return self.position_initial
    
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
    
    def getTeam(self):
        return self.team
    


    def setPosition(self,x,y):
        self.position['x'] = x
        self.position['y'] = y


    def setPositionInitial(self,x,y):
        self.position_initial['x'] = x
        self.position_initial['y'] = y
    
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

    def setTopic(self, topic):
        self.topic = topic

    def getTopic(self):
        return self.topic    


    def kicker(self):

        msg = SSL()
        msg.kicker = True
        print("patie soy: ",self.getId())
        self.getPublisher().publish(msg)
        msg.kicker = False
        self.getPublisher().publish(msg)


    def dribbler_on(self):
        msg = SSL()
        msg.dribbler = True
        print("estoy dribbleando: ",self.getId())
        self.getPublisher().publish(msg)

    def dribbler_off(self):
        msg = SSL()
        msg.dribbler = False
        print("deje de dribblear: ",self.getId())
        self.getPublisher().publish(msg)
        


