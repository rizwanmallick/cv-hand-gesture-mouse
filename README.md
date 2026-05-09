````md
# 🖐️ CV Hand Gesture Mouse

An AI-powered touchless virtual mouse system that enables users to control computer operations using real-time hand gestures captured through a webcam.

This project uses Computer Vision, Hand Tracking, and Gesture Recognition techniques to replace traditional mouse interaction with a modern touchless Human Computer Interaction (HCI) system.

The system is built using Python, OpenCV, MediaPipe, and PyAutoGUI, and supports cursor movement, mouse clicks, screenshots, multimedia volume control, and media play/pause operations using hand gestures.

---

# 🚀 Features

- Real-time hand tracking using webcam
- AI-based hand landmark detection
- Cursor movement 
- Left click gesture
- Right click gesture
- Screenshot capture gesture
- Smooth mouse movement
- Scroll up
- Scroll down
- drag
- Volume Up gesture
- Volume Down gesture
- Media Play/Pause gesture
- Touchless Human Computer Interaction
- Fast and lightweight processing
- MediaPipe-based hand landmark model
- Modular project architecture

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Computer vision processing |
| MediaPipe | Hand landmark detection |
| PyAutoGUI | Mouse and keyboard automation |
| NumPy | Mathematical operations |
| Webcam | Real-time video input |

---

# 📂 Project Structure

```bash
cv-hand-gesture-mouse/
│
```
gesture_mouse/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── hand_landmarker.task    # MediaPipe hand landmark model
├── config/
│   ├── __init__.py
│   └── settings.py         # Configuration settings
├── core/
│   ├── __init__.py
│   ├── gesture_classifier.py  # Gesture recognition logic
│   ├── hand_detector.py       # Hand detection using MediaPipe
│   ├── mouse_controller.py    # Mouse control functionality
│   ├── volume_controller.py   # Volume control using pycaw
│   ├── utils.py               # Utility functions
│   └── test_volume.py         # Volume control test script
```


---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/cv-hand-gesture-mouse.git
```

---

## 2️⃣ Navigate to Project Folder

```bash
cd cv-hand-gesture-mouse
```

---

## 3️⃣ Create Virtual Environment (Optional but Recommended)

### Windows

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Project

```bash
python main.py
```

After running:

* Webcam will start automatically
* Hand gestures will control the system cursor and multimedia operations

---

# ✋ Gesture Controls

| Gesture                  | Action           |
| ------------------------ | ---------------- |
| Index open + thumb open  | Move Cursor      |
| Thumb + Index Pinch      | Right Click      |
| Thumb + Middle Pinch     | Left Click       |
| index open + middle open | Scroll up        |
| half index + half middle | Scroll down      |
| Thumb open + pinky open  | Screenshot       |
| Thumb + ring pinch       | Drag             |

Volume mode
| All finger closed (hold 3 sec)  | Switch Mode      |
| Thumb + Index Pinch(move up)    | Volume Up        |
| Thumb + Index Pinch(move down)  | Volume Down      |
| index open + middle open        | Play/Pause Media |

---

# 🧠 How The Project Works

## Step 1 — Video Capture

The webcam continuously captures live video frames.

---

## Step 2 — Hand Detection

MediaPipe detects:

* Hand position
* Finger landmarks
* Hand coordinates

The project uses the pretrained MediaPipe hand landmark model:

```python
hand_landmarker.task
```

---

## Step 3 — Landmark Processing

The system extracts:

* Finger tip positions
* Distance between fingers
* Finger states (up/down)
* Gesture patterns

---

## Step 4 — Gesture Classification

Different hand gestures are classified into actions such as:

* Cursor movement
* Mouse clicks
* Volume control
* Media control
* Screenshot capture

---

## Step 5 — System Control

PyAutoGUI and system control functions perform:

* Cursor movement
* Mouse clicks
* Volume changes
* Media play/pause actions


# 🔥 Key Concepts Used

* Computer Vision
* Hand Tracking
* Gesture Recognition
* Human Computer Interaction (HCI)
* AI-based Interaction
* Real-time Video Processing
* Automation Systems

---

# 🚀 Future Improvements

* Air swipe gesture for app switching
* Brightness control using gestures
* Virtual keyboard
* Multi-hand support
* 3D gesture recognition
* AI-customizable gestures
* Smart glove integration
* Gaming gesture support
* Presentation mode
* Virtual drawing system

---

# 🌍 Future Industry Applications

## 1. Smart Classrooms

Touchless presentation and teaching control.

## 2. AR/VR Interaction

Natural interaction in virtual environments.

## 3. Medical Systems

Touchless control in hospitals and operation theaters.

## 4. Robotics

Gesture-based robot control systems.

## 5. Gaming Industry

Immersive gesture-based gaming experiences.

## 6. Industrial Automation

Machine control without physical interaction.

## 7. Assistive Technology

Helping physically challenged users interact with computers.

## 8. Smart TVs & Smart Homes

Gesture-based multimedia and appliance control.

## 9. Automotive Systems

Touchless infotainment control inside vehicles.

## 10. Human Computer Interaction Research

Advanced research in next-generation interaction systems.

---

# 📈 Advantages

* No physical mouse required
* Low-cost implementation
* Touchless interaction
* Real-time processing
* Easy to use
* Portable system
* Modern AI-based interface

---

# ⚠️ Limitations

* Requires proper lighting conditions
* Webcam quality affects accuracy
* Background noise may affect detection
* Very fast hand movement can reduce precision

---

# 📦 Requirements

```txt
opencv-python
mediapipe
pyautogui
numpy
```

---

# 👨‍💻 Author

## Rizwan

B.Tech CSE Student
Passionate about:

* Computer Vision
* AI Tools
* Python Development
* Human Computer Interaction
* Automation Systems

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you like this project:

* Star the repository
* Fork the project
* Share feedback
* Contribute improvements

---

# 📬 Contact

Feel free to connect for collaboration, improvements, or project discussions.

```
```
