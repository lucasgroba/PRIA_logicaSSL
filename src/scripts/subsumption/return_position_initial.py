from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))



class ReturnPositionInitialV2(Behavior):

    def __init__(self, player, ball_position, all_players, players_my_team):
        super().__init__()
        self.suppressed = False
        self.player = player
        self.ball_position = ball_position
        self.contador = 0
        self.all_players = all_players
        self.players_my_team = players_my_team

    def action(self):
        self.suppressed = False
        print('Volviendo a mi posicion inicial --', self.player.getId())

        r = rospy.Rate(10)
        msg = SSL()
        goal_angle = pend(self.player.getPositionInitial(), self.player.getPosition())
        heading = abs(goal_angle - self.player.getAngle())
        distance = dist(self.player.getPositionInitial(), self.player.getPosition())
        

        if (distance < 130):
            msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = 0
        else:
            if (heading < 0.4):
                msg.cmd_vel.linear.x = 1
                msg.cmd_vel.angular.z = 0
            else:
                msg.cmd_vel.linear.x = 0
                msg.cmd_vel.angular.z = 0.5

            try:
                self.player.getPublisher().publish(msg)
            except:
                print("exception")


 

    def suppress(self):
        print('suppress come')
        self.suppressed = True

    def check(self):
            print('Vuelvo a la posicion Inicial:',not utils.they_have_the_ball(self.all_players,self.ball_position,130))
            if utils.they_have_the_ball(self.all_players,self.ball_position,130) or self.ball_position['x'] > 2000 or self.ball_position['x'] < -2000 or self.ball_position['y'] > 2000 or self.ball_position['y'] < -2000:
                return True
            else:
                return False
