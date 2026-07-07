import cv2
import numpy as np
from GaussianBlur import apply_gaussian_blur 
from CNN import predict_emotion

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open")
    exit()

else:
#camera analyzing loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive")
            break
    
        #calling preprocessing function from GaussianBlur.py
        blurred_gray = apply_gaussian_blur(frame)
    
        #face recognition using Haar-Cascade
        faces = face_cascade.detectMultiScale(blurred_gray, scaleFactor=1.3, minNeighbors=5)
    
        #analyze and output
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_roi = blurred_gray[y:y+h, x:x+w]
            detected_emotion = predict_emotion(face_roi)
            cv2.putText(frame, detected_emotion, (x + 5, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Emotion: {detected_emotion} -> Choosing suitable song...")
        cv2.imshow('Camera Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
