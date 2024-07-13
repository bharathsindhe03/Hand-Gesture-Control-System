# Hand Gesture Control System

This project uses a combination of MediaPipe, OpenCV, PyAutoGUI, and other libraries to create a hand gesture control system. The system captures hand gestures via a webcam and maps them to various computer control actions such as changing tabs, adjusting brightness and volume, and closing tabs.

## Features

- **Change Tabs**: Move to the next or previous tab in your browser using specific hand gestures.
- **Adjust Brightness**: Increase or decrease the screen brightness.
- **Adjust Volume**: Increase or decrease the system volume.
- **Close Tabs**: Close the current tab.

![alt text](https://github.com/bharathsindhe03/Hand-Gesture-Control-System/blob/main/img/img1.jpg)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/bharathsindhe03/Hand-Gesture-Control-System.git
    cd hand-gesture-control
    ```


2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the script:**
    ```sh
    python hand_gesture_control.py
    ```

2. **Control actions:**
    - **Increase Brightness:** Raise the index finger.
    - **Decrease Brightness:** Raise the index and middle fingers.
    - **Increase Volume:** Raise the index, middle, and ring fingers.
    - **Decrease Volume:** Raise the index, middle, ring, and pinky fingers.
    - **Next Tab:** Raise the thumb and pinky.
    - **Previous Tab:** Raise only the thumb.
    - **Close Tab:** No fingers raised.

## Dependencies

- `opencv-python`
- `mediapipe`
- `pyautogui`
- `screen_brightness_control`
- `pycaw`

You can install these dependencies using the following command:
```sh
pip install opencv-python mediapipe pyautogui screen_brightness_control pycaw

## Contact Information

If you have any questions, suggestions, or feedback, feel free to reach out:

- **Email:** [aravind.shyamkrishna@gmail.com] and [sindhebharath10@gmail.com]


Feel free to connect or send a message! We'd love to hear from you.

---
