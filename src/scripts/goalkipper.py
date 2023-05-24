#!/usr/bin/env python3


import rospy
from geometry_msgs.msg import Twist
from grsim_ros_bridge_msgs.msg import SSL
from krssg_ssl_msgs.msg import SSL_DetectionFrame, SSL_DetectionBall, SSL_DetectionRobot
import math

robot0 = SSL_DetectionRobot()
robot1 = SSL_DetectionRobot()
robot2 = SSL_DetectionRobot()
robot3 = SSL_DetectionRobot()
robot4 = SSL_DetectionRobot()
ball = SSL_DetectionBall()

def vision_callback(data):
    global robot0,robot1,robot2,robot3,robot4, ball
    for i in range(0,len(data.robot_blue)):
        if(data.robot_blue[i].robot_id == 0):
            robot0 = data.robots_blue[i]
        if(data.robot_blue[i].robot_id == 1):
            robot1 = data.robots_blue[i]
        if(data.robot_blue[i].robot_id == 2):
            robot2 = data.robots_blue[i]
        if(data.robot_blue[i].robot_id == 3):
            robot3 = data.robots_blue[i]
        if(data.robot_blue[i].robot_id == 4):
            robot4 = data.robots_blue[i]
    ball = data.balls[]

if __name__=="__main__":
    rospy.init_node("grsim_pria",anonymous = False)
    rospy.Subscriber("/vision",SSL_DetectionFrame,vision_callback)
    pub_robot_4_blue = rospy.Publisher("/robot_blue_4/cmd", SSL,queue_size=10)

    r = rospy.Rate(100)

    robot0_x = 0
    robot0_y = 0
    ball_x = 0
    ball_y = 0
    msg = SSL()

    while not rospy.is_shutdown():
        try:
            robot0_x = robot0.x
            robot0_y = robot0.y
            ball_x = ball[0].x
            ball_y = ball[0].y
            
        except:
             pass
        
        goal_angle = math.atan2(ball_y-robot0_y,ball_x - robot0_x)
        heading = abs(goal_angle - robot0.orientation)
        distance = math.sqrt((ball_x - robot0_x)**2 + (ball_y - robot0_y)**2)

        if(distance < 0.2):
            msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = 0
        else:
            if(heading<0.2):
                msg.cmd_vel.linear.x = 0.25
                msg.cmd_vel.angular.z = 0
            else:
                msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = 0.25
