 #Requirements
* Python 3 (3.6+)
* Pip

#Installation
#####This step assumes that you have Python and pip installed
Step 1: `pip install pipenv`

Step 2: `pipenv install -r requirements.txt`

Step 3: `pipenv shell` 


Now the required packages have been installed and system is ready to run the project

#Initialization
In order for the project to run we need to initialize database which will store all the data

Step 4: From the root of the project run the following:
`./init_db_windows` or `init_db_windows.bat`
OR 
`./init_db_linux_mac` or `bash init_db_linux_mac.sh`

Step 5 Validate a folder by the name `migrations` and a file by the name `p3i.db` should now exist at the root of the project

#Run

There are two modes to run the project
1. Development
    
    To run the project in this mode
    
    Step 6: Run the following command from the root of the project
    `./debug_windows` or `debug_windows.bat`
    OR
    `./debug_linux_mac` or `bash debug_linux_mac.sh`
    
2. Production

    To run the project in this mode
    
    Step 6: Run the following command from the root of the project
    `./deploy_windows` or `deploy_windows.bat`
    OR
    `./deploy_linux_mac` or `bash deploy_linux_mac.sh`
    
By default your project will start running at the localhost:5000 or http://127.0.0.1:5000/

####Note:
By default a user would be created with CEO (admin) level access, when you run the system for the first time, in the system so that further users can be created using that one.

Credentials for this users are as follows:

* Username: admin@polito.it
* Password: admin123