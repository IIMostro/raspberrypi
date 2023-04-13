import time

import cv2
import face_recognition
import numpy as np


def show_video_stream(image_process=None):
    # Open the video stream
    cap = cv2.VideoCapture(0)
    known_face_encodings, known_face_names = image_face_init()
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if image_process is not None:
            frame = image_process(frame, known_face_encodings, known_face_names)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # cv2.imwrite("li.bowei.jpg", frame)
            break
        time.sleep(0.01)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def image_face_init():
    known_image = face_recognition.load_image_file("li.bowei.jpg")
    known_image_encoding = face_recognition.face_encodings(known_image)[0]
    known_face_encodings = [known_image_encoding]
    known_face_names = ["Li Bowei"]
    return known_face_encodings, known_face_names


def image_face_process(frame, known_face_encodings, known_face_names):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.3)
        name = "Unknown"
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame


if __name__ == '__main__':
    show_video_stream(image_face_process)
