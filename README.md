# Motion Camera Project

Motion Camera which records when movement is detected, with a tuneable cooldown window of five seconds by default

All detection carried out on device via array comparison with tuneable thresholds

## Hardware
- Raspberry Pi OS Lite 64-bit
- Pi Zero 2 W
- Pi Camera Module 3
- 3D printed casing

## How it works
The camera module provides a main stream and low resolution stream, the detection logic takes a low resolution stream array frame every 0.25 seconds (tuneable parameter) in YUV format, slicing only the Y section of the output and blurring it, then comparing the difference to the previous frame. Frames are dropped after use so that only two are held in memory. Motion is detected by counting the number of pixels which register a brightness change of a certain amount. The number of pixels which register the change, `count_thrs`, is by default set to 500. The brightness change, `pixel_thrs`, is by default set to 20. On detection of motion, video is captured via the main stream and saved to device. Files are organised by date and time of capture.

## Running
- Run `capture.py` for main loop and recording. 
- System requires numpy, picamera2 and OpenCV packages via:
```
sudo apt install python3-numpy python3-picamera2 python3-opencv
```

## Start on boot 
Place `mocam.service` in `/etc/systemd/system` and run the following to enable start on boot and begin running in current session:
```
sudo systemctl daemon-reload
sudo systemctl enable mocam 
sudo systemctl start mocam  
```


## Repository layout
- Comparison logic contained within `detector.py`
- Camera stream and main loop within `capture.py`
- `mocam.service` unit file contains system information for run on boot

## Design notes
- mp4 output via `PyavOutput` rather than .h264 so that it is immediately playable for the user.
- Continually analyses a low resolution stream for motion rather than still images to prevent need for the camera to switch operations on detection of motion.
- Low resolution stream output in YUV420 rather than outputting in RGB and then conversion to greyscale.
- Difference taken as the larger pixel value minus the smaller, rather than plain
subtraction, to avoid wraparound errors on unsigned 8-bit values.
- Blurred images before comparison to smooth out anomalous recordings and prevent false detections.
- Exposure and white balance locked after camera settles to prevent auto adjustments registering as motion.
- Detection logic kept in separate script to allow testing without camera hardware.

## Limitations
- Exposure and white balance lock could cause issues if the camera is run for a long time and light conditions change. This could be amended by having the exposure and white balance checked periodically.
- Videos currently kept on device meaning the user has to access the system via SSH to view recordings.
- Video is currently lost if stream cut during recording.

## Next steps
- Introduce pre-roll recording to grab the frames prior to motion starting rather than the current which starts after motion has been detected.
- Region masking.
- Storage management, deleting old footage, etc.
- Implement object identification and email notifications for the user. 
- Introduce a basic Visual-Language Model (VLM) to provide a description of the video to the user. 
- Split the work between the Pi Zero 2 W and a Pi 5 with a Hailo AI Hat to offload AI processing while keeping data on device for privacy.






