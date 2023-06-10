from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import utils
import rospy

class ShootBallV2(Behavior):

    def __init__(self, player, ball_position, goal_position,all_players, players_my_team):
        super().__init__()
        self.suppressed=True
        self.player=player
        self.ball_position = ball_position
        self.goal_position = goal_position
        self.all_players = all_players
        self.players_my_team = players_my_team
        
    def action(self):
        self.suppressed=False
        print('action shoot the ball')
        self.player.setPublisher(rospy.Publisher("/robot_blue_"+self.player.getId()+"/cmd", SSL,queue_size=10))
        
        r = rospy.Rate(10)
        msg = SSL()


            ##goal_angle = pend(ball_position,self.player.getPosition())
            #heading = abs(goal_angle - self.player.getAngle())
            #distance = dist(ball_position,self.player.getPosition())
        msg.cmd_vel.linear.x = 0
        msg.cmd_vel.angular.z = 0
        msg.kicker = True
        # if self.contador % 5000 == 0:
        print("playerid: ", self.player.getId(), "publisher: ", self.player.getPublisher(),' mensaje ',msg)
        self.player.getPublisher().publish(msg)
        
    def suppress(self):
        print('suppress shoot the ball')
        r = rospy.Rate(10)
        msg = SSL()
        msg.cmd_vel.linear.x = 0
        msg.cmd_vel.angular.z = 0
        msg.kicker = False
        self.player.getPublisher().publish(msg)
        self.suppressed=True

    def check(self):

        if utils.they_have_the_ball(self.all_players,self.ball_position,105):
            print('Entre al if del check del shoot')
            player_near, distance_to_ball = utils.get_active_player(self.players_my_team,self.ball_position)
            ##me retorna el jugador que tiene la pelota
            player_near_goal, distance_to_goal = utils.get_active_player(self.players_my_team,self.goal_position)
            #retorna el jugador de mi equipo  mas cercano al arco rival
            if(player_near.getId() == self.player.getId() and player_near_goal.getId() == self.player.getId() and distance_to_goal < 1500):
                return True
            else:
                return False
        else:
            return False  