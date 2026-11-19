from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import PyavOutput
from datetime import datetime as dt
import time
import cv2
import numpy as np
import os

# Variables
pixel_thrs = 20
count_thrs = 500
motion_cooldown = 5 #seconds
image_capture = 0.5 #seconds

# Creating the camera and configuring
cam = Picamera2()
config = cam.create_video_configuration(main={"format": "YUV420"}, lores={"size": (640, 360), "format": "YUV420"})
cam.configure(config)
cam.start()

# Encoder and directory
encoder = H264Encoder()
if not os.path.isdir(f"video_recordings/{str(dt.now().strftime("%Y-%m-%d"))}"):
    os.makedirs(f"video_recordings/{str(dt.now().strftime("%Y-%m-%d"))}")

time.sleep(2) # 2 Second to allow the camera to warm up
cam_controls = cam.capture_metadata() # Captures the cam metadata after warm up for use below

control_dict= ({"AeEnable": False,
                "ExposureTime": cam_controls["ExposureTime"],
                "AnalogueGain": cam_controls["AnalogueGain"],
                "AwbEnable": False,
                "ColourGains": cam_controls["ColourGains"]})

cam.set_controls(control_dict)

running = True
filming = False
frame_1 = cam.capture_array("lores")
print(frame_1.shape)
height = int((frame_1.shape[0]/1.5))
frame_1 = cv2.GaussianBlur(frame_1[:height,:], (5,5), 0)
state = "No Motion Detected"
print("Camera Running")
while running:
    frame_2 = cam.capture_array("lores")
    frame_2 = cv2.GaussianBlur(frame_2[:height,:], (5,5), 0)

    difference = np.maximum(frame_1, frame_2) - np.minimum(frame_1, frame_2)
    frame_1 = frame_2

    if (difference > pixel_thrs).sum() > count_thrs:
        last_motion_time = time.time()
        if not filming:
            print("Starting Filming")
            start_time = dt.now()
            destination = f"/home/motioncam/motion_cam/video_recordings/{dt.now().strftime("%Y-%m-%d")}/\
            {dt.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4"
            output = PyavOutput(destination)
            filming = True
            cam.start_recording(encoder, output, quality=Quality.MEDIUM)
        
        #print(start_time)
    elif filming:
        if last_motion_time + motion_cooldown <= time.time():
            cam.stop_recording()
            print("Stopping Filming")
            print("Video Saved")
            filming = False

    time.sleep(image_capture)


