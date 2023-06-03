# Idea
The goal of this project is to develop a drone that can simultaneously send an ambulance and deploy from its base to the patient's location, picking the best path and avoiding obstacles. In addition, each patient receives a T-shirt with a magnetic-mechanical locking mechanism and a watch with a pulse sensor and location module. When the drone arrives at the patient's position and is centred on the patient's chest, it is hooked to the T-shirt magnets and performs mechanical cardiopulmonary resuscitation, this small standalone consistently and automatically administers deep, high-quality chest compressions, while waiting for the ambulance to arrive the location and apply the required procedures to the patient.

# Project parts:
1. Cardiac arrest prediction: Achieved in 96.25% accuracy using random forest model.
2. Heart rate monitor watch: To monitor the patient's heart rate in real-time as an early warning sign of cardiac arrest. To build the watch, a Heart Rate sensor, a GPS module, an OLED display, a battery, and an ESP8266 microcontroller are needed. The Adafruit IO platform is used to monitor and analyze the heart rate and GPS data from the watch.
3. Path planning: To enable the quadcopter to move autonomously from its base into the destination which is sent to the quadcopter from the GPS module (of the watch) throughout the Adafruit server. This is done by using Informed RRT* algorithm.
4. QR code recognition & distance estimation: It is achieved by combining a detection model trained with YOLOv3 and a classification neural network. For distance estimation, the pi camera v2.1 parameters are used to avoid GPS errors exceeding 2m.
5. Control software using pixhawk flight controller and RPI4:
  - Navigation of the drone is achieved using a RPI 4 and a control script created from DroneKit source code.
  - The implemented algorithms and systems are tested for accuracy using SITL simulation and mission planner.
  - The Adafruit server and Bluetooth are used to connect all remaining components, including the watch and CPR device.
6. CPR function:
  - It is to maintain blood flow by chest compression when the heart stopped functioning.
  - It is based on AVR microcontroller interfaced with servo motor to separate CPR part from drone, Bluetooth module to receive data from RPI 4, DC motor for chest up and down motion, and switches to control it and servo motor using interrupt.
7. Hardware:
  - Pixhawk Flight controller, RPI 4, 1000kv BLDC motors, 10 inch propellers, 30 amp ESCs, 3300mAh 3-cell battery, and M8n GPS/Compass module for autonomous  navigation.
  - The Watch includes an ESP8266-12E microcontroller, MAX30102 heart rate monitor, 7M GPS module, 0.92inch oled display, and 400 mAH battery for monitoring and transmitting patient data.
  - The CPR system includes an Atmega32, hc-05 Bluetooth Module, n20 motor for demonstration, and SG90 servo for connecting and disconnecting to the drone.
