"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
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

    frame_position_history=[]
    status_position_history=[]
    ball_position_history=[]
    ball_speed_position_history=[]    
    platform_1P_position_history=[]   
    platform_2P_position_history=[]    
    ball=[]
    
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.get_scene_info()
        frame_position_history.append( scene_info.frame)
        status_position_history.append( scene_info.status)
        ball_position_history.append( scene_info.ball)
        ball_speed_position_history.append( scene_info.ball_speed)        
        platform_1P_position_history.append( scene_info.platform_1P)
        platform_2P_position_history.append( scene_info.platform_2P)        
        #platform_center_x = scene_info.platform[0] + 20
        """
        if len(ball_position_history)==1:
            ball_going_down = 0
        elif ball_position_history[-1][1]-ball_position_history[-2][1]>0:
        """
        if len(ball_position_history)>1:
            #ball_going_down = 1
            vy=ball_position_history[-1][1]-ball_position_history[-2][1]
            vx=ball_position_history[-1][0]-ball_position_history[-2][0]
            ball_going_down = 0
            platform_1P_center_y=platform_1P_position_history[-1][1]-300
            platform_2P_center_y=platform_2P_position_history[-1][1]+330             
            platform_1P_center_x=platform_1P_position_history[-1][0]+20 
            platform_2P_center_x=platform_2P_position_history[-1][0]+20 
            plat_1P=np.array([platform_1P_center_x,platform_1P_center_y])
            input_1P=plat_1P[np.newaxis, :]
            plat_2P=np.array([platform_2P_center_x,platform_2P_center_y])
            input_2P=plat_2P[np.newaxis, :]
            if vy >0 :
                ball_going_down = 1
            else :   
                ball_going_down = 0
            #ball=np.array([vx,vy])
            #ball.append( (vx,vy))
            #print(ball_position_history[-1])
            #print(ball)
        #else: ball_going_down = 0 
            
            if side == "1P":           
                if ball_going_down == 1 and ball_position_history[-1][1]>=120:
                    ball_destination = ball_position_history[-1][0]+(((415-ball_position_history[-1][1])/vy)*vx)
                    #print(input_1P[-1][0])
                    #pp=3+vx/2
                    #px=(170//vx)
                    #print((((415-ball_position_history[-1][1])/vy)*vx))
                    if ball_destination>= 195:
                        ball_destination =195-(ball_destination-195)
                        #print("195")
                    elif ball_destination<=0:
                        ball_destination=-ball_destination
                        #print("0")
                    #else:
                       # ball_destination=platform_1P_center_x
                    #print(ball_destination)#print("B")
                    if platform_1P_center_x>ball_destination:
                        #print("L")
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_1P_center_x<ball_destination:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        #print("R")
                    
                #######平板位置回中
                if ball_going_down == 0 : 
                    state = "1p-c"
                    #print("1p-c")
                    if input_1P[-1][0] >100:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif input_1P[-1][0] <100: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)                    
                    
                    
                
                """
                if ball_position_history[-1][1] >350 :  
                    if platform_1P_position_history[-1][0]+20 < ball_position_history[-1][0]:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_1P_position_history[-1][0]+20 > ball_position_history[-1][0]: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    elif ball_position_history[-1][1] >350 and ball_position_history[-1][0] <30: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif ball_position_history[-1][1] >400 and ball_position_history[-1][0] <30: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)    
                elif ball[-1][1] < 1 : 
                    print("1p-c")
                    if platform_1P_position_history[-1][0]+20 >100:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_1P_position_history[-1][0]+20 <100: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                       
                #######平板位置回中
                elif ball[-1] < 1 :    
                    if platform_1P_position_history[-1][0]+20 >100:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_1P_position_history[-1][0]+20 <100: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        return
                #comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                """
            
            else:
                #######平板位置2#######
                
                #print("2P")
                if ball_going_down == 0 and ball_position_history[-1][1]<=380:
                    ball_destination = ball_position_history[-1][0]+(((ball_position_history[-1][1]-80)/-vy)*vx)
                   # print(input_2P[-1][0])
                    if ball_destination>= 195:
                        ball_destination =195-(ball_destination-195)
                    elif ball_destination<=0:
                        ball_destination=-ball_destination
            
                    #else:
                    #    ball_destination=platform_1P_center_x
                    #print((ball_position_history[-1][1]-80)//-vy)
                    if input_2P[-1][0]>ball_destination:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif input_2P[-1][0]<ball_destination:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)

                #######平板位置回中

                if ball_going_down == 1 : 
                    state = "2p-c"
                    #print("2p-c")
                    if platform_2P_center_x >100:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_2P_center_x <100: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)



                """
                if ball_position_history[-1][1] <250 :  
                    if platform_2P_position_history[-1][0]-40 > ball_position_history[-1][0]:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_2P_position_history[-1][0]-20 < ball_position_history[-1][0]: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT) 
                    elif ball_position_history[-1][1] <180 and ball_position_history[-1][0] <60: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif ball[-1][1] > 1 : 
                    print("2p-c")
                    if platform_2P_position_history[-1][0]+20 >100:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_2P_position_history[-1][0]+20 <100: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    
                
                elif ball[-1] > 1 :    
                    if platform_2P_position_history[-1][0]+20 >100:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_2P_position_history[-1][0]+20 <100: 
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)               

                    print("123")
                    if ball_position_history[-1][1] <120:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif ball_position_history[-1][1] <320:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)

                elif ball[-1] < 1 and ball_position_history[-1][0] <20:  
                    if ball_position_history[-1][1] >180:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif ball_position_history[-1][0] <20:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT) 

                    


                

      
                #######平板位置5#######
                elif ball[-1] < 1 and ball_position_history[-1][1] <250 and ball_position_history[-1][0] <100 :
                    return
                    if platform_2P_position_history[-1][0]+20 >180:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif platform_2P_position_history[-1][0]+20 <180:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)                
                           
                #######平板位置2#######
                elif ball[-1] < 1 and ball_position_history[-1][1] < 250:  
                    if vx > 1 and ball_position_history[-1][0] > 130 and ball_position_history[-1][0] < 180:
                        if platform_2P_position_history[-1][0]+20 >60:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif platform_2P_position_history[-1][0]+20 <60:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                            #return
                #######平板位置3#######               
                elif ball[-1] < 1 and ball_position_history[-1][1] < 250:   
                    if vx > 1 and ball_position_history[-1][0] > 70 and ball_position_history[-1][0] < 130:
                        if platform_2P_position_history[-1][0]+20 >100:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif platform_2P_position_history[-1][0]+20 <100:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                            #return 
                #######平板位置4#######
                elif ball[-1] < 1 and ball_position_history[-1][1] < 250: 
                    if vx > 1 and ball_position_history[-1][0] > 20 and ball_position_history[-1][0] < 70:
                        if platform_2P_position_history[-1][0]+20 >140:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        elif platform_2P_position_history[-1][0]+20 <140:
                            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                            #return 
                    #if vx > 1 and vx < 1 and ball_position_history[-1][0] <20 :
                """        
                #######平板位置回中


                
                


        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
            scene_info.status == GameStatus.GAME_2P_WIN:
            # Do some updating or resetting stuff
    
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue
        """
        # 3.3 Put the code here to handle the scene information
        
        if ball_going_down == 1 and ball_position_history[-1][1]>=0:
            ball_destination = ball_position_history[-1][0]+ ((395-ball_position_history[-1][1])/vy)*vx
            if ball_destination >= 195:
                ball_destination = 195-(ball_destination-195)
            elif ball_destination <= 0:
                ball_destination = - ball_destination
        else:
        """
        #   ball_destination = platform_center_x
        # 3.4 Send the instruction for this frame to the game process
        """
        if ball_position_history[-1][0] > 100 :
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        elif ball_position_history[-1][0] < 100 :    
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        """
        #else:
        #   comm.send_instruction(scene_info.frame, PlatformAction.MOVE_NONE)
            
        #vy=ball_position_history[-1][1]-ball_position_history[-2][1]
            #vx=ball_position_history[-1][0]-ball_position_history[-2][0]
        
        #print(ball_position_history[-1])
    