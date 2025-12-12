
---

# 🚘 Developing-a-driver-monitoring-system-to-avoid-traffic-accidents-using-artificial-intelligence


### 🔍 YOLOv8 • CARLA Simulator • Flask API

A real-time driver monitoring system integrated with a neural-controlled autonomous driving agent inside the CARLA simulator.

---

## 📌 Overview

This project aims to reduce traffic accidents by accurately detecting driver behaviors using deep learning and enabling the simulated vehicle to react automatically based on real-time driver state analysis.

The system integrates:

* **YOLOv8** for detecting driver states
* **CARLA** for autonomous driving simulation
* **Flask API** to connect YOLO with the CARLA agent in real time

---

## 🎯 Project Objectives

* Detect driver states with high accuracy in real time
* Integrate driver monitoring with autonomous driving logic
* React automatically to dangerous driver behaviors
* Build a flexible framework for future deployment on real vehicles

---

## 🧱 System Components

### 1️⃣ YOLOv8 Driver State Detection

File: **`YOLO_SENT.py`** 

Responsible for:

* Loading a trained YOLOv8 model
* Processing video frames
* Detecting unsafe behaviors (sleeping, texting, calling, etc.)
* Sending detected classes to CARLA via Flask

---

### 2️⃣ Flask API

Implemented inside: **`slslkn_test9.py`** 

Used to:

* Receive detected driver states from the YOLO script
* Share them with the CARLA autonomous control logic

---

### 3️⃣ CARLA Autonomous Reaction System

File: **`slslkn_test9.py`** 

Provides:

* Full CARLA environment setup
* Vehicle spawning, sensors, camera management
* BehaviorAgent / BasicAgent autonomous driving
* Real-time reaction based on YOLO detection
* Custom parking algorithm implementation

---

## 📂 Project Structure

```
project/
│── YOLO_SENT.py                # YOLOv8 driver behavior detection
│── slslkn_test9.py             # CARLA + Flask + autonomous control logic
│── README.md                   # Project documentation
│── /runs/obb/train*/           # YOLO model weights (best.pt)
│── YOLO_S1.mp4                 # Optional test video
```

---

## 🖥️ How to Run the Project

### 1️⃣ Run YOLO Detection

Edit paths inside `YOLO_SENT.py`:

```python
model_path = "path/to/best.pt"
video_path = "path/to/video.mp4"
```

Then execute:

```bash
python YOLO_SENT.py
```

---

### 2️⃣ Run CARLA + Flask Server

Start CARLA simulator:

```
CarlaUE4.exe -quality-level=Low
```

Then run the main script:

```bash
python slslkn_test9.py
```

The system will:

* Receive YOLO state detections
* Trigger autonomous reactions
* Update the HUD and camera feeds

---

## 🧪 Supported YOLO Driver States

| Label | Description          |
| ----- | -------------------- |
| c0    | Safe driving         |
| c1    | Texting              |
| c2    | Phone call           |
| c3    | Adjusting radio      |
| c4    | Drinking             |
| c5    | Reaching back        |
| c7    | Talking to passenger |
| d0    | Eyes closed          |
| d1    | Yawning              |
| d2    | Drowsiness           |
| d3    | Eyes open            |

---

## 🛠️ Requirements

### YOLO / Python Dependencies

```
torch
ultralytics
opencv-python
requests
```

### CARLA Dependencies

```
pygame
numpy
Flask
carla PythonAPI
agents (BehaviorAgent / BasicAgent)
```

---

## 📸 Examples & Visual Output

> You can later add GIFs, detected frames, or CARLA screenshots here.

---

## 📚 Academic Report

The full academic project document is included:
**Developing a driver monitoring system to avoid traffic accidents**


---

## 🚀 Future Improvements

* Increase and diversify training dataset
* Add driver identity recognition (anti-theft)
* Deploy system on real hardware (Jetson / Raspberry Pi)
* Integrate with advanced ADAS systems

---

## 📝 License

MIT License 

---


## ⭐ Contributions

Pull requests are welcome!
Feel free to open issues or suggest improvements.

---

إذا رغبت:

