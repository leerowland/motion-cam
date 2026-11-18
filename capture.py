from picamera2 import Picamera2
from datetime import datetime
import time
import cv2
import numpy as np

# Creating the camera and configuring
cam = Picamera2()
config = cam.create_preview_configuration(main={"format": "YUV420"})
cam.configure(config)
cam.start()

time.sleep(2) # 2 Second to allow the camera to warm up
cam_controls = cam.capture_metadata()

control_dict= ({"AeEnable": False,
"ExposureTime": cam_controls["ExposureTime"],
"AnalogueGain": cam_controls["AnalogueGain"],
"AwbEnable": False,
"ColourGains": cam_controls["ColourGains"]})

cam.set_controls(control_dict)

running = True
frame_1 = cam.capture_array()
height = int((frame_1.shape[0]/1.5))
frame_1 = cv2.GaussianBlur(frame_1[:height,:], (5,5), 0)
while running:
    frame_2 = cam.capture_array()
    frame_2 = cv2.GaussianBlur(frame_2[:height,:], (5,5), 0)

    difference = np.maximum(frame_1, frame_2) - np.minimum(frame_1, frame_2)
    frame_1 = frame_2

    count_20 = (difference > 20).sum()
    count_30 = (difference > 30).sum()
    count_40 = (difference > 40).sum()
    count_50 = (difference > 50).sum()

    print(f">20={count_20}, >30={count_30}, >40={count_40}, >50={count_50}")
    time.sleep(2)


