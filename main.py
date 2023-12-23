import time
import cv2
# from datetime import datetime

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

    # Check if any contour is detected
    return len(contours) > 0

def main():
    cap = cv2.VideoCapture(0)
    
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
            t = time.time()
            # timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(t))
            filename = f"E://Nackademin//Camera_Project//Recordings//activity_{timestamp}.avi" #Literal String Interpolation
            
            # Create video writer object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filename, fourcc, 30.0, (frame.shape[1], frame.shape[0]))
            
            # Record video for a few seconds (you can change this duration)
            for _ in range(200): 
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