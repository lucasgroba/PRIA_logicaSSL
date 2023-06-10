#!/usr/bin/env python3

from math import sqrt, asin, atan2
import numpy as np


dist = lambda a,b: sqrt((a['x']-b['x'])**2+(a['y']-b['y'])**2)
pend = lambda a,b: atan2((a['y']-b['y']),(a['x']-b['x']))

def get_closer_player(all_players, our_player, isRival = False):
# retorna cual es el jugador mas cercano a nuestro player

    if isRival:
        players = [item for item in all_players if item.get_team() == 'yellow']
    else:
        players = [item for item in all_players if (item.get_team() == 'blue' and item.get_role() != our_player.get_role())]

    n = len(players)
    distances = []
    for i in range(n):
        distances.append(dist(players[i].getPosition(),our_player.getPosition()))
    np_distances = np.array(distances)

    index = np_distances.argmin()
    closer_player = players[index]
    distance = np_distances.min()

    return [closer_player, distance]


def calculate_distance_matrix(data):
    #calculo matris de distancias
    n = len(data)
    dist_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(i, n):
            dist_matrix[i,j] = dist(data[i],data[j])
            dist_matrix[j,i] = dist_matrix[i,j]

    return dist_matrix

def ball_player_min_distance(our_players, ball_position):
#retorno mi jugador mas cercano a la pelota
    n = len(our_players)
    distances = []
    for i in range(n):
        distances.append(dist(our_players[i],ball_position))
    np_distances = np.array(distances)

    return [np_distances.argmin(), np_distances.min()]

def they_have_the_ball(all_players, ball_position, gap_player_ball):
# retorna si el equipo rival tiene la pelota
    n = len(all_players)
    distances = []
    for i in range(n):
        distances.append(dist(all_players[i].getPosition(),ball_position))
    np_distances = np.array(distances)

    distance = np_distances.min()

    closer_player = all_players[np_distances.argmin()]

    if closer_player.getTeam() != 'blue':
        if distance <= gap_player_ball:
            return True

    return False



def get_angle_player_object(player_position, object_position, initial_angle):
## retorna diferencia angular entre un jugador y un objeto
    angle = pend(player_position, object_position)

    return angle - initial_angle

def get_distance_player_object(player_position, object_position):
    ## retorna distancia entre un jugador y un objeto
    return dist(player_position, object_position)

def get_active_player(players, ball_position):
    #soy el jugador mas cercano

    our_players_positions = [item.getPosition() for item in players]
    index_player, distance_player_ball = ball_player_min_distance(our_players_positions, ball_position)

    closer_player = players[index_player]

    return [closer_player, distance_player_ball]

    #if closer_player.ball_is_in_area(ball_position):
        # si la pelota esta en Area del player mas cercano, se activa
        #return [closer_player, distance_player_ball]
    #else:
        # sino, sigo con el siguiente jugador mas cercano
        #del players[index_player]
        #return get_active_player(players, ball_position)
    