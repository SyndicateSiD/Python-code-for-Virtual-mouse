import mediapipe as mp
import cv2
import numpy as np
import win32api
import pyautogui


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
click_count = 0

video = cv2.VideoCapture(0)

# Set up MediaPipe Hands model with confidence thresholds
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands: 
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        image_height, image_width, _ = image.shape

        # Process the hand landmarks
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
        # Draw hand landmarks and connections if detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))

        # Perform mouse click action based on hand gestures
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                index_fingertip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                index_fingertip_x = int(index_fingertip.x * image_width)
                index_fingertip_y = int(index_fingertip.y * image_height)
                thumb_tip_x = int(thumb_tip.x * image_width)
                thumb_tip_y = int(thumb_tip.y * image_height)

                # Move mouse cursor to index fingertip position
                win32api.SetCursorPos((index_fingertip_x * 4, index_fingertip_y * 5))

                # Calculate distance between index fingertip and thumb tip
                distance_x = abs(index_fingertip_x - thumb_tip_x)
                distance_y = abs(index_fingertip_y - thumb_tip_y)

                # Perform mouse click action if distance is within threshold
                if distance_x < 5 and distance_y < 5:
                    click_count += 1
                    if click_count % 5 == 0:
                        print("Single click")
                        pyautogui.click()

        cv2.imshow('Hand Tracking', image)
 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
