### Date: 3/1/2024 - 7/1/2024

### Changing motion detection function
research: 
<br>
https://docs.opencv.org/3.4/d1/dc5/tutorial_background_subtraction.html
<br>
https://learnopencv.com/background-subtraction-with-opencv-and-bgs-libraries/
<br>
https://pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/ . This one is basically what i am using in my script
#### Thoughts
On first glance this motion detection technique looks similar to what i am currently doing in my script, taking a frame and converting it to grayscale, then comparing it to an imput frame. Hovever, here we have a static picture that is constantly being compared to new frames from the camera feed. In comparison i dont have a static picture and am constantly comparing between just two consecutive frames, hence why my threshold is so low. I think this technique(Background subtraction) will help in making my script more accurate. 
<br>
I still want to keep the core functionality of my script where i utilize two cores and have an output to a GUI window, but i will see if that will be possible while i try to implement this functionallity. I may as well add a box in the video feed of what gets detected if possible.

### Results
In the process of improving the motion detection function i added more functionalities and imporovements. 

1. Config file. The script now has a config file for fine tuning the motion detection parameters and duration of the video capture as well as the path for the recordings
The config file utilizes the built in python library configparser.
2. Threading is now handled more carefully and each thread is executed and instantiated in different dunctions. I have also added a stop function for the threads.
Each thread still starts in _init_ but has its own function. A stop_threads function is also called upon program close that uses a flag in each threaded function. 
Previously if was just while(True) and now it is while self.is_running
3. The script now stops on exiting the tkinter window.
This is handled by using a function in the tkinter library called protocol that then calls my stop_threads function and closes the tkinter root.

```Python
    def on_closing():
        video_stream_widget.stop_threads()  # Call the method to stop threads and release resources
        root.destroy()  # Close the Tkinter window

    # Bind the on_closing function to the window's close event
    root.protocol("WM_DELETE_WINDOW", on_closing)
```

#### Better motion detection
The motion detection now uses background subtraction with a built in function from openCV called BackgroundSubtractorMOG2, witch is a Gaussian Mixture-based Background/Foreground Segmentation Algorithm. 
<br>
I have found this method more reliable than the one i used before and it can be fine tuned using different parameters. 
1. History: The number of frames used to build the background model
2. varThreshold: Returns the variance threshold for the pixel-model match.
3. detectShadows: Whether or not shadows are detected
4. Amount of contours required to trigger as motion detected

The function now only takes one frame and the Background Subtractor class as parameters, this removed the need for the fix i created regarding double recordings. However, the recorded footage is now a slight bit sped up and i have not found the cause for it yet. It is not a frame rate mismatch and it has nothing to do with the video codec. My guess is that it has to do with thread execution speeds so i will leave it as is for the time being. 
