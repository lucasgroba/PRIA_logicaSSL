from behivours.behavior import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math

dist = lambda a,b: math.sqrt((a['x']-b['x'])**2+(a['y']-b['y'])**2)
pend = lambda a,b: math.atan2((a['y']-b['y']),(a['x']-b['x']))
ball_position = {'x':0, 'y':0}



class GoToTheball(Behavior):

    def __init__(self,player):
        super().__init__()
        self.surpressed=True
        self.player=player
        
    def action(self):
        self.surpressed=False
        print('action gato')
        self.player.setPublisher(rospy.Publisher("/robot_blue_"+self.player.getId()+"/cmd", SSL,queue_size=10))
        
        r = rospy.Rate(10)
        msg = SSL()

        while not rospy.is_shutdown():

            goal_angle = pend(ball_position,self.player.getPosition())
            heading = abs(goal_angle - self.player.getAngle())
            distance = dist(ball_position,self.player.getPosition())

            if(distance < 0.2):
                msg.cmd_vel.linear.x = 0
                msg.cmd_vel.angular.z = 0
            else:
                if(heading<0.2):
                    msg.cmd_vel.linear.x = 0.5
                    msg.cmd_vel.angular.z = 0
                else:
                    msg.cmd_vel.linear.x = 0
                    msg.cmd_vel.angular.z = 0.25
            print(heading, distance)
            self.player.getPublisher().publish(msg)
        
    def surpress(self):
        print('surpress come')
        self.surpressed=True

    def takeControl(self):
        print('takeControl goToTheBall')
        return True #condicion para ejecutar el go to the ball