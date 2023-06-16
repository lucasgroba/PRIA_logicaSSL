from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))
ball_position = {'x': 0, 'y': 0}


class GoToTheBallV2(Behavior):

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

        r = rospy.Rate(10)
        msg = SSL()
        goal_angle = pend(self.ball_position, self.player.getPosition())
        heading = abs(goal_angle - self.player.getAngle())
        distance = dist(self.ball_position, self.player.getPosition())
        #print('action GoToTheball--', goal_angle)

        if (distance < 110):
            msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = 0
        else:
            if (heading < 0.4):
                msg.cmd_vel.linear.x = 0.75
                msg.cmd_vel.angular.z = 0
            else:
                    msg.cmd_vel.linear.x = 0
                    msg.cmd_vel.angular.z = goal_angle
            try:
                self.player.getPublisher().publish(msg)
            except:
                print("exception go to the ball")


 

    def suppress(self):
        print('suppress come')
        self.suppressed = True

    def check(self):
            #print('check goToTheBall')
            player_near, distance_to_ball = utils.get_active_player(self.players_my_team,self.ball_position)
            #print('go_to_teh_ball: distancia a mi jugador mas cercano',self.player.getId(), player_near.getId(),distance_to_ball)
            if(player_near.getId() == self.player.getId()):
                return True
            else:
                return False

        # condicion para ejecutar el go to the ball
