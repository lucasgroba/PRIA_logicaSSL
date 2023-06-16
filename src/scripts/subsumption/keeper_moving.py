from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))


class KeeperMovingV2(Behavior):

    def __init__(self, player):
        super().__init__()
        self.suppressed = False
        self.player=player

    def action(self):
        self.suppressed = False

        msg = SSL()
        r = rospy.Rate(10)

        print('action KeeperMovingV2-- pos y=', self.player.getPosition()['y'])


        if self.player.getPosition()['y'] <= 0:
            msg.cmd_vel.linear.y = -1.5
            msg.cmd_vel.linear.x = 0.3
        if self.player.getPosition()['y'] > 0:
            msg.cmd_vel.linear.y = 1.5
            msg.cmd_vel.linear.x = 0.3

        try:
            r = rospy.Rate(10)

            self.player.getPublisher().publish(msg)
        except:
            print("exception KeeperMovingV2")


 

    def suppress(self):
        print('suppress come')
        self.suppressed = True

    def check(self):
        print('action KeeperMovingV2-- pos y=', self.player.getPosition()['y'])
        return True


        # condicion para ejecutar el go to the ball
