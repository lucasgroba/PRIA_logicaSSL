from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback
import utils


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))
position_max = {'x': 1450, 'y': -1250}


class RightSideAttackV2(Behavior):

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
        print('action right_side_attack --', self.player.getPosition()['x'])

        r = rospy.Rate(10)
        msg = SSL()
        goal_angle = pend(self.position_max, self.player.getPosition())
        heading = abs(goal_angle - self.player.getAngle())
        distance = dist(self.position_max, self.player.getPosition())
        

        if (distance < 105):
            msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = 0
        else:
            if (heading < 0.2):
                msg.cmd_vel.linear.x = 0.75
                msg.cmd_vel.angular.z = 0
            else:
                msg.cmd_vel.linear.x = 0
                msg.cmd_vel.angular.z = 1

            try:
                self.player.getPublisher().publish(msg)
            except:
                print("exception")


 

    def suppress(self):
        print('suppress come')
        self.suppressed = True

    def check(self):
            print('right condition:',not utils.they_have_the_ball(self.all_players,self.ball_position,110))
            if not utils.they_have_the_ball(self.all_players,self.ball_position,110):
                player_have_ball, distance_to_ball = utils.get_active_player(self.players_my_team,self.ball_position)
                print('check right_side_attack:', player_have_ball.getId(),self.player.getId(), distance_to_ball)
                if(player_have_ball != None and player_have_ball.getId() != self.player.getId() and self.player.getId() == 2 ):
                    #si uno de mis companeros tiene la peota y no soy yo y soy el jugador 2
                    return True
                else:
                    return False
            else:
                False
