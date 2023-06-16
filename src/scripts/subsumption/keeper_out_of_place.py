from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))
ball_position = {'x': 0, 'y': 0}


class KeeperMovingToPlaceV2(Behavior):

    def __init__(self, player):
        super().__init__()
        self.suppressed = False
        self.player = player


    def action(self):
        self.suppressed = False

        r = rospy.Rate(10)

        msg = SSL()

        print('action KeeperMovingToPlaceV2--', self.player.getPosition()['y'])

        msg.cmd_vel.linear.x = -1

        try:
            self.player.getPublisher().publish(msg)
        except:
            print("exception KeeperMovingToPlaceV2")


 

    def suppress(self):
        print('suppress KeeperMovingToPlaceV2')
        self.suppressed = True

    def check(self):
        print('check KeeperMovingToPlaceV2')
        r = rospy.Rate(10)

        return self.player.getPosition()['x'] < 1700



