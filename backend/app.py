from flask import Flask, Response, jsonify, render_template
import cv2
from flask_cors import CORS
import os
import sys

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
CORS(app)

# Load face cascade
try:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print(f"Face cascade loaded: {not face_cascade.empty()}")
except Exception as e:
    print(f"Error loading cascade: {e}")
    face_cascade = None

latest_coords = {"x": 0, "y": 0}


def generate_frames():
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    frame_id = 0
    faces = [] 
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame")
                break
            
            frame_id += 1
            
            if frame_id % 5 == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                small = cv2.resize(gray, None, fx=0.5, fy=0.5)
                detected = face_cascade.detectMultiScale(small, 1.2, 5)
                faces = [(x*2, y*2, w*2, h*2) for x,y,w,h in detected]
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(frame, (x+w//2, y+h//2), 5, (0, 0, 255), -1)
                global latest_coords
                latest_coords["x"] = int(x + w // 2)
                latest_coords["y"] = int(y + h // 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print(f"Error in generate_frames: {e}")
    finally:
        cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/coords')
def get_coords():
    print(f"Coords requested: {latest_coords}")
    return jsonify(latest_coords)

@app.route('/status')
def status():
    return jsonify({"status": "running", "coords": latest_coords})

if __name__ == "__main__":
    print("Starting Flask app...")
    print(f"OpenCV version: {cv2.__version__}")
    app.run(debug=True, port=5000, host='0.0.0.0')