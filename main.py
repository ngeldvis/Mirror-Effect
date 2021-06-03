import cv2 as cv
import numpy as np

# keep track of the most recent mouse position after the user clicked their left mouse button
class MousePosition():

    def __init__(self, x: int) -> None:
        self.pos = x

    def get_mouse_position(self, event, x: int, y: int, flags, params) -> None:
        # Left Mouse Button Clicked
        if event == cv.EVENT_LBUTTONDOWN:
            self.pos = x


# release the video capture device and close all windows
def cleanup(capture: cv.VideoCapture) -> None:
    capture.release()
    cv.destroyAllWindows()


# returns the frame but flipped over the given axis
def get_argmented_img(frame: np.ndarray, w: int, h: int, x: int) -> np.ndarray:
    # create an empty frame
    img = np.zeros((h, w, 3), np.uint8)

    # check which side of the screen the user most recently clicked on
    left = True if x > w // 2 else False
    if left: # flipping the left side onto the right side
        img[0:h, 0:x] = frame[0:h, 0:x]
        img[0:h, x:w] = np.flip(frame[0:h, 2*x-w:x], 1)
    else: # flipping the right side onto the left side
        img[0:h, x:w] = frame[0:h, x:w]
        img[0:h, 0:x] = np.flip(frame[0:h, x:x*2], 1)

    return img


# main function
def main() -> None:
    
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)
    if not capture.isOpened():
        print("Cannot open camera")
        return

    width, height = int(capture.get(cv.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
    # set the initial axis position to half of the width of the screen
    mouse_position = MousePosition(width // 2)

    while True:
        # continuously grab the image from the capture device
        ret, frame = capture.read()
        if not ret:
            print("Can't receive frame")
            break

        # display the frame onto the window
        cv.imshow('frame', get_argmented_img(frame, width, height, mouse_position.pos))

        # check for any mouse click events
        cv.setMouseCallback('frame', mouse_position.get_mouse_position)

        # wait for either the 'q' check to be pressed or the X window button to be clicked to end the program
        if cv.waitKey(1) == ord('q') or cv.getWindowProperty('frame', cv.WND_PROP_AUTOSIZE) < 1:
            break

    # close all windows and free the capture device
    cleanup(capture)


if __name__ == '__main__':
    main()
