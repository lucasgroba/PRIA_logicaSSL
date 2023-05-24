#!/usr/bin/env python3
import numpy as np

# Definir el entorno y las acciones posibles
num_players = 5
num_actions = 6  # Ejemplo: arriba, abajo, izquierda, derecha,patear, esquivar

# Inicializar las tablas Q1 y Q2 con valores arbitrarios o aleatorios
Q1 = np.zeros((num_players, num_actions))
Q2 = np.zeros((num_players, num_actions))

# Definir los hiperparámetros del algoritmo Double Q-learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Exploración-Explotación

# Función para elegir una acción en función de la política epsilon-greedy
def choose_action(state,episode):
    epsilon = max(epsilon_min, epsilon_decay ** episode)

    if np.random.uniform(0, 1) < epsilon:
        # Acción aleatoria (exploración)
        action = np.random.randint(num_actions)
    else:
        # Acción según la política Q1 + Q2 (explotación)
        action = np.argmax(Q1[state] + Q2[state])
    return action

# Bucle principal de entrenamiento
num_episodes = 1000  # Número de episodios de entrenamiento
for episode in range(num_episodes):
    # Reiniciar el estado del entorno
    state = 0  # Ejemplo: estado inicial

    # Bucle para cada paso dentro del episodio
    while not done:
        # Elegir una acción
        action = choose_action(state,num_episodes)

        # Tomar la acción y obtener la siguiente observación y recompensa
        next_state, reward, done = env.step(action)

        # Actualizar Q1 o Q2 al azar
        if np.random.uniform(0, 1) < 0.5:
            Q1[state, action] += alpha * (reward + gamma * Q2[next_state, np.argmax(Q1[next_state])] - Q1[state, action])
        else:
            Q2[state, action] += alpha * (reward + gamma * Q1[next_state, np.argmax(Q2[next_state])] - Q2[state, action])

        # Actualizar el estado actual
        state = next_state

# Una vez que el entrenamiento haya finalizado, se puede utilizar la combinación de Q1 y Q2 para tomar decisiones en tiempo real



























import numpy as np

# Definir el entorno y las acciones posibles
num_players = 5
num_actions = 4  # Ejemplo: arriba, abajo, izquierda, derecha

# Inicializar la tabla Q con valores arbitrarios o aleatorios
Q = np.zeros((num_players, num_actions))

# Definir los hiperparámetros del algoritmo Q-learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Exploración-Explotación

epsilon_min = 0.01  # Valor mínimo de epsilon
epsilon_decay = 0.999  # Factor de decaimiento de epsilon

# Función para elegir una acción en función de la política epsilon-greedy
def choose_action(state, episode):
    epsilon = max(epsilon_min, epsilon_decay ** episode)

    if np.random.uniform(0, 1) < epsilon:
        # Acción aleatoria (exploración)
        action = np.random.randint(num_actions)
    else:
        # Acción según la política Q (explotación)
        action = np.argmax(Q[state])
    return action

# Bucle principal de entrenamiento
num_episodes = 1000  # Número de episodios de entrenamiento
for episode in range(num_episodes):
    # Reiniciar el estado del entorno
    state = 0  # Ejemplo: estado inicial

    # Bucle para cada paso dentro del episodio
    while not done:
        # Elegir una acción
        action = choose_action(state,num_episodes)

        # Tomar la acción y obtener la siguiente observación y recompensa
        next_state, reward, done = env.step(action)

        # Actualizar la tabla Q
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])

        # Actualizar el estado actual
        state = next_state
