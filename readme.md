
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#env=staging/https://github.com/uwidcit/pharm-backend)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# Pharm Backend
Backend application for pharmacy application

# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
This step runs automatically when this project is opened in gitpod.
```
$ pip3 install -r requirements.txt
```

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate database credentials are set in environment.staging.json file. 
If environment.staging.json does not exist, it must be created in the root directory of this project. It should contain the follow configuration

```
{
    "SQLALCHEMY_DATABASE_URI" : <url_to_database> or "sqlite:///test.db",
    "SECRET_KEY" : <some custom key text>,
    "JWT_ACCESS_TOKEN_EXPIRES" : <num days jwt should expire>,
    "DEBUG": true,
    "ENV" : "staging"
}
```

Then run the following command.

```
$ python3 manage.py initDB
```

When adding new models or changing models this command may also work to update the database. If it is unsuccessful you should use the migration command in the migration section.

# Running the Project
After installing dependencies and initializing the database, run the following command to run the project.

_For development:_
```
$ python3 manage.py start
```

When running the project for development in gitpod 

_For production using gunicorn:_
```
$ gunicorn -w 4 App.main:app
```

Instead of using a json file, when running in production, the project will look for environment variables named after the same fields as in environment.staging.json.

# Deploying
App will be configured to auto deploy master branch to heroku at [https://pharmacy-app-2021.herokuapp.com](https://pharmacy-app-2021.herokuapp.com). You will need to setup the environment variables in heroku. 

# Manage.py Commands

Manage.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```
# inside manage.py


@manager.command
def hello():
    print('hello')

...    
```

Then execute the command by calling the function name as a parameter to the script

```
$ python3 manage.py hello
```



# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```
$ python3 manage.py db init
$ python3 manage.py db migrate
$ python3 manage.py db upgrade
$ python3 manage.py db --help
```
