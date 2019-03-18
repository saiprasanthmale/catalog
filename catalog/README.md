# Item Catalog Web App Project

BY MALE SAI PRASANTH

This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Project overview
This project shows the webapp it allows only user who created the data to edit/delete and add details.If a new user logged in he cannot edit/delete/add other users data but he can view.A new user can add a new college and he can enter data there his data cannot be edit/delete/add data by other users.

## Skills Required FOR THE PROJECT
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModel

## Files Contain folder
This project contains the files:
main.py
setup_file.py
data_init.py
templates folder contains html files
static folder contains css files
client_secrets.json file.

## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repository or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. Setup application database `python setup_file.py`
7. Insert sample data `python data_init.py`
8. Run application using `python  main.py`


## In This Project Main files 
- In this project contains `main.py` contains routes and json endpoints.
- `setup_file.py` contains the database models and tablenames it creates a database file with table.
- `data_init.py` contains the sample data and insert into the database.

### we need to install some modules and python
- Update `sudo apt-get update`
- Install Python `sudo apt-get install python`
- Install pip `sudo apt-get install python-pip`
- Import module `pip install flask`
- Import module`pip install sqlalchemy`
- Import module `pip install oauth2client`
- Import module `pip install httplib2`
- After installing modules we have to run `python setup_file.py` to create database models 
- Next run `python data_init.py` to insert sample data.
- Next run `python main.py` to execute project

							
##Creating API and OAuth client-id 
we have to create a new API and client-id.
To create client id : (https://console.developers.google.com)
- goto to credentials
- create credentials
- Click API KEY
- to create client id we have to create oAuth constent screen
- create OAuth client ID
- Application type(web application)
- Enter name(CollegeWeb)
- Authorized JavaScript origins (http://localhost:8000)
- Authorized redirect URIs = (http://localhost:8000/login) && (http://localhost:8000/gconnect)
- create
- download client_data.json and place it in the folder 


## JSON Endpoints

The following are to check JSON endpoints:

allCollegesJSON: '/CollegeWeb/JSON'
    - shows the whole college and student details

categoriesJSON: '/CollegeWeb/college_Name/JSON'
    - Displays the college names and its id
	
detailsJSON: '/CollegeWeb/colleges/JSON'
	- It shows all student details in college

categorydetailsJSON: '/CollegeWeb/<path:collegename>/colleges/JSON'
    - It shows the details in the college

DetailsJSON:
'/CollegeWeb/<path:collegename>/<path:studentdetails_name>/JSON'
    - It shows the details that the college name and student_name matches

## Final output images:

![home.png]

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
