# CS-Ground

## Description


# Client Setup

## Description

Front end system using ReactJs

## Running Client
```commandline
cd client
npm install  # update dependencies
npm start
```

# Server Setup

## Description

Backend server API using Python Flask

## Dependencies

* Python 3.9+
* The required dependencies are included in the requirements.txt file

## Environment Setup
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

## Installing

Install the required Python dependencies using:

```commandline
pip install -r requirements.txt
```

## Running the Server

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
