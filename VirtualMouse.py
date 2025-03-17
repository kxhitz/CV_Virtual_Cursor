from pynput.mouse import Controller, Button
import cv2
import numpy as np
import HandTracking as htm
import time
import mediapipe as mp
import os
import subprocess

##########################
# Camera and tracking settings
wCam, hCam = 640, 480  # Camera resolution
frameR = 100  # Frame reduction for movement control
smoothening = 7  # Smoothing factor for mouse  movement
doubleClickThreshold = 0.5  # Time threshold for double click detection
eyeLockThreshold = 4  # Time threshold for locking the screen when eyes are not detected
pauseThreshold = 1   # Time threshold for pausing media when eyes are not detected
volumeSensitivity = 4  # Adjusts volume change sensitivity  (lower = more sensitive)
volumeChangeAmount = 10   # Volume change step
#########################

# Variables for tracking time and position
pTime = 0
plocX, plocY = 0, 0  # Previous mouse location
clocX, clocY = 0, 0  # Current mouse location
lastClickTime = 0  # Last click timestamp
lastEyeDetectedTime = time.time()  # Last time eyes were detected
mediaPaused = False  # Flag for media pause status

# Initialize mouse controller
mouse = Controller()

# Capture video from camera (change index if using a different camera)
cap = cv2.VideoCapture(2)
cap.set(3, wCam)
cap.set(4, hCam) 

# Initialize hand detector
detector = htm.handDetector(maxHands=1, detectionCon=0.7, trackCon=0.7)

# Initialize Face Mesh for facial landmark detection
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variable to track previous nose Y-coordinate for volume control
prev_nose_y = None


def toggle_media():
    """Simulates Play/Pause action on macOS using AppleScript."""
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 49'])  # Spacebar


def change_volume(direction):
    """Changes system volume on macOS using AppleScript."""
    if direction == "up":
        subprocess.run(["osascript", "-e", f"set volume output volume (output volume of (get volume settings) + {volumeChangeAmount})"])
    else:
        subprocess.run(["osascript", "-e", f"set volume output volume (output volume of (get volume settings) - {volumeChangeAmount})"])


# Main loop for processing video frames
while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame. Check your camera connection.")
        break

    img = cv2.flip(img, 1)  # Flip the image horizontally
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert frame to RGB

    # Detect facial landmarks
    results = face_mesh.process(imgRGB)
    eye_detected = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            eye_detected = True
            lastEyeDetectedTime = time.time()  # Update last detected time

            # Get nose landmark (landmark 1 in MediaPipe Face Mesh)
            nose = face_landmarks.landmark[1]
            nose_y = int(nose.y * hCam)  # Convert to pixel coordinates

            # Adjust volume based on vertical head movement
            if prev_nose_y is not None:
                movement = nose_y - prev_nose_y

                if movement > volumeSensitivity:
                    print("Head moved down: Decreasing volume")
                    change_volume("down")

                elif movement < -volumeSensitivity:
                    print("Head moved up: Increasing volume")
                    change_volume("up")

            prev_nose_y = nose_y  # Update previous nose position

    # Lock screen if eyes are not detected for a certain duration
    if not eye_detected and (time.time() - lastEyeDetectedTime > eyeLockThreshold):
        print("No eyes detected! Locking screen...")
        os.system("pmset displaysl eepnow")

    # Pause media if eyes are not detected for a certain duration
    if not eye_detected and (time.time() - lastEyeDetectedTime > pauseThreshold):
        if not mediaPaused:
            print("No eyes detected! Pausing media...")
            toggle_media()
            mediaPaused = True

    # Resume media if eyes are detected again
    if eye_detected and mediaPaused:
        print("Eyes detected again! Resuming media...")
        toggle_media()
        mediaPaused = False

    # Detect hands and get landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Get index finger tip coordinates
        fingers = detector.fingersUp()  # Detect which fingers are up

        if len(fingers) >= 5:
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                          (255, 0, 255), 2)

            # Move mouse if index finger is up and middle finger is down
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, 1920))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, 1080))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                mouse.position = (clocX, clocY)

                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            # Left click when index and middle fingers are close together
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)

                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

                    currentTime = time.time()
                    if currentTime - lastClickTime < doubleClickThreshold:
                        mouse.click(Button.left, 2)  # Double click
                        lastClickTime = 0
                    else:
                        mouse.click(Button.left, 1)  # Single click
                        lastClickTime = currentTime

            # Right click when only the thumb is up
            if fingers[0] == 1 and sum(fingers[1:]) == 0:
                mouse.click(Button.right, 1)
                time.sleep(1)

            # Scroll down when ring finger is up
            if fingers[3] == 1 and fingers[4] == 0:
                mouse.scroll(0, -1)

            # Scroll up when pinky is up
            if fingers[4] == 1 and fingers[3] == 0:
                mouse.scroll(0, 1)

    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    # Display output frame
    cv2.imshow("Image", img)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()