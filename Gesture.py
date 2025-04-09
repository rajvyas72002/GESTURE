import cv2
import mediapipe as mp
import pyautogui
import time
import math
import webbrowser

import webbrowser

# Update this to your actual Chrome path
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# Register Chrome browser
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
cam.set(cv2.CAP_PROP_FRAME_WIDTH, screen_w)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_h)

hand_detector = mp.solutions.hands.Hands()

while True:
    _,frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

     # Hand detection
    hand_results = hand_detector.process(rgb_frame)

    frame_h, frame_w, _ = frame.shape


    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    frame_h,frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id,landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0, ))
            if id ==1:
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255,))
        if (left[0].y - left[1].y)  < 0.004:
            pyautogui.click()
            print('click')
            pyautogui.sleep(1)

            
    # === Hand Scroll Control ===
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[8]
            index_base = hand_landmarks.landmark[5]

            x_tip = int(index_tip.x * frame_w)
            y_tip = int(index_tip.y * frame_h)
            x_base = int(index_base.x * frame_w)
            y_base = int(index_base.y * frame_h)

            cv2.circle(frame, (x_tip, y_tip), 5, (255, 0, 0), -1)
            cv2.circle(frame, (x_base, y_base), 5, (0, 0, 255), -1)

            # Check for scroll gesture
            diff = y_base - y_tip
            if diff > 40:
                pyautogui.scroll(50)
                print("Scroll Up")
                time.sleep(0.3)
            elif diff < -40:
                pyautogui.scroll(-50)
                print("Scroll Down")
                time.sleep(0.3)

                # Zoom (Thumb + Index distance)
            thumb_tip = hand_landmarks.landmark[4]
            x_thumb = int(thumb_tip.x * frame_w)
            y_thumb = int(thumb_tip.y * frame_h)

            cv2.circle(frame, (x_thumb, y_thumb), 5, (0, 255, 255), -1)

            distance = math.hypot(x_tip - x_thumb, y_tip - y_thumb)

            if distance > 100:
                pyautogui.hotkey('ctrl', '+')
                print("Zoom In")
                time.sleep(0.5)
            elif distance < 40:
                pyautogui.hotkey('ctrl', '-')
                print("Zoom Out")
                time.sleep(0.5)

    if hand_results.multi_hand_landmarks and len(hand_results.multi_hand_landmarks) == 2:
        thumbs_up_count = 0
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Tip of thumb (4) and base of thumb (2)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_base = hand_landmarks.landmark[2]

            y_tip = int(thumb_tip.y * frame_h)
            y_base = int(thumb_base.y * frame_h)

            # Check if thumb is pointing up (tip is above base)
            if y_tip < y_base:
                thumbs_up_count += 1

        if thumbs_up_count == 2:
            print("👍 Both thumbs up detected! Playing song...")
            webbrowser.get('chrome').open_new_tab("https://www.youtube.com/watch?v=AETFvQonfV8")
            time.sleep(3)  # Prevent it from triggering repeatedly
           

                


    cv2.imshow('mouse',frame)
    cv2.waitKey(1)
