import cv2
import face_recognition
import os 
import numpy as np
from datetime import datetime
import pandas as pd
import time  # added for message timing
import mysql.connector

def recognize_and_mark():
    known_encodings = [] 
    known_names = [] 

    for file in os.listdir("faces"):
        data = np.load(f"faces/{file}")
        name = file.replace(".npy","")  #only name is extracted . ex : 101_karthik.npy -> 101_karthik
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
        boxes = face_recognition.face_locations(rgb) # detects face location in frame
        encodings = face_recognition.face_encodings(rgb,boxes) #it stores encodings of each captured image or frame

        # for encoding in encodings :
        #     matches = face_recognition.compare_faces(known_encodings,encoding,tolerance=0.5) #compare registered encoding with currently captured one
        #     face_dist = face_recognition.face_distance(known_encodings,encoding)
        #     best_match = np.argmin(face_dist)

        #     if matches[best_match]:
        #         name = known_names[best_match]
        #         if name not in attendance:
        #             marked, msg = mark_attendance(name)
        #             last_marked_name = msg
        #             message_time = time.time()
        #             if marked:
        #                 attendance.add(name)
        #                 print(f"{name} marked")   
        for box, encoding in zip(boxes, encodings):
                top, right, bottom, left = box
            # Draw rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
                face_dist = face_recognition.face_distance(known_encodings, encoding)
                best_match = np.argmin(face_dist)

                if matches[best_match]:
                    name = known_names[best_match]
                    if name not in attendance:
                        marked, msg = mark_attendance(name)
                        last_marked_name = msg
                        message_time = time.time()
                        if marked:
                            attendance.add(name)
                            print(f"{name} marked")


        # Show message for 3 seconds if face was matched
        if last_marked_name and time.time() - message_time < 3:
            cv2.putText(frame, last_marked_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 150), 2)

        cv2.imshow("Attedance",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

def mark_attendance(full_name):
    roll_no, name = full_name.split("_")
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    # connecting to mysql server
    try:
        con = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "attendance_system" 
        )

        cursor = con.cursor()

        # To ensure there is no duplicate entries of same date
        query = "SELECT * FROM attendance WHERE rollno=%s AND date=%s" 
        cursor.execute(query, (roll_no, date_str))
        result = cursor.fetchone()

        if result:
            message = f"{name} ({roll_no}) already marked today"
            print(message)
            return False,message
        

        # if there is no entry then update the database by inserting record
        insert_query = "INSERT INTO attendance (rollno, name, date, time) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (roll_no, name, date_str, time_str))
        con.commit()

        message = f"{name} ({roll_no}) marked at {time_str}"
        print(message)
        return True, message
    
    except mysql.connector.Error as e:
        print("Database Error:", e)
        return False, "Error connecting to database"
    finally :
        cursor.close()
        con.close()
if __name__ == "__main__":
    recognize_and_mark()
