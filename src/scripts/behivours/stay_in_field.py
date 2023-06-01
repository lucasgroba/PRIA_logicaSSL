from behivours.behavior import Behavior
from behivours.behavior import Behavior
from behivours.behavior import Behavior
from behivours.behavior import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy

class StayInField(Behavior):

    def __init__(self,player):
        super().__init__()
        self.surpressed=True
        self.player=player
            
    def action(self):
        self.surpressed=False
        print('action pass the ball')
        self.player.setPublisher(rospy.Publisher("/robot_blue_"+self.player.getId()+"/cmd", SSL,queue_size=10))
        
        r = rospy.Rate(10)
        msg = SSL()

        while not rospy.is_shutdown() and not self.surpressed:

            msg.cmd_vel.angular.x=0
            msg.cmd_vel.angular.y=0
            msg.cmd_vel.angular.z=0
            msg.cmd_vel.linear.x=0
            msg.cmd_vel.linear.y=0
            msg.cmd_vel.linear.z=0
            self.player.getPublisher().publish(msg)
            
    def surpress(self):
        print('surpress pass the ball')
        self.surpressed=True

    def takeControl(self):
        print('takeControl passTheball')
        return True #condicion para ejecutar el go to the ball