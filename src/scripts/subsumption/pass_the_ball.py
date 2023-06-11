from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
from utils import dist
import rospy

class PassTheballV2(Behavior):

    def __init__(self, player, ball_position):
        super().__init__()
        self.suppressed=True
        self.player=player
        self.ball_position = ball_position
        
    def action(self):
        self.suppressed=False
        print('action pass the ball')
        self.player.setPublisher(rospy.Publisher("/robot_blue_"+self.player.getId()+"/cmd", SSL,queue_size=10))

        msg = SSL()


            ##goal_angle = pend(ball_position,self.player.getPosition())
            #heading = abs(goal_angle - self.player.getAngle())
            #distance = dist(ball_position,self.player.getPosition())
        msg.cmd_vel.linear.x = 0
        msg.cmd_vel.angular.z = 0
        msg.kicker = 100
        # if self.contador % 5000 == 0:
        print("playerid: ", self.player.getId(), "publisher: ", self.player.getPublisher(),' mensaje ',msg)
        self.player.getPublisher().publish(msg)
        
    def suppress(self):
        print('suppress pass the ball')
        self.suppressed=True

    def check(self):

        distance = dist(self.ball_position, self.player.getPosition())
        print('check passTheball distance: ',distance)
        return distance < 105 #condicion para ejecutar el go to the ball