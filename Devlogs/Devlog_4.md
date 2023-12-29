### Date: 29/12/2023

Found the cause for live feed not working, i put print commands where the motion detection function ends and where the cv2.imshow displays a frame. 
When there is no movement the feed works without delay, but as soon as a motion is detected the feed is paused because cv2.imshow is not being called anymore. 

<br>
Trying to use threads to run the live feed. But running in to an issue where the main loop does not start after a thread is started.
Error is: https://stackoverflow.com/questions/63156943/opencv-cvcapture-msmfgrabframe-videoiomsmf-cant-grab-frame-error-214748

<br>
more research:
<br>
https://stackoverflow.com/questions/55099413/python-opencv-streaming-from-camera-multithreading-timestamps
https://realpython.com/intro-to-python-threading/
<br>
```Python
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
```

<br><br>
Finally realized that the video feed lags depending on where the .read call happens, i put the .read in the thread where the video gets displayed and the video is displayed without delay... but the motion detection stops working until i close that thread. This seems to be the case even when multithreadng as the video source is shared? The plus side to this is that i now get a single video output, hurray!
<br><br>
In the above code the show_frame function seems to have prio in the class as it defines self.frame with self.capture.read(). After putting a threadalive for the first thread i notice this: 
### cource of action in the program:
1. live feed is running and both threads are active
2. as soon as a motion is detected the .read in thread1 starts buffering and thread2 keeps running fine
3. after thread1 has finished reading it keeps on being active.
### Summary
What i thought was the program not responding was actually just the .read function buffering the frames. I now have a working live feed that records any movement, but the program needs to buffer the recording before it can detect movement again. 
### ToDo:
1. Fix double recording issue