import cv2
import face_recognition
import os
import numpy as np

def register_face(name, roll_number):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open webcam")
        return

    encodings = []

    while len(encodings) < 5:
        ret, frame = cam.read()
        print("Frame captured:", ret)
        if not ret:
            print("Failed to grab frame")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        print(f"Faces found: {len(boxes)}")

        if boxes:
            encoding = face_recognition.face_encodings(rgb, boxes)[0]
            encodings.append(encoding)
            print(f"Captured encoding {len(encodings)}")

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting on user request")
            break

    cam.release()
    cv2.destroyAllWindows()

    if len(encodings) > 0:
        os.makedirs("faces", exist_ok=True)
        np.save(f"faces/{roll_number}_{name}.npy", np.array(encodings))
        print("Face registered successfully.")
    else:
        print("No faces registered.")


if __name__ == "__main__":
    name = input("Enter your name: ")
    roll_number = input("Enter your roll number: ")
    register_face(name, roll_number)
