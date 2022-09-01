# About
**Project Title:**   Ekklesia<br>
**Built By:**  Benjamin A. Ngafua<br>
**Location:** Monrovia, Liberia<br>
**Description:** Church Management Software<br>
**Video Demo:** [Benjamin A. Ngafua's cs50x Final Project](https://youtu.be/nzqE3m4DkJ8)

# What is Ekklesia?
- Ekklesia is a church management software that aids churches and similar in managing, automating and organizing daily operations.

- It allows church members to see God's hand through ministries

# Functions?
1. It tracks and manages resources
2. It enhances communication
3. It monitors church growth
4. Currently use for administrator.

# Technology used
- **Framework:**
    - Flask
    
- **Templates :**
    - Jinja2
- **Frontend**
    - >Template from: [TEMPLATEMO](https://themewagon.com/)

- **Backend Language:** 
    - Python
- **Database**
    - SQLite3
- **Images use:**
    - > The images are from: [PEXELS](https://www.pexels.com/)


# Feature
|Description |Status |
|---------|------|
|Landing page|90%|
|Dashboard statistics | 80%|
| Store users | 80% |
|Create Members | 80% |
|Communicate to members| Yet to be started|
| Track financial transaction | Yet to be started |

# Requirements
Install all the modules in requirements.txt file to get access to all the functionalities and packages running well

> Manually install each module by running
```
pip3 install <module>
```

<br>

> Automatically install all the modules by running

```
pip3 install -Ur requirements.txt
``` 

<br>

## Virtual environments
Virtual environments are independent groups of Python libraries, one for each project.
Python comes bundled with the venv module to create virtual environments and install packages for a project that do not affect other projects on your computer.
Let's setup our   [venv](https://docs.python.org/3/library/venv.html#module-venv)
<br>
## Create an environment
Create a the folder<b style="color: orange;"> venv </b> within this `home` directory: 

> macOS/Linux
```
$ python3 -m venv venv
```

## Activate the environment

Before you work on this project, activate the corresponding environment:

> macOS/Linux
```
. venv/bin/activate
```


Run the app
```
flask run
```


If you are new to flask, you might want to learn a bit about flask [here](https://flask.palletsprojects.com/en/2.2.x/quickstart/) to get you started
<br>
<br>

# Directories and Files:
- **churchAPP:**
    - Comprises of all code that runs the application.
    - **static:**
        > Contains the css, js, fonts and  images files with important 
        links that enhance the layout and the performances
    - **templates**
        > Contains html file layouts and structure
        
    - **__init__.py**
        > This makes the 'churchAPP directory' a python package
        > Once churchAPP is imported the ``_init_.py``  runs automatically
    - **modules.py** 
        > This file heavily comprises of databases
    - **views.py** 
        > Main views, it controls all url endpoints for routing
        > It also deals with functionality on the frontend data 
- **app.py**
    > This file will be run when starting the web server of this application
- **requirements.txt**
    > This file comprises of all the packages that supports this application. The packages need to be install before getting started
- **Procfile, Gemfile**
    > These files are used for the hosting of this app on `Heroku`
- **church.db**
    > The database that stores all the queries info
- **README.md**
    > Comprises of the application's detail