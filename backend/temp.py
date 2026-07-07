import cv2
face_cascade=cv2.CascadeClassifier(
    cv2.data.haarcascades+
    "haarcascade_frontalface_default.xml"
)
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
frame_id=0
faces=[]
while True:
    ret,frame=cap.read()
    if not ret:
        break
    frame_id+=1
    gray=cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )
    if frame_id%5==0:
        small=cv2.resize(
            gray,
            None,
            fx=0.5,
            fy=0.5
        )
        faces=face_cascade.detectMultiScale(
            small,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(40,40)
        )
        faces=[
            (x*2,y*2,w*2,h*2)
            for x,y,w,h in faces
        ]
    for x,y,w,h in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.circle(frame,(x+w//2,y+h//2),5,(255,0,0),-1)
    cv2.imshow(
        "Camera",
        frame
    )
    if faces:
        print(f"X coordinate: {x+w//2}, Y coordinate: {y+h//2}")
    if cv2.waitKey(1)&0xff==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()