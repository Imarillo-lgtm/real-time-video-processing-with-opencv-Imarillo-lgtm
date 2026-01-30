import cv2
import os
import time

# --- Params ---
DITTO_DELAY = 5     # countdown before showing Ditto (in seconds)
DITTO_SCALE = 1.0   # scale of Ditto relative to face size

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DITTO_PATH = os.path.join(BASE_DIR, "data", "Ditto.png")

# --- Load Ditto ---
ditto = cv2.imread(DITTO_PATH, cv2.IMREAD_UNCHANGED)
if ditto is None:
    print("ERROR: WHERE IS DITTO???:", DITTO_PATH)
    exit()

# --- Face detection ---
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# --- Initialize camera ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()

face_detected_time = None  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    current_time = time.time()

    if len(faces) > 0:
        if face_detected_time is None:
            face_detected_time = current_time
    else:
        face_detected_time = None  # reset timer if no face

    for (x, y, w, h) in faces:
        remaining_time = 0
        if face_detected_time:
            remaining_time = max(0, int(DITTO_DELAY - (current_time - face_detected_time)))

        if face_detected_time and (current_time - face_detected_time >= DITTO_DELAY):
            # Show Ditto over face
            new_w = int(w * DITTO_SCALE)
            new_h = int(h * DITTO_SCALE)

            ditto_resized = cv2.resize(ditto, (new_w, new_h))
            
            y1 = y
            y2 = y + new_h
            x1 = x
            x2 = x + new_w

            alpha = ditto_resized[:, :, 3] / 255.0
            for c in range(3):
                frame[y1:y2, x1:x2, c] = (
                    alpha * ditto_resized[:, :, c] +
                    (1 - alpha) * frame[y1:y2, x1:x2, c]
                )
        else:
            # Show countdown
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                str(remaining_time),
                (x + 10, y + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3
            )

    cv2.imshow("Face → Ditto Countdown", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
