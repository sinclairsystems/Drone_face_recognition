from djitellopy import Tello
import cv2

# Connect to Tello
tello = Tello()
tello.connect()

# Print battery level to ensure connection is established
print(f"Battery: {tello.get_battery()}%")

# Start video stream
tello.streamon()

# Start OpenCV window for video stream
cv2.namedWindow("Tello Video Stream")

try:
    while True:
        # Read a frame from the video stream
        frame = tello.get_frame_read().frame

        # Resize the frame (optional)
        frame = cv2.resize(frame, (640, 480))

        # Display the frame in the OpenCV window
        cv2.imshow("Tello Video Stream", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop video stream and close the OpenCV window
    tello.streamoff()
    cv2.destroyAllWindows()
