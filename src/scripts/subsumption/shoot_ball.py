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
        
        self.player.setPublisher(rospy.Publisher("/robot_blue_"+self.player.getId()+"/cmd", SSL,queue_size=10))
        

        goal_angle = utils.pend(self.goal_position,self.player.getPosition())
        #obtengo pendiente entre el arco y el jugador 
        heading_goal = abs(goal_angle - self.player.getAngle())
        #obtengo la diferencia de orientecion ente arco y robot 
        distance_goal = utils.dist(self.goal_position,self.player.getPosition())
        #obtengo la distancia entre el arco y el jugador

        ball_angle = utils.pend(self.ball_position,self.player.getPosition())
        #obtengo pendiente entre la pelota y el jugador 
        heading_ball = abs(ball_angle - self.player.getAngle())
        #obtengo la diferencia de orientecion la pelota y el robot 
        distance_ball= utils.dist(self.ball_position,self.player.getPosition())
        #obtengo la distancia entre la pelota y el jugador

        print('action Shoot', goal_angle ,heading_goal,distance_goal,ball_angle,heading_ball,distance_ball)
        r = rospy.Rate(10)
        msg = SSL()
        msg.cmd_vel.linear.x = 0
        msg.cmd_vel.angular.z = 0
        msg.kicker = 100
        # if (abs(heading_ball - heading_goal)< 0.3 and distance_goal < 1900 and distance_ball < 103 and abs(goal_angle) < 15):
        #     msg.cmd_vel.linear.x = 0
        #     msg.cmd_vel.angular.z = 0
        #     msg.kicker = 100
        #     print('Patie ', self.player.getId())
        # else:
        #     print('Me acomodo para patear')
        #     if (goal_angle > 15):
        #         msg.cmd_vel.linear.x = 0
        #         msg.cmd_vel.angular.z = 0.50
        #         #roto hacia la izquierda
        #     elif(goal_angle < -15):
        #         msg.cmd_vel.linear.x = 0
        #         msg.cmd_vel.angular.z = -0.50
        #         #roto hacia la derecha

        self.player.getPublisher().publish(msg)
        
    def suppress(self):
        print('suppress shoot the ball')
        self.suppressed=True

    def check(self):
        print('Check shoot ball') 
        if not utils.they_have_the_ball(self.all_players,self.ball_position,105):
            player_near, distance_to_ball = utils.get_active_player(self.players_my_team,self.ball_position)
            ##me retorna el jugador que tiene la pelota
            if(player_near != None and distance_to_ball != None and distance_to_ball < 105):
                player_near_goal, distance_to_goal = utils.get_active_player(self.players_my_team,self.goal_position)
                #retorna el jugador de mi equipo  mas cercano al arco rival
                
                if(player_near.getId() == self.player.getId() and player_near_goal.getId() == self.player.getId() and distance_to_goal < 1700):
                    print('Entro al Action Shoot:', distance_to_goal, self.player.getId())
                    return True
                else:
                    return False
            else:
                return False 
        else:
            return False  