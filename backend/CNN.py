import cv2
import numpy as np
from tensorflow.keras.models import load_model

#load file
model = load_model('emotion_cnn_model.keras')

#emotions list
EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

def predict_emotion(face_roi):
    if face_roi is None or face_roi.size == 0: 
        return "Neutral"
    
    #preprocess
    resized = cv2.resize(face_roi, (48, 48))
    normalized = resized / 255.0
    reshaped = np.reshape(normalized, (1, 48, 48, 1))
    
    #predict the emotion using the loaded model
    preds = model.predict(reshaped, verbose=0) 
    return EMOTIONS[np.argmax(preds)]