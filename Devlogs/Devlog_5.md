### Date: 29/12/2023

Code cleanup, changed threshold to 180 as changes in shadows triggered motion. 
#### Double recording issue
Setting sleep after motion detected does not fix issue. Setting variable to check if motion detected does not fix issue. Tried closing capture but that stops the live feed as well, cannot have 2 instances of VideoCapture utilising the same source. 
<br>
ISSUE FIXED: resetting frame1 after a recording has been saved fixed the issue of double recordings, my hypothesis is that it immediately compared frame2 from the past recording to the current frame1. By setting frame1 to None both frames are reset. 

#### Inaccurate timer
New issue is that the recording time is not 5s as i set it to be. If timer is set to 5s video ends up at 2s, timer 10s video 5s, timer 20s video 10s. The recording seems to cut my timer in half. Using fps gives accurate timer. Issue resolved. 
```Python

# Inaccurate using time class
while(int(time.time() - t) < 20):

# Range in amount of frames to record, video is 30fps
for _ in range(300): 
```

### GUI Buildup
I want the script to show a popup or text in the preview window when a video is being recorded, maybe add a timestamp as well. 
<br>
To write text on the live feed i need to add it to the frame before imshow() is called. I will instead use a pyhton library called tkinter. To get the frames to displat in tkinter i need to use another library called pillow. The frame from cv2 is then colour corrected and transformed into an image whitch can be displayed in the tkinter window. 
<br>
initial code from: https://www.geeksforgeeks.org/how-to-show-webcam-in-tkinter-window-python/
<br>
Video feed flickers but solved with: https://stackoverflow.com/questions/48364168/flickering-video-in-opencv-tkinter-integration
<br>
The script now opens a window and displays the live feed from cv2, window has two text boxes that display when the camera is recording and where the recordings go. 

### ToDo
1. Try to change motion detection to only include part of the video feed, current build too sensitive
2. Add more features to the GUI