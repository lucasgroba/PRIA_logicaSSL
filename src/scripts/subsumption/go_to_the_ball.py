from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import rospy
import math
import traceback


dist = lambda a, b: math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)
pend = lambda a, b: math.atan2((a['y'] - b['y']), (a['x'] - b['x']))
ball_position = {'x': 0, 'y': 0}


class GoToTheballV2(Behavior):

    def __init__(self, player, ball_position):
        super().__init__()
        self.suppressed = False
        self.player = player
        self.ball_position = ball_position

    def action(self):
        self.suppressed = False
        print('action GoToTheball--')

        r = rospy.Rate(10)
        msg = SSL()
        print('action GoToTheball--2'+str(not (rospy.is_shutdown() or self.suppressed)))

        while not rospy.is_shutdown() or not self.suppressed:
            print("ball position: ", str(self.ball_position), " player: ", str(self.player.getPosition()))

            goal_angle = pend(self.ball_position, self.player.getPosition())
            print("im in2")

            heading = abs(goal_angle - self.player.getAngle())
            print("im in3")
            distance = dist(self.ball_position, self.player.getPosition())
            print(heading, distance)

            if (distance < 0.2):
                msg.cmd_vel.linear.x = 0
                msg.cmd_vel.angular.z = 0
            else:
                if (heading < 0.2):
                    msg.cmd_vel.linear.x = 0.5
                    msg.cmd_vel.angular.z = 0
                else:
                    msg.cmd_vel.linear.x = 0
                    msg.cmd_vel.angular.z = 1
            print(heading, distance, "playerid: ", self.player.getId(), "publisher: ", self.player.topic)
            try:
                self.player.getPublisher().publish(msg)
            except:
                print("exception")

            print('check goToTheBall'+str(self.player.getPosition()['x'] >2000))

    def suppress(self):
        print('suppress come')
        self.suppressed = True

    def check(self):
        # print('check goToTheBall'+str(self.player.getPosition()['x'] >2000))
        return True  # condicion para ejecutar el go to the ball
