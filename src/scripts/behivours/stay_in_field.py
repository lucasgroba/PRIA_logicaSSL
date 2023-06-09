from behivours.behavior import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy

class StayInField(Behavior):

    def __init__(self, player):
        super().__init__()
        self.suppressed = False
        self.player = player
        self.i=0

    def action(self):
        self.suppressed = False

        r = rospy.Rate(10)
        msg = SSL()

        while not rospy.is_shutdown() and not self.suppressed:

            msg.cmd_vel.angular.x = 0
            msg.cmd_vel.angular.y = 0
            msg.cmd_vel.angular.z = 0
            msg.cmd_vel.linear.x = -1
            msg.cmd_vel.linear.y = 0
            msg.cmd_vel.linear.z = 0
            self.player.getPublisher().publish(msg)
            self.i += 1
            if self.i % 5000 == 0:
                print('takedControl StayInField :'+str(self.player.getPosition()['x']), msg.cmd_vel.angular.z)
            
    def suppress(self):
        print('surpress StayInField')
        self.suppressed = True

    def takeControl(self):

        # if self.i % 5000 == 0:
        #     print('takeControl StayInField: ',self.player.getPosition()['x'])
        return self.player.getPosition()['x'] >2000 #condicion para ejecutar el go to the ball