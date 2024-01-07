import time, cv2, configparser
from tkinter import *
from threading import Thread
from PIL import Image, ImageTk 

# Read configuration from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve values from the configuration file
filepath = config.get('General', 'filepath')
min_thresh = config.getint('General', 'min_thresh')
bgs_history = config.getint('General', 'bgs_history')
recording_duration = config.getint('General', 'recording_duration')

root = Tk()

label_video = Label(root)
label_text = Label(root)
label_text2 = Label(root)
label_text.pack(pady=10)
label_video.pack(padx=50,pady=20)
label_text2.pack(pady=10)

def detect_motion(frame, background_subtractor):
    # Apply the background subtractor to get the foreground mask
    fg_mask = background_subtractor.apply(frame)

    # Remove noise by applying a series of morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours on the foreground mask
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour is detected
    for c in contours:
        if cv2.contourArea(c) > min_thresh: # Sensitivity adjustment
            return True

    return False

# Class to handle video streaming, motion detection, and recording
class VideoStreamWidget(object):
    def __init__(self, src=0):
        # Flag to check if the threads should keep running
        self.is_running = True
        # Instantiate video capture
        self.capture = cv2.VideoCapture(src)
        # Instantiate subtractor model
        self.bsm = cv2.createBackgroundSubtractorMOG2(history= bgs_history, varThreshold=50, detectShadows=False)

        # Start threads
        self.start_update_thread()
        self.start_show_frame_thread()

    def start_update_thread(self):
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def start_show_frame_thread(self):
        self.thread2 = Thread(target=self.show_frame, args=())
        self.thread2.daemon = True
        self.thread2.start()

    def stop_threads(self):
        self.is_running = False  # Set the flag to False to stop the threads
        self.capture.release()   # Release the video capture device if it's not already released


    def update(self):
        while self.is_running:
            label_text.configure(text="Camera Online")
            ret, frame = self.capture.read()
            if not ret:
                break

            if detect_motion(frame, self.bsm):
                t = time.time()
                timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(t))
                filename = f"{filepath}activity_{timestamp}.avi"
                # print("Activity detected!")
                
                # Create video writer object
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filename, fourcc, 30, (frame.shape[1], frame.shape[0]))
                
                for _ in range(recording_duration * 30): 
                    ret, frame = self.capture.read()
                    if not ret:
                        break
                    out.write(frame)
                    label_text.configure(text="Recording")
                
                out.release()
                label_text2.configure(text=f"Video saved as {filename}")
                # print(f"Video saved as {filename}")

    
    def show_frame(self):
        while self.is_running:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = Image.fromarray(self.frame)
            self.frame = ImageTk.PhotoImage(self.frame)

            label_video.configure(image=self.frame)
            label_video.image = self.frame

    def on_closing():
        video_stream_widget.stop_threads()  # Call the method to stop threads and release resources
        root.destroy()  # Close the Tkinter window

    # Bind the on_closing function to the window's close event
    root.protocol("WM_DELETE_WINDOW", on_closing)

def main():
    # Create an instance of VideoStreamWidget
    video_stream_widget = VideoStreamWidget()

    try:
        # Start the Tkinter event loop
        root.mainloop()
    except KeyboardInterrupt:
        # If KeyboardInterrupt (e.g., Ctrl+C) is detected, stop the threads gracefully
        video_stream_widget.stop_threads()
        

if __name__ == "__main__":
    video_stream_widget = VideoStreamWidget()
    try:
        root.mainloop()
    except KeyboardInterrupt:
        video_stream_widget.stop_threads()