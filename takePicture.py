from picamera import PiCamera
import time, datetime

camera = PiCamera()

while (1):
	camera.start_preview(alpha=200)
	time.sleep(5)
	camera.capture('/home/pi/Desktop/image_' & datetime.datetime.Now() & '.jpg')
	camera.stop_preview()
	time.sleep(180)
