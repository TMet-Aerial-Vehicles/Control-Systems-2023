# Control Systems 2023
Toronto Metropolitan Aerial Vehicles (formally RUAV)

Control Systems 2023


This repository contains source code used for drone flight and computer vision
detection, executed on a Raspberry Pi

## Description

The code in this repository is used to control quadcopter drones using mavlink
connection through dronekit. It additionally contains code for creating and
reading QR codes, along with the ability to map the drone's path and export
its binary files into csv. 

## Dependencies

* Python 3.9+
* The required dependencies are included in the requirements.txt file

## Installing

Install the required Python dependencies using:
```commandline
pip install -r requirements.txt
```

## Executing program

* To run the main script, which does...:
```
python main.py
```

## Creating a Script

* Important imports:
    * For standardized logging across different scripts:
  ```python
  import logging
  from logging_script import start_logging
  start_logging()
  ```
    * For drone control and connection:
  ```python
  from pixhawk import Pixhawk
  ```
    * For sound notifications:
  ```python
  from sound import countdown, play_quick_sound
  ```
For method utilization, see main.py and backup.py



## Authors

* [Craig Pinto](https://github.com/CraigP17)

## File Structure (To Be Updated)

* drone_testing/: testing scripts for different components
    * file.py: File description
* images/
* qr/
    * qr_creator.py: Creates QR codes
    * qr_reader.py: Reads QR and decodes into given competition format
* sampleQR/
    * Sample competition QR codes
* sounds/
    * Sample sound wave files
* venv/: Python virtual environment
* videos/
* algorithms.py: Methods for path optimization
* logging_script: Logging method to standardize logging to the same file
* pixhawk.py: Pixhawk class with methods to control drone flight
* requirements.txt: Package dependencies
* sound.py: Methods for playing sound files
* task_1.py: Task 1 Main File
* task_2.py: Task 2 Main File

## Acknowledgements
