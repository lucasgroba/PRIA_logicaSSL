from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))
ball_position = {'x': 0, 'y': 0}


class FaceFrontV2(Behavior):

    def __init__(self, player):
        super().__init__()
        self.suppressed = False
        self.player = player


    def action(self):
        self.suppressed = False
        r = rospy.Rate(10)


        msg = SSL()

        print('action FaceFrontV2--', self.player.getPosition()['y'])

        central_point_angle = utils.pend({'x': -4000, 'y': self.player.getPosition()['y']}, self.player.getPosition())

        if central_point_angle < 0:
            msg.cmd_vel.angular.z = 1.5
        else:
            msg.cmd_vel.angular.z = -1.5
        try:
            self.player.getPublisher().publish(msg)
        except:
            print("exception FaceFrontV2")


 

    def suppress(self):
        print('suppress FaceFrontV2')
        self.suppressed = True

    def check(self):
        r = rospy.Rate(10)

        central_point_angle = utils.pend({'x': -4000, 'y': self.player.getPosition()['y']}, self.player.getPosition())
        heading = abs(central_point_angle - self.player.getAngle())
        print('check FaceFrontV2: heading', heading," central_point_angle: ",central_point_angle)
        return heading > 1


        # condicion para ejecutar el go to the ball
