from rsk import Client, ClientRobot, constants
import numpy as np
from math import sqrt, tan, cos, sin

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
        max(min(ball[1], constants.goal_virtual_height/2), -constants.goal_virtual_height/2),
        DEFAULT_ANGLE
    ))

    # Attacker move
    pose = allies[1].pose
    Y_MULT = 1 if pose[1]>= 0 else -1
    rapport = sqrt((constants.field_length/2 - ball[0]) ** 2 + ball[1] ** 2) + ROBOT_RADIUS + BALL_RADIUS if X_MULT == 1 else sqrt((constants.field_length/2 + ball[0]) ** 2 + ball[1] ** 2) + ROBOT_RADIUS + BALL_RADIUS
    angle = tan(ball[1] ** 2 / (constants.field_length/2 - ball[0]) ** 2) if X_MULT == 1 else tan(ball[1] ** 2 / (constants.field_length/2 + ball[0]) ** 2)
    destination = (
        rapport * cos(angle) * X_MULT,
        rapport * sin(angle) * Y_MULT,
        angle * np.pi / 180 * -Y_MULT
    )
    
     # If destination is in left or right defense area (extended) OR destination exceed y limit, go in front of our goal
    if (abs(destination[0]) > (constants.field_length/2) - ROBOT_RADIUS - constants.defense_area_length) or (abs(destination[1] > constants.field_weight/2)):
        destination[0] = -((constants.field_length/2) - ROBOT_RADIUS - constants.defense_area_length)*X_MULT
        destination[1] = 0

    allies[1].goto(destination)

        pr = allies[1].pose
    if round(pr[0]*100) == round(destination[0]*100) and round(pr[1]*100) == round(destination[1]*100) and round(pr[3]*10) == round(destination[0]*10):
        allies[1].kick()

if __name__ == "__main__":
    client.on_update = main_loop
