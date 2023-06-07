from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy

class PassTheballV2(Behavior):

    def __init__(self,player):
        super().__init__()
        self.suppressed=True
        self.player=player
        
    def action(self):
        self.suppressed=False
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
        
    def suppress(self):
        print('suppress pass the ball')
        self.suppressed=True

    def check(self):
        print('check passTheball')
        return True #condicion para ejecutar el go to the ball