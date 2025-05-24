import cv2
import numpy as np
import face_recognition
from datetime import datetime
import os
from database import get_all_face_encodings

# converting bgr format to rgb
def convert_bgr_to_rgb(frame):
    return cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


# code for drawing rectangle around the face
def draw_face_box(frame,box,name=None):
    top, right, bottom, left = box
    cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2) # draws box

    if name :
        cv2.putText(frame,name,(left,top-10), #prints name top-left corner
        cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,100,150),2)

def get_face_encodings(rgb_frame):
    boxes = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame,boxes)
    return boxes, encodings

def load_known_faces_from_db():
    data = get_all_face_encodings()
    known_encodings = []
    known_names = []

    for id, name, usn, face_encoding in data:
        encoding = np.frombuffer(face_encoding,dtype=np.float64)
        known_encodings.append(encoding)
        known_names.append(f"{name} {usn}")
    
    return known_encodings, known_names


def get_current_date_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%I:%M:%S:%p")


def show_success_message(name):
    import streamlit as st
    st.success(f"Attendance marked for {name}")


def show_error_message(msg):
    import streamlit as st
    st.error(f"❌ Error: {msg}")