from picamera2 import Picamera2
from datetime import datetime
import time

cam = Picamera2()
config = cam.create_still_configuration()
cam.configure(config)
cam.start()

time.sleep(2)

filename = f"/home/motioncam/motion_cam/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

cam.capture_file(filename)

print(f"Saved {filename}")
