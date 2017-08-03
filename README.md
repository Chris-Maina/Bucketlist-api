[![Build Status](https://travis-ci.org/Chris-Maina/Bucketlist-api.svg?branch=develop)](https://travis-ci.org/Chris-Maina/Bucketlist-api)     [![Coverage Status](https://coveralls.io/repos/github/Chris-Maina/Bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/Chris-Maina/Bucketlist-api?branch=develop)   [![Code Health](https://landscape.io/github/Chris-Maina/Bucketlist-api/develop/landscape.svg?style=flat)](https://landscape.io/github/Chris-Maina/Bucketlist-api/develop)

# Bucketlist-api
Flask API for bucketlist application

## Installation and setup
Clone this repo:
  * https://github.com/Chris-Maina/Bucketlist-api.git
  
Navigate to the bucketlist-api directory:
  * cd bucketlist-api
  
Create a virtual environment and activate it.
  * mkvirtualenv bucketlist-api workon bucketlist-api
  
Install dependencies:
  * pip install -r requirements.txt
  
 Initialize, migrate and update the database:
  * python run.py db init python run.py db migrate python run.py db upgrade
  
 Test the application by running:
  * nosetests test_file_name
  
## Running application
To start application:
  * python run
Access the endpoints using your preferred client e.g. Postman

#### Endpoints

| Resource URL                                | Methods | Description        | Requires Token |
|---------------------------------------------|---------|--------------------|----------------|  
| /auth/register/                             | POST    | User registers     | FALSE          |
| /auth/login/                                | POST    | User login         | FALSE          |
| /bucketlist/                                | POST    | Creates buckets    | TRUE           |
| /bucketlist/                                | GET     | Get buckets        | TRUE           |
| /bucketlist/<int:bid>                       | PUT     | Edit a bucket      | TRUE           |
| /bucketlist/<int:bid>                       | DELETE  | Delete a bucket    | TRUE           |
| /bucketlist/<int:bid>                       | GET     | Get a bucket       | TRUE           |
| /bucketlist/<int:bid>/activities            | POST    | Create an activity | TRUE           |
| /bucketlist/<int:bid>/activities            | GET     | Get activities     | TRUE           |
| /bucketlist/<int:bid>/activities/<int:aid>  | PUT     | Edit an activity   | TRUE           |
| /bucketlist/<int:bid>/activities/<int:aid>  | DELETE  | Delete an activity | TRUE           |
| /bucketlist/<int:bid>/activities/<int:aid>  | GET     | Get an activity    | TRUE           |

#### Options

| Method | Description                 |
|--------|-----------------------------|
| GET    | Retrieves a resource(s)     |
| POST   | Creates a new resource      |
| PUT    | Edits an existing resource  |
| DELETE | Deletes an existing resource|
