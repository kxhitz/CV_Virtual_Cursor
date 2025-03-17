# CV_Virtual_Cursor

## Topic : Virtual Cursor using Hand and Eye Detection

Aim : To develop a computer vision-based gesture recognition system that enables users to control a
virtual cursor using hand and eye movements, enhancing human-computer interaction.

**Short Summary :**

1. This project allows users to control their computer’s mouse, media playback, and volume using hand gestures and face tracking. It uses OpenCV, MediaPipe, and pynput to detect hand movements, facial landmarks, and simulate keyboard/mouse actions.
   
**2. Functionalities & Their Implementation**
   
      Move the mouse using the index finger.
   
      Left-click when index & middle fingers are close together.

      Double Click Fast repeated clicks when fingers are close.
   
      Right-click when only the thumb is up.
   
      Scroll up/down using the pinky and ring fingers.

      Adjust volume based on head movement (nose Y-coordinate).
   
      Pause media if eyes are not detected for a certain time.
   
      Sleep the screen if eyes are not detected for too long.
   
**3. Requirements**
   
      OpenCV (cv2)
   
      MediaPipe (mediapipe)
   
      pynput (pynput.mouse)
   
      NumPy (numpy)

**4. Applications**

      Gaming and Virtual Reality (VR)

      Augmented Reality (AR) and Smart Displays

      Assistive Technology

      Security and Authentication
