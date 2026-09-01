from djitellopy import Tello
import cv2
import time

# 1.To check battery before fligt
tello = Tello()
tello.connect()
print(f"Battery level before flight: {tello.get_battery()}%")

tello.streamon()
frame_read = tello.get_frame_read()

# 2. Take off
tello.takeoff()
time.sleep(2)  


# 3. Up 60 cm - climb to survey height

tello.move_up(60)
time.sleep(2)


# 4. Forward 100 cm - fly out along side A of the triangle

tello.move_forward(100)
time.sleep(2)

# 5. Take picture - capture the view at this far point of the triangle

cv2.imwrite("exp4_picture.png", frame_read.frame)
print("Picture saved as exp4_picture.png")

# 6. Right 80 cm then Back 100 cm
#    bringing the drone back toward its original position
tello.move_right(80)
time.sleep(2)
tello.move_back(100)
time.sleep(2)


# 7. Record video for 5 seconds
print("Recording video for 5 seconds...")
video_writer = cv2.VideoWriter(
    "exp4_video.avi",
    cv2.VideoWriter_fourcc(*"XVID"),
    30,
    (frame_read.frame.shape[1], frame_read.frame.shape[0])
)

start_time = time.time()
while time.time() - start_time < 5:
    video_writer.write(frame_read.frame)
    time.sleep(1 / 30)

video_writer.release()
print("Video saved as exp4_video.avi")

tello.enable_mission_pads()
pad_id = tello.get_mission_pad_id()
if pad_id == 7:
    tello.rotate_clockwise(360)

# 8. Down 60 cm
tello.move_down(60)
time.sleep(2)


# 9. Land 
tello.land()
print(f"Flight time: {tello.get_flight_time()} seconds")
print(f"Battery level after flight: {tello.get_battery()}%")


tello.streamoff()

