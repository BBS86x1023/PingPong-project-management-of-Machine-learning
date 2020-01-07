"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pickle
import time
import os
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
    ball_vx = []
    ball_vy = []
    list_platform_center_x = []
    list_ball_destination = []
    #print (time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())) 
    #file = open('save/'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+".pickle",'wb')
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        ball_position_history.append(scene_info.ball)
        platform_center_x = scene_info.platform_1P[0] + 20
        list_platform_center_x.append(platform_center_x)
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
        ball_vx.append(vx)
        ball_vy.append(vy)
        

        # 3.3 Put the code here to handle the scene information

        if ball_going_down == 1 :
            ball_destination = ball_position_history[-1][0] + ((415-ball_position_history[-1][1])/vy)*vx
            if ball_destination > 390:
                ball_destination = 195-(585-ball_destination)
            elif ball_destination < -195:
                ball_destination = 390 + ball_destination
            elif ball_destination > 195:
                ball_destination = 195-(ball_destination-195)
            elif ball_destination < 0:
                ball_destination = -ball_destination
#            print(ball_destination)
            ball_destination = round(abs(ball_destination))
            list_ball_destination.append(ball_destination)
        else :
            ball_destination = ball_position_history[-1][0] - ((ball_position_history[-1][1]+260)/vy)*vx
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
#            print(ball_destination)
            ball_destination = round(abs(ball_destination))
            list_ball_destination.append(ball_destination)
#"""            
        # 3.4. Send the instruction for this frame to the game process
        #ball_destination = ball_destination - ball_destination%5
#        print(ball_destination)
        if ball_going_down == 1 :            
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
        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
           scene_info.status == GameStatus.GAME_2P_WIN:
            # Do some updating or resetting stuff
            if scene_info.status == GameStatus.GAME_1P_WIN :
                print(len(ball_vx),len(ball_vy),len(list_platform_center_x),len(list_ball_destination),len(ball_position_history))
                ##字典
                pickle_data_dict = {'ball_vx':ball_vx,'ball_vy':ball_vy,'ball_destination':list_ball_destination,'platform_center_x':list_platform_center_x,'ball_position_history':ball_position_history}
                #print(pickle_data_dict['ball_destination'])
                print("紀錄1P玩家")
            ##-----------------------------存成pickle檔-------------------------------------------------##
                #print('紀錄1P玩家特徵')
                #file = open('save/'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+"_GAME_1P_WIN.pickle",'wb')
                #pickle.dump(pickle_data_dict, file)
                #file.close()
            ball_vx.clear()
            ball_vy.clear()
            list_ball_destination.clear()
            list_platform_center_x.clear()
            ball_position_history.clear()
            ##------------------------------------------------------------------------------------------##
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue
#        if ball_going_down == 0 :
#            if (platform_center_x + 5) < ball_destination :
#                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
#            elif (platform_center_x - 5) > ball_destination :
#                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
#            else:
#                comm.send_instruction(scene_info.frame, PlatformAction.NONE)