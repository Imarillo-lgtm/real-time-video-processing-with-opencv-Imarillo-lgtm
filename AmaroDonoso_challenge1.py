# openCV test-1
# Phase 1: iniciate webcam

# import cv2

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         break

#     cv2.imshow("Webcam", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# Phase 2: add grayscale, blur add edge detection.

import cv2

cap = cv2.VideoCapture(0)

mode = 0  

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo acceder a la cámara")
        break

    if mode == 1:
        output = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    elif mode == 2:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        output = cv2.GaussianBlur(gray, (7, 7), 0)

    elif mode == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        output = cv2.Canny(blur, 50, 150)

    else:
        output = frame

    cv2.imshow("Camera", output)

    
    key = cv2.waitKey(1) & 0xFF

    if key == ord('1'):
        mode = 1
        print("Mode: Grayscale")

    elif key == ord('2'):
        mode = 2
        print("Mode: Blur")

    elif key == ord('3'):
        mode = 3
        print("Mode: Edge Detection")

    elif key == ord('0'):
        mode = 0
        print("Mode: Original")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
