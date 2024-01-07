### Date: 

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
I still want to keep the core functionality of my script where i utilize two cores and have an output to a GUI window, but i will see if that will be possible while i try to implement this functionallity. I may as well add a box in the video feed of what gets detected. 

### Results
