# Autonomous-Driving-FPGA
Autonomous driving system using supervised learning and FPGA integration
# Hardware Design
The FPGA implementation is provided in the `verilog/` folder, which includes UART communication logic and 7-segment display control.
# Project Title 
Supervised Learning-Based Autonomous Driving System with FPGA-Based Real-Time Output
# Description
This project implements an autonomous driving system using a simulation-based approach combined with hardware interfacing. A virtual driving environment is created using PyGame, where data is collected by manually controlling the vehicle. The collected images are labeled with steering directions and used to train a supervised learning model.
The trained model is then used to perform real-time autonomous driving within the simulation. Based on the input frames, the system predicts the appropriate steering direction such as left, straight, or right. These decisions are transmitted to an FPGA board through serial communication over a USB interface, where the output is displayed using a 7-segment display.
# Features
- Simulation-based autonomous driving using PyGame  
- Data collection and labeling for supervised learning  
- Image preprocessing using OpenCV  
- Real-time steering prediction  
- Serial communication between PC and FPGA  
- Hardware integration using FPGA  
- Direction display using 7-segment display
# How to Run
1. Run manual simulation to collect dataset:
   python manual_simulator.py
2. Train the model using collected data:
   python train_csv.py
3. Extract trained model weights:
   python extract_weights.py
4. Run autonomous simulation:
   python autonomous_simulator.py
5. Run FPGA interface program:
   python pygame_fpga.py
Before running the project, ensure that Python is installed on your system. The following libraries are required to execute the simulation, data processing, and communication tasks.

Install the required Python libraries using the following commands:

pip install pygame  
pip install numpy  
pip install opencv-python  
pip install pyserial  

Additionally, Xilinx Vivado must be installed for FPGA design and programming. Ensure that the Basys 3 FPGA board drivers are properly installed and the board is recognized by the system.

After completing the installations, verify that the required libraries are successfully installed before running the project.
# Hardware Used
- Basys 3 FPGA Board  
- USB cable for communication and power supply  
- Computer system for running simulation and training  
The FPGA is used to receive steering commands from the Python application and display the corresponding direction on a 7-segment display.
# Note about Dataset
The dataset used in this project is generated from the simulation environment during manual driving. Due to size limitations, only a few sample images are included in this repository. The complete dataset was used during the training phase but is not uploaded to maintain repository efficiency.

