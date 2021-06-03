import cv2 as cv
import numpy as np


def terminate_windows(capture: cv.VideoCapture) -> None:
    capture.release()
    cv.destroyAllWindows()



def main() -> None:
    
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)

    while True:
        ret, frame = capture.read()
        if not ret:
            print('Could not capture video')

        cv.imshow('frame', frame)

        if cv.getWindowProperty('frame', cv.WND_PROP_AUTOSIZE) < 1:        
            break  

    terminate_windows(capture)   

if __name__ == '__main__':
    main()