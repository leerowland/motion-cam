import time
import cv2
import os
import numpy as np
from datetime import datetime as dt
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import PyavOutput

# Variables
pixel_thrs = 20
count_thrs = 500
motion_cooldown = 5 #seconds
image_capture = 0.25 #seconds
directory = "/home/motioncam/motion_cam/video_recordings"

def make_directory():
    os.makedirs(f"{directory}/{dt.now().strftime('%Y-%m-%d')}", exist_ok=True)

# Creating the camera and configuring
cam = Picamera2()
config = cam.create_video_configuration(main={"format": "YUV420"}, lores={"size": (640, 360), "format": "YUV420"})
cam.configure(config)
try:
    cam.start()

    # Encoder and directory
    encoder = H264Encoder()
    make_directory()

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
    height = int((frame_1.shape[0]/1.5))
    frame_1 = cv2.GaussianBlur(frame_1[:height,:], (5,5), 0)
    print("Camera Running")
    while running:
        frame_2 = cam.capture_array("lores")
        frame_2 = cv2.GaussianBlur(frame_2[:height,:], (5,5), 0)
        difference = np.maximum(frame_1, frame_2) - np.minimum(frame_1, frame_2)
        frame_1 = frame_2

        if (difference > pixel_thrs).sum() > count_thrs:
            last_motion_time = time.time()
            if not filming:
                destination = (
                    f"{directory}/{dt.now().strftime('%Y-%m-%d')}/"
                    f"{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
                )
                make_directory()
                output = PyavOutput(destination)
                filming = True
                cam.start_encoder(encoder, output, quality=Quality.MEDIUM)
                print("Starting Filming")

        elif filming:
            if last_motion_time + motion_cooldown <= time.time():
                cam.stop_encoder()
                print("Stopping Filming")
                print("Video Saved")
                filming = False

        time.sleep(image_capture)
finally:
    if filming:
        cam.stop_encoder()
    cam.stop()
    print("  Camera Shutdown Correctly")
