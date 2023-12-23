### Date: 23/12/2023

Added branching to the repository. Every devlog will now be a separate branch 1."nr of the devlog"
<br>
The code from todays devlog has been sourced from chatGPT. 
### Input
"using python and opencv write a program that will be used to minotor a door and record whenever there is any activity in the video feed"

### Output
```Python
import cv2
import numpy as np
from datetime import datetime

def detect_motion(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between frames
    frame_diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference image
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour is detected
    return len(contours) > 0

def main():
    cap = cv2.VideoCapture(0)  # Use default camera (change to file path if reading from a file)
    
    frame1 = None
    frame2 = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame1 is None:

            frame1 = frame.copy()
            continue

        frame2 = frame1
        frame1 = frame.copy()

        if detect_motion(frame1, frame2):
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"activity_{timestamp}.avi"
            
            # Create video writer object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            
            # Record video for a few seconds (you can change this duration)
            for _ in range(50):  # 50 frames at 20 fps = 2.5 seconds
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            
            out.release()
            print(f"Activity detected! Video saved as {filename}")

        cv2.imshow('Door Monitoring', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
```
### Results
Numpy is imported but never used so i remove it. I will retain the time library and not use datetime since it does not provide me with any benefits. 
<br>
I had already thought of a similar solution to use time for storing the video files since they get overwritten in the previous build, and it also helps with sorting and managing the video files since i plan to only store a certain amount in the future. Changes to timestamp:
```Python
t = time.time()

timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(t))
filename = f"activity_{timestamp}.avi" #Literal String Interpolation
```
The entirety of my previous code is replaced by a main function and a motion detection function. The code will now store two separate frames, one old and one new frame that gets overwritten as the program is running. These frames will then be used in the motion detection function to detect differences between the frames to ascertain when to store a recording. 
<br><br>
I noticed that the videos take up a lot less space now, i changed the codec back to 'MJPG' from 'XVID' and the file size increased again, this is explained in the openCV documentation as "XVID is more preferable. MJPG results in high size video. X264 gives very small size video".
<br><br>
Added path to folder for recordings in the filename. Folder will be ignored with a gitignore.
<br><br>
The program is now running fine, i had to tweak the threshold function to 50 instead of 25 as it was way too low, may need to change the value in the future as well. I also changed the framerate to 30 from 20 and the amount of frames captured to 200. The live feed is unusable as it is delayed and runs on a very low framerate, the motion detection is ran twice every time it detects something and results in two output videos, one of the actual motion and one after. This might be fixed with a delay or a timer for how often a motion can be detected, ex. once/30s. As for the live feed i will have to dig a little deeper to find a fix, might have to do with it displaying only one frame?:
```Python
cv2.imshow('Door Monitoring', frame)
```
### ToDo
1. Make live feed usable.
2. Try to change resoulution
3. Fix double recording issue



