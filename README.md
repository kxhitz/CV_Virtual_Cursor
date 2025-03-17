# CV_Virtual_Cursor

## Topic : Virtual Cursor using Hand and Eye Detection

Aim : To develop a computer vision-based gesture recognition system that enables users to control a
virtual cursor using hand and eye movements, enhancing human-computer interaction.

**Short Summary :**
1. This project allows users to control their computer’s mouse, media playback, and volume using hand gestures and face tracking. It uses OpenCV, MediaPipe, and pynput to detect hand movements, facial landmarks, and simulate keyboard/mouse actions.
**2. Features:**
   Hand Tracking for Mouse Control
   
   Face Tracking for Volume & Media Control
   
   Auto-Lock Screen When Eyes Are Not Detected
   
   Gesture-Based Scrolling & Clicking
   
   Dynamic FPS Display
   
**3. Functionalities & Their Implementation**
   
   Move the mouse using the index finger.
   
   Left-click when index & middle fingers are close together.
   
   Right-click when only the thumb is up.
   
   Scroll up/down using the pinky and ring fingers.

   Adjust volume based on head movement (nose Y-coordinate).
   
   Pause media if eyes are not detected for a certain time.
   
   Lock the screen if eyes are not detected for too long.

   Single Click: Bring index & middle fingers close together.
   
   Double Click: Fast repeated clicks when fingers are close.
   
   Scrolling: Pinky/Ring finger movement controls scroll.
   
**4. Requirements**
   
   OpenCV (cv2)
   
   MediaPipe (mediapipe)
   
   pynput (pynput.mouse)
   
   NumPy (numpy)
