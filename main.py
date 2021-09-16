import cv2 as cv
import numpy as np

class MousePosition():

    def __init__(self, x: int) -> None:
        self.pos = x

    def get_mouse_position(self, event, x: int, y: int, flags, params) -> None:
        if event == cv.EVENT_LBUTTONDOWN:
            self.pos = x


class VideoCaptureCM(cv.VideoCapture):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.release()


def get_augmented_img(frame: np.ndarray, w: int, h: int, x: int) -> np.ndarray:
    img = np.zeros((h, w, 3), np.uint8)
    left = True if x > w // 2 else False
    if left:
        img[0:h, 0:x] = frame[0:h, 0:x]
        img[0:h, x:w] = np.flip(frame[0:h, 2*x-w:x], 1)
    else:
        img[0:h, x:w] = frame[0:h, x:w]
        img[0:h, 0:x] = np.flip(frame[0:h, x:x*2], 1)
    return img
    

def main() -> None:

    with VideoCaptureCM(0, cv.CAP_DSHOW) as capture:
        
        if not capture.isOpened():
            print("Cannot open camera")
            return

        width, height = int(capture.get(cv.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
        mouse_position = MousePosition(width // 2)

        while True:
            ret, frame = capture.read()
            if not ret:
                print("Can't receive frame")
                break

            cv.imshow('frame', get_augmented_img(frame, width, height, mouse_position.pos))
            cv.setMouseCallback('frame', mouse_position.get_mouse_position)

            if cv.waitKey(1) == ord('q') or cv.getWindowProperty('frame', cv.WND_PROP_AUTOSIZE) < 1:
                break

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
