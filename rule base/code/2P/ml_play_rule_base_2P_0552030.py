"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
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
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        ball_position_history.append(scene_info.ball)
        platform_center_x = scene_info.platform_2P[0] + 20
        if (len(ball_position_history)) == 1 :
            ball_going_down = 1
            vx=7
            vy=7
        elif ball_position_history [-1][1] - ball_position_history [-2][1] < 0:
            ball_going_down = 0
            vy = ball_position_history[-1][1] - ball_position_history[-2][1]
            vx = ball_position_history[-1][0] - ball_position_history[-2][0]
            
        else:
            ball_going_down = 1
            vy = ball_position_history[-1][1] - ball_position_history[-2][1]
            vx = ball_position_history[-1][0] - ball_position_history[-2][0]

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
           scene_info.status == GameStatus.GAME_2P_WIN:
            # Do some updating or resetting stuff
            if scene_info.status == GameStatus.GAME_2P_WIN :
                print("紀錄2P玩家")
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        if ball_going_down == 0:
            ball_destination = ball_position_history[-1][0] - ((ball_position_history[-1][1]-80)/vy)*vx
            if ball_destination > 390:
                ball_destination = 195-(585-ball_destination)
            elif ball_destination < -195:
                ball_destination = 390 + ball_destination
            elif ball_destination > 195:
                ball_destination = 195-(ball_destination-195)
            elif ball_destination < 0:
                ball_destination = -ball_destination
        else :
            ball_destination = ball_position_history[-1][0] + ((760-ball_position_history[-1][1])/vy)*vx
            if ball_destination > 585:
                ball_destination = 780-ball_destination
            elif ball_destination < -390:
                ball_destination = 195-(585 + ball_destination)
            elif ball_destination > 390:
                ball_destination = 195-(585-ball_destination)
            elif ball_destination < -195:
                ball_destination = 390 + ball_destination
            elif ball_destination > 195:
                ball_destination = 195-(ball_destination-195)
            elif ball_destination < 0:
                ball_destination = -ball_destination

#"""            
        # 3.4. Send the instruction for this frame to the game process
        #ball_destination = ball_destination - ball_destination%5
        if ball_going_down == 0 :            
            if (platform_center_x) < ball_destination :
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif (platform_center_x) > ball_destination :
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        else :
            if (platform_center_x) < ball_destination :
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif (platform_center_x) > ball_destination :
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
#        if ball_going_down == 0 :
#            if (platform_center_x + 5) < ball_destination :
#                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
#            elif (platform_center_x - 5) > ball_destination :
#                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
#            else:
#                comm.send_instruction(scene_info.frame, PlatformAction.NONE)