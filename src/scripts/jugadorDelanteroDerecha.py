#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from grsim_ros_bridge_msgs.msg import SSL
from krssg_ssl_msgs.msg import SSL_DetectionFrame, SSL_DetectionBall, SSL_DetectionRobot
import math
import utils
import player

PLAYER_ID = 3


#Funciones lambda para facilitar la lectura del codigo
dist = lambda a,b: math.sqrt((a['x']-b['x'])**2+(a['y']-b['y'])**2)
pend = lambda a,b: math.atan2((a['y']-b['y']),(a['x']-b['x']))

player0 = player.Player('blue','0')
player1 = player.Player('blue','1')
player2 = player.Player('blue','2')
player3 = player.Player('blue','3')
player4 = player.Player('blue','4')
# instancio los jugadores de mi equipo


rival0 = player.Player('yellow','0')
rival1 = player.Player('yellow','1')
rival2 = player.Player('yellow','2')
rival3 = player.Player('yellow','3')
rival4 = player.Player('yellow','4')
#instancio mis rivales


ball_position = {'x':0, 'y':0}
#instancio la posicion de la pelota

player_my_team = [player0,player1,player2,player3,player4]
#agregue mis jugadores a un array

player_rival_team = [rival0,rival1,rival2,rival3,rival4]
#agrego mis rivales en un array 

all_players = player_my_team + player_rival_team


def vision_callback(data):
    global player0,player1,player2,player3,player4, ball_position,rival0,rival1,rival2,rival3,rival4
    if len(data.robots_blue)> 0:
        for item in data.robots_blue:
            
            try:
                
                if item.robot_id == 0:
                    player0.setPosition(item.x,item.y)
                    player0.setAngle(item.orientation)
                if item.robot_id == 1:
                    player1.setPosition(item.x,item.y)
                    player1.setAngle(item.orientation)
                if item.robot_id == 2:
                    player2.setPosition(item.x,item.y)
                    player2.setAngle(item.orientation)
                if item.robot_id == 3:
                    player3.setPosition(item.x,item.y)
                    player3.setAngle(item.orientation)
                if item.robot_id == 4:
                    player4.setPosition(item.x,item.y)
                    player4.setAngle(item.orientation)      
            except:
                pass
    if len(data.robots_yellow)> 0:
        for item in data.robots_yellow:
            
            try:
                
                if item.robot_id == 0:
                    rival0.setPosition(item.x,item.y)
                    rival0.setAngle(item.orientation)
                if item.robot_id == 1:
                    rival1.setPosition(item.x,item.y)
                    rival1.setAngle(item.orientation)
                if item.robot_id == 2:
                    rival2.setPosition(item.x,item.y)
                    rival2.setAngle(item.orientation)
                if item.robot_id == 3:
                    rival3.setPosition(item.x,item.y)
                    rival3.setAngle(item.orientation)
                if item.robot_id == 4:
                    rival4.setPosition(item.x,item.y)
                    rival4.setAngle(item.orientation)      
            except:
                pass
    

    if len(data.balls)> 0:
        ball_position['x'] = data.balls[0].x
        ball_position['y'] = data.balls[0].y





def go_to_ball(player):
        
        player.setPublisher(rospy.Publisher("/robot_blue_"+player.getId()+"/cmd", SSL,queue_size=10))


        r = rospy.Rate(10)

     
        
        msg = SSL()

        while not rospy.is_shutdown():

            goal_angle = pend(ball_position,player.getPosition())
            heading = abs(goal_angle - player.getAngle())
            distance = dist(ball_position,player.getPosition())

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
            player.getPublisher().publish(msg)


def go_to_goal(player):
        ##implementar manana
        player.setPublisher(rospy.Publisher("/robot_blue_"+player.getId()+"/cmd", SSL,queue_size=10))


        r = rospy.Rate(10)

     
        
        msg = SSL()

        while not rospy.is_shutdown():

            goal_angle = pend(ball_position,player.getPosition())
            heading = abs(goal_angle - player.getAngle())
            distance = dist(ball_position,player.getPosition())

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
            player.getPublisher().publish(msg)




def search_to_pass(self):


        player_near = utils.get_closer_player()
        angle_player_near = utils.get_angle_player_object(self.getPosition(),)





if __name__=="__main__":
    rospy.init_node("grsim_pria",anonymous = False)
    rospy.Subscriber("/vision",SSL_DetectionFrame,vision_callback)
    
    #comienza la logica de Juego
    if utils.they_have_the_ball(all_players,ball_position,0.04):
        player_near, distance_to_ball = utils.get_active_player(player_my_team,ball_position)
        if player_near.getId() == PLAYER_ID:
