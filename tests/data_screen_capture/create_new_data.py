import time

from PIL import ImageGrab

while True:
    time.sleep(1)
    capture = ImageGrab.grab()
    capture.save(f"{time.ctime(time.time()).replace(':', '_')}.jpeg", format='JPEG')
