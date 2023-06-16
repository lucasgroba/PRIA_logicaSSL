from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))


class KeeperPassTheBallV2(Behavior):

    def __init__(self, player,allPlayers,ballPosition):
        super().__init__()
        self.suppressed = False
        self.player=player
        self.allPlayers=allPlayers
        self.ballPosition=ballPosition

    def action(self):
        self.suppressed = False

        msg = SSL()
        r = rospy.Rate(10)

        print('action KeeperPassTheBallV2-- pos y=', self.player.getPosition()['y'])

        closer_player= utils.get_closer_player(self.allPlayers, self.player,True)

        central_point_angle = utils.pend({'x': -4000, 'y': self.player.getPosition()['y']}, self.player.getPosition())


        if central_point_angle < 0:
            msg.cmd_vel.angular.z = 1.5
        else:
            msg.cmd_vel.angular.z = -1.5


        try:
            r = rospy.Rate(10)

            self.player.getPublisher().publish(msg)
        except:
            print("exception KeeperMovingV2")


 

    def suppress(self):
        print('suppress KeeperPassTheBallV2')
        self.suppressed = True

    def check(self):
        distance = utils.dist(self.goal_position, self.player.getPosition())

        print('action KeeperPassTheBallV2-- pos distance=',distance)
        return distance < 105


        # condicion para ejecutar el go to the ball
