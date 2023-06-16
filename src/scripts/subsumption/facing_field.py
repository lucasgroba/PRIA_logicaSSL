from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))
ball_position = {'x': 0, 'y': 0}


class FaceFieldV2(Behavior):

    def __init__(self, player):
        super().__init__()
        self.suppressed = False
        self.player = player


    def action(self):
        self.suppressed = False

        r = rospy.Rate(10)
        msg = SSL()

        print('action FaceFieldV2--', self.player.getPosition()['y'])

        central_point_angle = utils.pend({'x': 0, 'y': 0}, self.player.getPosition())

        if(central_point_angle < 0):
            msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = -0.5
        else:
            msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = 0.5
        try:
            self.player.getPublisher().publish(msg)
        except:
            print("exception FaceFieldV2")


 

    def suppress(self):
        print('suppress come')
        self.suppressed = True

    def check(self):
        r = rospy.Rate(10)

        central_point_angle = utils.pend({'x': 0, 'y': 0}, self.player.getPosition())
        heading = abs(central_point_angle - self.player.getAngle())
        print('action FaceFieldV2: ', heading," ",central_point_angle)
        return heading > 0.3


        # condicion para ejecutar el go to the ball
