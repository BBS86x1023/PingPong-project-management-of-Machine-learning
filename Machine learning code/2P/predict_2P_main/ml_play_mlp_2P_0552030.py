"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pickle
import time
import os
import numpy as np
import games.pingpong.communication as comm
from games.pingpong.communication import (
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop(side: str):
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_position_history = [ ]
    

    filename1="C:\\Users\\BBS\\Desktop\\game\\MLGame-master\
\\games\\pingpong\\ml\\mlp_model_2P_0552030_1.sav"

    model = pickle.load(open(filename1, 'rb'))
    print(model)
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        ball_position_history.append(scene_info.ball)
        platform_center_x = scene_info.platform_1P[0] + 20
        
        if (len(ball_position_history)) == 1 :
            ball_going_down = 0
            vx=7
            vy=7
        elif ball_position_history [-1][1] - ball_position_history [-2][1] > 0:
            ball_going_down = 1
            vy = ball_position_history[-1][1] - ball_position_history[-2][1]
            vx = ball_position_history[-1][0] - ball_position_history[-2][0]
            
        else:
            ball_going_down = 0
            vy = ball_position_history[-1][1] - ball_position_history[-2][1]
            vx = ball_position_history[-1][0] - ball_position_history[-2][0]
        
        

        # 3.3 Put the code here to handle the scene information

        inp_temp=np.array([scene_info.ball[0], scene_info.ball[1],scene_info.platform_1P[0] + 20,scene_info.platform_1P[1],
                           scene_info.platform_2P[0] + 20,scene_info.platform_2P[1] + 30,vx, vy])
        input=inp_temp[np.newaxis, :]
        #print(input)
        if(len(ball_position_history) > 1):
            move=model.predict(input)
        else:
            move = 0
        #print(move)
#"""            
        # 3.4. Send the instruction for this frame to the game process
        #ball_destination = ball_destination - ball_destination%5
#        print(ball_destination)


        if (move > 0.3) :
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif (move < -0.3)  :
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
#        
        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
           scene_info.status == GameStatus.GAME_2P_WIN:
            # Do some updating or resetting stuff
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            print(scene_info.ball_speed)
            comm.ml_ready()
            continue
