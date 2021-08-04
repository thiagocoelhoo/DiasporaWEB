import time
from datetime import datetime

import cv2


def camera_loop():
    cap = cv2.VideoCapture(0)
    interval = 5
    last = time.time()

    while True:
        ret, frame = cap.read()
        now = time.time()
        if  now - last >= interval:
            path = f"src/diaspora/myapp/static/camera_images/img-{datetime.now()}.png"
            cv2.imwrite(filename=path, img=frame)
            last = now
            print('saved')


def streaming():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()        
        path = f"src/diaspora/myapp/static/camera_images/current_frame.png"
        cv2.imwrite(filename=path, img=frame)


if __name__ == '__main__':
    # camera_loop()
    streaming()