# Control-Systems-2023

## Overview

This project was built for TMAV 2023's competition project of an autonomous drone taxi system.
It is split into three major components: [Flight](#flight), [Ground](#ground), and Shared. The Shared component contains shareable methods that the Flight and Ground components use such as logging capabilities. 


# Flight

## Description
Control Systems Flight (CS-Flight) is the flight system that will be running on the UAV. It will interact with the Pixhawk on the UAV, and communicate with the ground station.
It has two components of a Server built with Python Flask, and a Script using Python. The Server receives directional commands from CS-Ground, and sends telemetry received from the Pixhawk. The Script is designed for managing and executing flight operations using a Pixhawk flight controller and a custom Flight API

### Dependencies
* Python 3.9+
* The required dependencies are included in the requirements.txt file

### Hardware Used
* Jetson
* Pixhawk 4


## CS-Flight Server Setup

### Description
This Flask server script provides a robust API for managing and controlling flight operations. The server is designed to handle various tasks related to flight management, including route planning, command execution, telemetry forwarding, and battery status tracking. The key features of the API include:
* **Flight Readiness**: Checks and reports the readiness of the flight system at /flight-ready.
* **Telemetry Management**:
    * Propagate Telemetry: Receives and forwards telemetry data to a ground system via POST requests at /propagate-telemetry.
* **Route Management**:
    * Set Initial Route: Accepts a JSON payload to set the initial flight route at /set-initial-route.
    * Get Initial Route: Retrieves the current flight route at /get-initial-route.
    * Get Updated Route: Provides information about any updates to the flight route at /get-updated-route.
    * Set Detour Route: Updates the flight route with a detour and priority command via POST requests at /set-detour-route.
* **Command Handling**:
    * Launch: Initiates the flight launch sequence at /launch.
    * Check for Launch: Verifies if the launch process has started at /check-for-launch.
    * Set Priority Command: Sets a priority command for immediate execution at /set-priority-command.
    * Set/Reset Command: Manages and resets commands through /set-command and retrieves the last saved command with /get-command.
* **Battery Management**:
    * Battery Change Completed: Reports the completion of a battery change at /battery-change-completed.
    * Check Battery Change: Checks if the battery change has been completed at /check-for-battery-change-completed.
 
### Running CS-Flight Server
```bash
python app.py
```

## CS-Flight Script Setup

### Description
The script provides a robust framework for automated flight operations with real-time updates and command management.
The main features include:

* Configuration and Initialization: Loads configuration from a config.ini file and sets up logging. Initializes connections with Pixhawk, the Flight API, and various controllers for lights and sound.
* Route Management: Retrieves and validates an initial flight route from the Flight API. Continuously monitors and updates the route if changes are detected.
* Launch Sequence: Waits for an initiation signal from the Flight API, performs a countdown with sound alerts, and begins executing the flight route commands.
* Command Execution: Sends commands to Pixhawk based on the route, checks for priority commands, and manages execution flow. It includes handling updates to the flight route and ensuring commands are completed.


## Running CS-Flight Script
There are two tasks from the competition task days.
```commandline
python task_1.py
```



# Ground

## Description
Control Systems Ground (CS-Ground) is the ground system that will be running on a dedicated computer. It is the server that the UAV will communicate with.
It has two components of a Server built with Python Flask, and a Client built with ReactJs. The Server receives GPS telemetry and sends directional commands to the UAV. The Client displays the UAV's location on a map, as well as it provides QR Readability (competition requirement) that contains the taxi pickup and dropoff locations.

## CS-Ground Client Setup

### Description

Front end system using ReactJs

### Dependencies

npm version 8.19.2+

### Running Client
```commandline
cd client
npm install  # update dependencies
npm start
```

If an error related to dependencies is raised, run the following:
```
npm install --legacy-peer-deps
```

## CS-Ground Server Setup

### Description

Backend server API using Python Flask

### Dependencies

* Python 3.9+
* The required dependencies are included in the requirements.txt file

### Environment Setup
```commandline
cd server
```

If using Pycharm, follow 
[Virtual Environment Guide](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)
for creating the virtual environment


If creating through terminal:

```commandline
python -m venv venv
```

Activate virtual environment using:

MacOS and Linux:

```commandline
source venv/bin/activate 
```

Windows:

```commandline
venv\Scripts\activate
```

### Installing

Install the required Python dependencies using:

```commandline
pip install -r requirements.txt
```

### Running the Server

```commandline
python app.py
```



# Contributing

After cloning the repo, you'll be in the main branch

Create a new branch for your task and switch to it

```commandline
git checkout -b <branch-name>
```

Now implement your tasks and insert code

Once finished, you will push it to your branch

Use ```git status``` to see which files you have changed

Track your changes using
```commandline
git add <file-name>
```

Commit your changes to the repo, after adding all files
```commandline
git commit -m "Descriptive message about your changes"
```

Push changes to repo and set upstream
```commandline
git push -u origin <branch-name>
```

Now go to our repository in GitHub and your branch, 
create a Pull Request

Assign the Reviewer to Craig or Jacob

Add the Assignee as yourself
