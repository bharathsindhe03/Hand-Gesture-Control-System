import cv2
import mediapipe as mp
import pyautogui
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_finger_status(hand_landmarks):
    finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                   mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                   mp_hands.HandLandmark.RING_FINGER_TIP,
                   mp_hands.HandLandmark.PINKY_TIP]
    
    thumb_tip = mp_hands.HandLandmark.THUMB_TIP
    thumb_ip = mp_hands.HandLandmark.THUMB_IP

    finger_status = [0, 0, 0, 0, 0]

    
    for i, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_status[i + 1] = 1
    
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_ip].x:
        finger_status[0] = 1

    return finger_status

def change_tab(next_tab=True):
    if next_tab:
        pyautogui.hotkey('ctrl', 'tab')
    else:
        pyautogui.hotkey('ctrl', 'shift', 'tab')

def close_tab():
    pyautogui.hotkey('ctrl', 'w')

def increase_brightness(amount=10):
    current_brightness = sbc.get_brightness(display=0)[0]
    new_brightness = min(100, current_brightness + amount)
    sbc.set_brightness(new_brightness, display=0)

def decrease_brightness(amount=10):
    current_brightness = sbc.get_brightness(display=0)[0]
    new_brightness = max(0, current_brightness - amount)
    sbc.set_brightness(new_brightness, display=0)

def increase_volume(amount=0.1):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + amount)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def decrease_volume(amount=0.1):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current_volume - amount)
    volume.SetMasterVolumeLevelScalar(new_volume, None)


cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                finger_status = get_finger_status(hand_landmarks)
                
                if finger_status == [0, 1, 0, 0, 0]:
                    increase_brightness(10)
                elif finger_status == [0, 1, 1, 0, 0]:
                    decrease_brightness(10)
                elif finger_status == [0, 1, 1, 1, 0]:
                    increase_volume(0.1)
                elif finger_status == [0, 1, 1, 1, 1]:
                    decrease_volume(0.1)
                elif finger_status == [1, 0, 0, 0, 1]:
                    change_tab(next_tab=True)
                elif finger_status == [1, 0, 0, 0, 0]:
                    change_tab(next_tab=False)
                elif finger_status == [0, 0, 0, 0, 0]:
                    close_tab()
            
                cv2.putText(image, f'Fingers: {finger_status}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', image)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
