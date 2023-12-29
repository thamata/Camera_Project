import time, cv2
from tkinter import *
from threading import Thread
from PIL import Image, ImageTk 

root = Tk()

label_video = Label(root)
label_text = Label(root)
label_text2 = Label(root)
label_text.pack(pady=10)
label_video.pack(padx=50,pady=20)
label_text2.pack(pady=10)

def detect_motion(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between frames
    frame_diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference image
    _, thresh = cv2.threshold(frame_diff, 180, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour is detected
    return len(contours) > 0

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        # Start thread to read frames from video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        # Start thread to display frames form video feed
        self.thread2 = Thread(target=self.show_frame, args=())
        self.thread2.daemon = True
        self.thread2.start()

    def update(self):
        frame1 = None
        frame2 = None

        while(True):
            label_text.configure(text="Camera Online")
            ret, frame = self.capture.read()
            if not ret:
                break

            # Set frame1 to be first frame in sequence
            if frame1 is None:
                frame1 = frame.copy()
                continue

            # Set frame2 as previous frame1 and frame1 is set to current frame
            frame2 = frame1
            frame1 = frame.copy()

            if detect_motion(frame1, frame2):
                t = time.time()
                timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(t))
                filename = f"C://Users//lik//Documents//Programmering//Camera_Project//Recordings//activity_{timestamp}.avi"
                # print("Activity detected!")
                
                # Create video writer object
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(filename, fourcc, 30.0, (frame.shape[1], frame.shape[0]))
                
                for _ in range(150): 
                    ret, frame = self.capture.read()
                    if not ret:
                        break
                    out.write(frame)
                    label_text.configure(text="Recording")
                
                out.release()
                frame1 = None
                label_text2.configure(text=f"Video saved as {filename}")
                # print(f"Video saved as {filename}")

    
    def show_frame(self):
        while(True):
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = Image.fromarray(self.frame)
            self.frame = ImageTk.PhotoImage(self.frame)
            label_video.configure(image=self.frame)
            label_video.image = self.frame

            '''
            # Display frames in main program
            cv2.imshow('frame', self.frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.capture.release()
                cv2.destroyAllWindows()
            '''

def main():
    try:
        while True:
            root.mainloop()
    except KeyboardInterrupt:
        pass
        

if __name__ == "__main__":
    video_stream_widget = VideoStreamWidget()
    main()