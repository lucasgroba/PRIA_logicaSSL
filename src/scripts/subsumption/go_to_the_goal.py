from subsumption.arbitratorV2 import Behavior
from grsim_ros_bridge_msgs.msg import SSL
import utils
import rospy

class GoToTheGoalV2(Behavior):

    def __init__(self, player, ball_position, goal_position,all_players, players_my_team):
        super().__init__()
        self.suppressed=True
        self.player=player
        self.ball_position = ball_position
        self.goal_position = goal_position
        self.all_players = all_players
        self.players_my_team = players_my_team
        
    def action(self):
        self.suppressed = False
        r = rospy.Rate(10)
        msg = SSL()
        goal_angle = utils.pend(self.goal_position, self.player.getPosition())
        heading = abs(goal_angle - self.player.getAngle())
        distance = utils.dist(self.goal_position, self.player.getPosition())
        

        if (distance < 105):
            msg.cmd_vel.linear.x = 0
            msg.cmd_vel.angular.z = 0
            #no hago nada 
        else:
            if (heading < 0.3):
                msg.cmd_vel.linear.x = 0.75
                msg.cmd_vel.angular.z = 0
                #me muevo hacia delante 
            else:
                msg.cmd_vel.linear.x = 0
                msg.cmd_vel.angular.z = 0.75
                #roto hacia la izquierda

        try:
            self.player.getPublisher().publish(msg)
        except:
            print("exception")
        
    def suppress(self):
        print('suppress come')
        self.suppressed = True

    def check(self):
        print('Check go to the goal') 
        if not utils.they_have_the_ball(self.all_players,self.ball_position,105):
            player_near, _ = utils.get_player_have_ball(self.players_my_team,self.ball_position)
            print(player_near)
            ##me retorna el jugador que tiene la pelota
            if(player_near != None):
                player_near_goal, _ = utils.get_active_player(self.players_my_team,self.goal_position)
                #retorna el jugador de mi equipo  mas cercano al arco rival
                if(player_near.getId() == self.player.getId() and player_near_goal.getId() == self.player.getId()):
                    print('Entre al goToTheGoal', self.player.getId())
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False  