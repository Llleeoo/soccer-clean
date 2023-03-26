from rsk import Client, constants
import rsk
import numpy as np
from math import sqrt, atan
#from time import time

# All mesures are in meters
COOLDOWN = 1000
ROBOT_RADIUS = 0.08
BALL_RADIUS = 0.01
TEAM = "blue"
SIDE = 1
#Vers négatif = 0; vers positif = 1 !!!!!!!!!
X_MULT = 1 if SIDE == 0 else -1
DEFAULT_ANGLE = 0 if SIDE == 1 else np.pi
client = Client(host="192.168.0.100", key="azert")

#last_kick_zero = time()

def main_loop():
    #global last_kick_zero

    allies = ()
    if TEAM == "blue":
        allies = (client.blue2, client.blue1)
    else:
        allies = (client.green2, client.green1)

    ball = client.ball

    # Defensor move
    allies[0].goto((
        0.93*X_MULT,
        max(min(ball[1], 0.30), -0.30),
        DEFAULT_ANGLE
    ), wait=False)
    """
    print(last_kick_zero)
    print(time())
    if last_kick_zero+COOLDOWN < time():
        allies[0].kick()
        last_kick_zero = time()
    """
    # Attacker move
    """
    pose = (ball[0]*X_MULT, ball[1])
    hypotenuse = sqrt((constants.field_length/2 - pose[0])**2 + pose[1]**2)
    rapport = hypotenuse / (hypotenuse + ROBOT_RADIUS + BALL_RADIUS)
    destination = (
        (constants.field_length - ((constants.field_length/2 - pose[0]) * rapport)) * X_MULT,
        pose[1] * rapport,
        atan(((constants.field_length/2 - pose[0])*X_MULT)/pose[1])
    )
    """
    bpr = (
            (ball[0]*X_MULT) - (1.83/2),
            ball[1]
            )
    de = bpr[1]
    eb = bpr[0]
    db = sqrt(de**2 + eb**2)
    ab = db + BALL_RADIUS + ROBOT_RADIUS
    cb = (eb * ab)/db
    ac = (de*cb)/eb
    beta = atan(ac/cb)
    destination = (
            (-((1.83/2) + cb)*(-X_MULT))-(0.15*-X_MULT),
            ac,
            (DEFAULT_ANGLE - beta)*X_MULT
            )

    pr = allies[1].pose
    if round(pr[0]*10) == round(destination[0]*10) and round(pr[1]*100) == round(destination[1]*100):
        allies[1].kick()
        print("KICK KICK KICK KICK KICK KICK KICK KICK KICK KICK ZIZOUUUUUU !!!")

    """
    # If destination is in left or right defense area (extended) OR destination exceed y limit, go in front of our goal
    if (abs(destination[0]) > (constants.field_length/2) - ROBOT_RADIUS - constants.defense_area_length) or (abs(destination[1] > constants.field_weight/2)):
        destination[0] = -((constants.field_length/2) - ROBOT_RADIUS - constants.defense_area_length)*X_MULT
        destination[1] = 0
    """

    allies[1].goto(destination, wait=False)

def safe_main():
    try:
        main_loop()
    except:
        print("Error when main loop")

if __name__ == "__main__":
    while True:
        safe_main()
    #client.on_update = safe_main
