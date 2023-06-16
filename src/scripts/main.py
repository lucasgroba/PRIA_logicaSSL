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
from subsumption.go_to_the_ball import GoToTheBallV2
from subsumption.stay_in_field import StayInFieldV2
from subsumption.pass_the_ball import PassTheballV2
from subsumption.shoot_ball import ShootBallV2
from subsumption.go_to_the_goal import GoToTheGoalV2
from subsumption.left_side_attack import LeftSideAttackV2
from subsumption.right_side_attack import RightSideAttackV2
from subsumption.return_position_initial import ReturnPositionInitialV2
from subsumption.keeper_moving import KeeperMovingV2
from subsumption.keeper_out_of_place import KeeperMovingToPlaceV2
from subsumption.facing_field import FaceFieldV2
from subsumption.facing_front import FaceFrontV2
import math
import utils
import player
import time
import sys
import time

# Constantes
POSITION_GOAL = {'x': 2000, 'y': 0}

# Funciones lambda para facilitar la lectura del codigo
dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))

player0 = player.Player('blue', '0',rospy.Publisher("/robot_blue_"+'0'+"/cmd", SSL, queue_size=10),{'x': -2000, 'y': 0})
player1 = player.Player('blue', '1',rospy.Publisher("/robot_blue_"+'1'+"/cmd", SSL, queue_size=10),{'x': -1300, 'y': 0})
player2 = player.Player('blue', '2',rospy.Publisher("/robot_blue_"+'2'+"/cmd", SSL, queue_size=10),{'x': -1500, 'y': -1500})
player3 = player.Player('blue', '3',rospy.Publisher("/robot_blue_"+'3'+"/cmd", SSL, queue_size=10),{'x': -500, 'y': 0})
player4 = player.Player('blue', '4',rospy.Publisher("/robot_blue_"+'4'+"/cmd", SSL, queue_size=10),{'x': -1500, 'y': 1500})
# instancio los jugadores de mi equipo

subsumption_controller_player0 = Controller(False)
subsumption_controller_player1 = Controller(False)
subsumption_controller_player2 = Controller(False)
subsumption_controller_player3 = Controller(False)
subsumption_controller_player_rival0 = Controller(False)

rival0 = player.Player('yellow', '0',rospy.Publisher("/robot_yellow_"+'0'+"/cmd", SSL, queue_size=10),{'x': 2000, 'y': 0})
rival1 = player.Player('yellow', '1',rospy.Publisher("/robot_yellow_"+'1'+"/cmd", SSL, queue_size=10),{'x': 2000, 'y': 0})
rival2 = player.Player('yellow', '2',rospy.Publisher("/robot_yellow_"+'2'+"/cmd", SSL, queue_size=10),{'x': 2000, 'y': 0})
rival3 = player.Player('yellow', '3',rospy.Publisher("/robot_yellow_"+'3'+"/cmd", SSL, queue_size=10),{'x': 2000, 'y': 0})
rival4 = player.Player('yellow', '4',rospy.Publisher("/robot_yellow_"+'4'+"/cmd", SSL, queue_size=10),{'x': 2000, 'y': 0})
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



    subsumption_controller_player2.behaviors = [StayInFieldV2(player2), 
                                                # PassTheballV2(player0, ball_position),
                                                ShootBallV2(player2, ball_position,POSITION_GOAL,all_players,player_my_team),
                                                GoToTheGoalV2(player2, ball_position,POSITION_GOAL,all_players,player_my_team),
                                                ReturnPositionInitialV2(player2, ball_position,all_players,player_my_team),
                                                GoToTheBallV2(player2, ball_position,all_players,player_my_team),
                                                RightSideAttackV2(player2, ball_position,all_players,player_my_team)]
    subsumption_controller_player1.behaviors = [StayInFieldV2(player1),
                                                GoToTheGoalV2(player1, ball_position,POSITION_GOAL,all_players,player_my_team),
                                                ReturnPositionInitialV2(player1, ball_position,all_players,player_my_team),
                                                GoToTheBallV2(player1, ball_position,all_players,player_my_team),
                                                ]
    subsumption_controller_player0.behaviors = [StayInFieldV2(player0),
                                                # PassTheballV2(player2, ball_position),
                                                ShootBallV2(player0, ball_position,POSITION_GOAL,all_players,player_my_team),
                                                GoToTheGoalV2(player0, ball_position,POSITION_GOAL,all_players,player_my_team),
                                                ReturnPositionInitialV2(player0, ball_position,all_players,player_my_team),
                                                GoToTheBallV2(player0, ball_position,all_players,player_my_team), 
                                                LeftSideAttackV2(player0, ball_position,all_players,player_my_team)]
    subsumption_controller_player3.behaviors = [StayInFieldV2(player3),
                                                ShootBallV2(player3, ball_position,POSITION_GOAL,all_players,player_my_team),
                                                GoToTheGoalV2(player3, ball_position,POSITION_GOAL,all_players,player_my_team),
                                                ReturnPositionInitialV2(player2, ball_position,all_players,player_my_team),
                                                GoToTheBallV2(player3, ball_position,all_players,player_my_team)]
    subsumption_controller_player_rival0.behaviors = [StayInFieldV2(rival0),FaceFrontV2(rival0),
                                                      KeeperMovingToPlaceV2(rival0),KeeperMovingV2(rival0)]

    controller_list = [subsumption_controller_player0,subsumption_controller_player1,subsumption_controller_player2,
                       subsumption_controller_player3,subsumption_controller_player_rival0]
    run(controller_list)
    print("Frun")

    rospy.spin()
