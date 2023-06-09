#!/usr/bin/env python3
import threading

from behivours.go_to_the_ball import GoToTheball
from behivours.stay_in_field import StayInField
from behivours.stop_all_action import StopAllAction
from behivours.pass_the_ball import PassTheball
from subsumption.arbitrator import Arbitrator
import rospy
from geometry_msgs.msg import Twist
from grsim_ros_bridge_msgs.msg import SSL
from krssg_ssl_msgs.msg import SSL_DetectionFrame, SSL_DetectionBall, SSL_DetectionRobot
from subsumption.arbitratorV2 import Controller
from subsumption.go_to_the_ball import GoToTheballV2
from subsumption.stay_in_field import StayInFieldV2
from subsumption.pass_the_ball import PassTheballV2
import math
import utils
import player
import time
import sys
import time

# Constantes
POSITION_GOAL = {'x': 2, 'y': 0}

# Funciones lambda para facilitar la lectura del codigo
dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))

player0 = player.Player('blue', '0')
player1 = player.Player('blue', '1')
player2 = player.Player('blue', '2')
player3 = player.Player('blue', '3')
player4 = player.Player('blue', '4')
# instancio los jugadores de mi equipo

subsumption_controller_player0 = Controller(False)
subsumption_controller_player1 = Controller(False)
subsumption_controller_player2 = Controller(False)

rival0 = player.Player('yellow', '0')
rival1 = player.Player('yellow', '1')
rival2 = player.Player('yellow', '2')
rival3 = player.Player('yellow', '3')
rival4 = player.Player('yellow', '4')
# instancio mis rivales
ball_position = {'x': 0, 'y': 0}
# instancio la posicion de la pelota

player_my_team = [player0, player1, player2, player3, player4]
# agregue mis jugadores a un array

player_rival_team = [rival0, rival1, rival2, rival3, rival4]
# agrego mis rivales en un array

all_players = player_my_team + player_rival_team


def vision_callback(data):
    global player0, player1, player2, player3, player4, ball_position, \
        rival0, rival1, rival2, rival3, rival4
    if len(data.robots_blue) > 0:
        for item in data.robots_blue:

            try:

                if item.robot_id == 0:
                    player0.setPosition(item.x, item.y)
                    player0.setAngle(item.orientation)
                if item.robot_id == 1:
                    player1.setPosition(item.x, item.y)
                    player1.setAngle(item.orientation)
                if item.robot_id == 2:
                    player2.setPosition(item.x, item.y)
                    player2.setAngle(item.orientation)
                if item.robot_id == 3:
                    player3.setPosition(item.x, item.y)
                    player3.setAngle(item.orientation)
                if item.robot_id == 4:
                    player4.setPosition(item.x, item.y)
                    player4.setAngle(item.orientation)
            except:
                pass
    if len(data.robots_yellow) > 0:
        for item in data.robots_yellow:

            try:

                if item.robot_id == 0:
                    rival0.setPosition(item.x, item.y)
                    rival0.setAngle(item.orientation)
                if item.robot_id == 1:
                    rival1.setPosition(item.x, item.y)
                    rival1.setAngle(item.orientation)
                if item.robot_id == 2:
                    rival2.setPosition(item.x, item.y)
                    rival2.setAngle(item.orientation)
                if item.robot_id == 3:
                    rival3.setPosition(item.x, item.y)
                    rival3.setAngle(item.orientation)
                if item.robot_id == 4:
                    rival4.setPosition(item.x, item.y)
                    rival4.setAngle(item.orientation)
            except:
                pass

    if len(data.balls) > 0:
        ball_position['x'] = data.balls[0].x
        ball_position['y'] = data.balls[0].y


# def go_to_ball(player):
#
#     player.setPublisher(rospy.Publisher("/robot_blue_"+player.getId()+"/cmd", SSL,queue_size=10))
#
#
#     r = rospy.Rate(10)
#
#
#
#     msg = SSL()
#     ret = True
#     while ret :
#
#         goal_angle = pend(POSITION_GOAL,player.getPosition())
#         heading = abs(goal_angle - player.getAngle())
#         distance = dist(POSITION_GOAL,player.getPosition())
#
#         if(distance < 105 and distance != 0.0):
#             msg.cmd_vel.linear.x = 0
#             msg.cmd_vel.angular.z = 0
#             ret = False
#
#         else:
#             if(heading < 0.2):
#                 msg.cmd_vel.linear.x = 0.25
#                 msg.cmd_vel.angular.z = 0
#             else:
#                 msg.cmd_vel.linear.x = 0
#                 msg.cmd_vel.angular.z = 0.25
#         print(player.getPosition())
#         print(heading, distance)
#         player.getPublisher().publish(msg)

# def go_to_goal(player):
#
#     player.setPublisher(rospy.Publisher("/robot_blue_"+player.getId()+"/cmd", SSL,queue_size=10))
#
#
#     r = rospy.Rate(10)
#
#
#
#     msg = SSL()
#     ret = True
#     while ret :
#
#         goal_angle = pend(ball_position,player.getPosition())
#         heading = abs(goal_angle - player.getAngle())
#         distance = dist(ball_position,player.getPosition())
#
#         if(distance < 105 and distance != 0.0):
#             msg.cmd_vel.linear.x = 0
#             msg.cmd_vel.angular.z = 0
#             ret = False
#
#         else:
#             if(heading < 0.2):
#                 msg.cmd_vel.linear.x = 0.25
#                 msg.cmd_vel.angular.z = 0
#             else:
#                 msg.cmd_vel.linear.x = 0
#                 msg.cmd_vel.angular.z = 0.25
#         print(player.getPosition())
#         print(heading, distance)
#         player.getPublisher().publish(msg)

def pass_to_another_player(self):
    player_near = utils.get_closer_player()
    angle_player_near = utils.get_angle_player_object(self.getPosition(), )


def search_to_pass(self):
    player_near = utils.get_closer_player()
    angle_player_near = utils.get_angle_player_object(self.getPosition(), )


def _run(subsumption_controller):
    try:
        subsumption_controller.start()
    except Exception as e:
        print(e)


def run(subsumption_controller_list):
    for controller in subsumption_controller_list:
        thread = threading.Thread(name="Continuous behavior checker",
                                  target=_run, args=[controller])
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    rospy.init_node("grsim_pria", anonymous=False)
    rospy.Subscriber("/vision", SSL_DetectionFrame, vision_callback)
    r = rospy.Rate(10)
    #
    # bh = GoToTheball(player0, ball_position)
    # bh.action()
    # go_to_ball(player0)
    # b0 = StopAllAction(player0)
    # b1 = StayInField(player0)
    # b2 = GoToTheball(player0, ball_position)
    # b3 = PassTheball(player0)
    #
    # bArray = [b3, b2, b1, b0]
    # bArray = [GoToTheball(player0, ball_position), StayInField(player0)]
    # arby = Arbitrator(bArray, True)
    # arby.go()
    subsumption_controller_player0.behaviors = [StayInFieldV2(player0), PassTheballV2(player0, ball_position),
                                                GoToTheballV2(player0, ball_position)]
    subsumption_controller_player1.behaviors = [StayInFieldV2(player1), GoToTheballV2(player1, ball_position)]
    subsumption_controller_player2.behaviors = [StayInFieldV2(player2), GoToTheballV2(player2, ball_position)]
    controller_list = [subsumption_controller_player0, subsumption_controller_player1, subsumption_controller_player2]
    run(controller_list)
    print("Frun")

    rospy.spin()

# def lucasMain():
#     rospy.init_node("grsim_pria",anonymous = False)
#     rospy.Subscriber("/vision",SSL_DetectionFrame,vision_callback)
#     # go_to_ball(player1)
#     # player1.dribbler_on()
#     # time.sleep(1.5)
#     # player1.dribbler_off()
#     # player1.kicker()
#     #go_to_ball(player1)
#     run  = True

#     while run:
#         #comienza la logica de Juego
#         if utils.they_have_the_ball(all_players,ball_position,0.04):
#             ##Si mi equipo tiene la pelota
#             player_near, distance_to_ball = utils.get_active_player(player_my_team,ball_position)
#             ##obtengo el jugador activo o mas cercano
#             go_to_goal(player_near)


#             if utils.they_have_the_ball(player_my_team,POSITION_GOAL,0.9):
#                 #Si tengo un jugador en mejor posicion tengo que dar el pase
#                 ## Implementar funcion de pase
#                 pass
#             else:
#                 go_to_goal(player3)
