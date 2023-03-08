from rsk import Client, ClientRobot, constants
import numpy as np
from math import sqrt, atan

# All mesures are in meters
ROBOT_RADIUS = 0.09
BALL_RADIUS = 0.02
TEAM = "green"
X_MULT = 1 if TEAM == "green" else -1
DEFAULT_ANGLE = 0 if TEAM == "green" else np.pi
client = Client()

def main_loop():
    allies: dict[ClientRobot, ClientRobot] = client.robots[TEAM]
    ball = client.ball
    # Defensor move
    allies[0].goto((
        ((constants.field_width/2)-ROBOT_RADIUS)*X_MULT,
        max(min(ball[1], -constants.goal_virtual_height/2), constants.goal_virtual_height/2),
        DEFAULT_ANGLE
    ))

    # Attacker move
    # (attention giga thales incoming)
    # (feat pithagore)
    # (feat trigonometrie)
    pose = allies[1].pose
    pose[0] *= X_MULT
    rapport = sqrt(ball[0]**2 + ball[1]**2) + ROBOT_RADIUS + BALL_RADIUS
    destination = (
        ball[0] * rapport * X_MULT,
        -abs(ball[1] * rapport),
        atan(ball[1]/ball[0])
    )
    
    allies[1].goto(destination)


if __name__ == "__main__":
    client.on_update = main_loop