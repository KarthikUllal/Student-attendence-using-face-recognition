import cv2
import face_recognition
import os 
import numpy as np
from datetime import datetime
import pandas as pd
import time  # added for message timing

def recognize_and_mark():
    known_encodings = [] 
    known_names = [] 

    for file in os.listdir("faces"):
        data = np.load(f"faces/{file}")
        name = file.replace(".npy","")
        known_encodings.append(np.mean(data,axis=0))
        known_names.append(name)
    
    print(f"Loaded encodings: {len(known_encodings)}")
    print(f"Names: {known_names}")

    cam = cv2.VideoCapture(0)
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open webcam.")
        return

    attendance = set()
    last_marked_name = None  # track last marked name
    message_time = 0         # track when message was shown

    while True:
        f , frame = cam.read()
        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) # converts BGR formate of image into RGB so that it can be recoginized using face recog module
        boxes = face_recognition.face_locations(rgb) # boxes holds the co ordinates of the captured face
        encodings = face_recognition.face_encodings(rgb,boxes) #it stores encodings of captured image or frame

        for encoding in encodings :
            matches = face_recognition.compare_faces(known_encodings,encoding,tolerance=0.5) #compare registered encoding with currently captured one
            face_dist = face_recognition.face_distance(known_encodings,encoding)
            best_match = np.argmin(face_dist)

            if matches[best_match]:
                name = known_names[best_match]
                if name not in attendance :
                    mark_attendance(name)
                    attendance.add(name)
                    last_marked_name = name         # store name for message
                    message_time = time.time()      # store current time
                    print(f"{name} marked")         # keep your print

        # Show message for 3 seconds if face was matched
        if last_marked_name and time.time() - message_time < 3:
            cv2.putText(frame,f"{last_marked_name} marked successfully",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.imshow("Attedance",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

def mark_attendance(name):
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M;%S")

    if not os.path.exists("attedance.csv"):
        with open("attendance.csv","w") as f:
            f.write("Name \t,Date\t,Time\t\n")

    with open("attendance.csv","a") as f:
        f.write(f"{name}\t,{date_str}\t,{time_str}\t\n")  
    if f :
        print(f"{name}")       

if __name__ == "__main__":
    recognize_and_mark()
