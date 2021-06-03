import cv2 as cv
import numpy as np
from numpy.lib.shape_base import split


def event_handlers(event, x, y, flags, params):
    # Left Mouse Button Clicked
    if event == cv.EVENT_LBUTTONDOWN:
        print(x, y)


def cleanup(capture: cv.VideoCapture) -> None:
    capture.release()
    cv.destroyAllWindows()


def main() -> None:
    
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)
    
    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))

    split_x = int(0.5 * width)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Can't receive frame")
            break

        img = np.zeros((height, width, 3), np.uint8)

        img[0:height, 0:split_x] = frame[0:height, 0:split_x]
        img[0:height, split_x:width] = np.flip(frame[0:height, 0:split_x], 1)

        cv.imshow('frame', img)
        cv.setMouseCallback('frame', event_handlers)

        if cv.waitKey(1) == ord('q') or cv.getWindowProperty('frame', cv.WND_PROP_AUTOSIZE) < 1:
            break

    cleanup(capture)

if __name__ == '__main__':
    main()