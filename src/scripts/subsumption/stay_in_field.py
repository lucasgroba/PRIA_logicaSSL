from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy

class StayInFieldV2(Behavior):

    def __init__(self, player):
        super().__init__()
        self.suppressed = False
        self.player = player

    def action(self):
        self.suppressed = False
        print('StayInField')

        r = rospy.Rate(10)
        msg = SSL()
        msg.cmd_vel.angular.x = 0
        msg.cmd_vel.angular.y = 0
        msg.cmd_vel.angular.z = 0
        msg.cmd_vel.linear.x = -1
        msg.cmd_vel.linear.y = 0
        msg.cmd_vel.linear.z = 0
        self.player.getPublisher().publish(msg)
            
    def suppress(self):
        print('suppress StayInField')
        self.suppressed=True

    def check(self):
        print('check StayInField: ',self.player.getPosition()['x'])
        return self.player.getPosition()['x'] >2000 or  self.player.getPosition()['x'] <-2000 \
        or self.player.getPosition()['y'] >2000 or self.player.getPosition()['y'] < -2000   #condicion para ejecutar el go to the ball