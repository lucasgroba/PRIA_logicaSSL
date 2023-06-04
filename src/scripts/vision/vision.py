


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

    print(data)
    if len(data.balls)> 0:
        ball_position['x'] = data.balls[0].x
        ball_position['y'] = data.balls[0].y