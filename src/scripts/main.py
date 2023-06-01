#!/usr/bin/env python3
from behivours.go_to_the_ball import GoToTheball
from behivours.stay_in_field import StayInField
from behivours.stop_all_action import StopAllAction
from behivours.pass_the_ball import PassTheball
from subsumption.arbitrator import Arbitrator
import rospy
from geometry_msgs.msg import Twist
from grsim_ros_bridge_msgs.msg import SSL
from krssg_ssl_msgs.msg import SSL_DetectionFrame, SSL_DetectionBall, SSL_DetectionRobot
import math
import utils
import player

dist = lambda a,b: math.sqrt((a['x']-b['x'])**2+(a['y']-b['y'])**2)
pend = lambda a,b: math.atan2((a['y']-b['y']),(a['x']-b['x']))



player0 = player.Player('blue','0')
player1 = player.Player('blue','1')
player2 = player.Player('blue','2')
player3 = player.Player('blue','3')
player4 = player.Player('blue','4')
# instancio los jugadores de mi equipo
behabe = GoToTheball(player0) 
behabe.action()
behabe.surpress()
behabe.takeControl()

ball_position = {'x':0, 'y':0}
#instancio la posicion de la pelota

player_my_team = [player0,player1,player2,player3,player4]
#agregi mis jugadores a un array

b1=StopAllAction(player1)
b2=StayInField(player1)
b3=GoToTheball(player1)
b4=PassTheball(player1)


bArray = (b4,b3,b2,b1)
arby = Arbitrator(bArray,True)
arby.start()




def vision_callback(data):
    global player0,player1,player2,player3,player4, ball_position
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

def pass_to_another_player(self):


        player_near = utils.get_closer_player()
        angle_player_near = utils.get_angle_player_object(self.getPosition(),)






if __name__=="__main__":
    rospy.init_node("grsim_pria",anonymous = False)
    rospy.Subscriber("/vision",SSL_DetectionFrame,vision_callback)
    
    go_to_ball(player1)
    go_to_ball(player0)
    
