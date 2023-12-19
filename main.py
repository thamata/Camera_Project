import time
import cv2

# Capture duration
duration = 10

cap = cv2.VideoCapture(0)

# Capture properties
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('U','Y','V','Y'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,100)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,100)

if (cap.isOpened()==False):
    print("Error reading video file")

Width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
Height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# VideoWriter will store output as .avi
result = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),30,(640,480))

start_time = time.time()

while(int(time.time()-start_time) < duration):
    ret,frame=cap.read()
    if ret==True:
        result.write(frame)
        cv2.imshow("OpenCVCam", frame)
        
        #Press Q to stop the process
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release video capture and write result
cap.release()
result.release()
cv2.destroyAllWindows()