from behivours.behavior import Behavior
from behivours.behavior import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy

class PassTheball(Behavior):

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

        while not rospy.is_shutdown():

            ##goal_angle = pend(ball_position,self.player.getPosition())
            #heading = abs(goal_angle - self.player.getAngle())
            #distance = dist(ball_position,self.player.getPosition())
            msg.kicker=True
            self.player.getPublisher().publish(msg)
        
    def surpress(self):
        print('surpress pass the ball')
        self.surpressed=True

    def takeControl(self):
        print('takeControl passTheball')
        return True #condicion para ejecutar el go to the ball