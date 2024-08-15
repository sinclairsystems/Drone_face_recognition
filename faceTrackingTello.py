from utlis import *
import cv2

w, h = 360, 240
pid_yaw = [0.8, 0.8, 0]  # Yaw PID coefficients for left-right movement
pid_up_down = [0.4, 0.4, 0]  # PID coefficients for up-down movement
pError_yaw = 0
pError_up_down = 0
startCounter = 0  # for no Flight 1 - for flight 0

myDrone = initializeTello()

# Print battery level
battery_level = myDrone.get_battery()
print(f"Battery Level: {battery_level}%")

while True:

    ## Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    ## Step 1
    img = telloGetFrame(myDrone, w, h)
    
    ## Convert BGR to RGB for correct color display
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    ## Step 2
    img, info = findFace(img)
    
    # Determine the face position and size
    cx, cy = info[0]
    area = info[1]
    
    ## Step 3: Yaw Movement (Left-Right)
    pError_yaw = trackFace(myDrone, info, w, pid_yaw, pError_yaw)
    
    ## Step 4: Up-Down Movement
    if cy != 0:
        error_up_down = h // 2 - cy  # Calculate vertical error
        speed_up_down = pid_up_down[0] * error_up_down + pid_up_down[1] * (error_up_down - pError_up_down)
        speed_up_down = int(np.clip(speed_up_down, -100, 100))
        
        # Check if the drone should move up or down
        if area < 6500:  # Threshold to avoid getting closer than 1 meter
            myDrone.up_down_velocity = speed_up_down
        else:
            myDrone.up_down_velocity = 0
        
        pError_up_down = error_up_down
    else:
        myDrone.up_down_velocity = 0
        pError_up_down = 0
    
    # Send the command to the drone
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    
    # Display the image
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
