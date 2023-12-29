import time
import cv2
from threading import Thread

def detect_motion(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between frames
    frame_diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference image
    _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print("motion detection")
    # Check if any contour is detected
    return len(contours) > 0

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        if self.capture.isOpened():
            (self.status, self.frame) = self.capture.read()

        self.thread2 = Thread(target=self.show_frame, args=())
        self.thread2.daemon = True
        self.thread2.start()

    def update(self):
        frame1 = None
        frame2 = None
        # Read the next frame from the stream in a different thread
        while True:
            if self.thread.is_alive():
                print("thread 1 active")

            ret, frame = self.capture.read()
            if not ret:
                break

            if frame1 is None:
                frame1 = frame.copy()
                continue

            frame2 = frame1
            frame1 = frame.copy()

            if detect_motion(frame1, frame2):
                t = time.time()
                # timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(t))
                filename = f"C://Users//lik//Documents//Programmering//Camera_Project//Recordings//activity_{timestamp}.avi" #Literal String Interpolation
                
                # Create video writer object
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(filename, fourcc, 30.0, (frame.shape[1], frame.shape[0]))
                
                # Record video for a few seconds (you can change this duration)
                for _ in range(200):  #range = duration in amount of frames
                    ret, frame = self.capture.read()
                    if not ret:
                        break
                    out.write(frame)
                
                out.release()
                print(f"Activity detected! Video saved as {filename}")

    
    def show_frame(self):
        while(True):
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            # Display frames in main program
            cv2.imshow('frame', self.frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.capture.release()
                cv2.destroyAllWindows()
                exit(1)

def main():
    print("main called")

    try:
        while True:
            a = 10
    except KeyboardInterrupt:
        pass
        

if __name__ == "__main__":
    video_stream_widget = VideoStreamWidget()
    main()