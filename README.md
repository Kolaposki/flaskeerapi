# Flask REST API application

This is an application providing a REST API.

The entire application is contained within the `app.py` file.

Code is hosted on [Heroku](https://flaskeerapi.herokuapp.com/) and database at mongodb

## Installation and Running the app

- pip install -r requirements.txt
- python3 app.py

# REST API

The REST API to the app is described below.

## Authentication Endpoints

### Register

    URL : https://flaskeerapi.herokuapp.com/register

    Method : POST

    Headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }

    Body :    {
                first_name : 'lead_test@subi.com',
                last_name : '123456'
                email : 'lead_test@subi.com',
                password : '123456'
              }

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    status: successful
    message: user created successfully

### Login

    URL : https://flaskeerapi.herokuapp.com/login

    Method : POST

    Headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }

    Body :    {
                email : 'lead_test@subi.com',
                password : '123456'
              }

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    "status": "successful",
    "message": "user authenticated",
    "data": "{'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImVtYWlsIjoienVja0BtYWlsLmNvbSIsIl9pZCI6IjYyYjFiYWRmZWQ1NmRkNzlmYjUxMmU3NyJ9LCJleHBpcmF0aW9uIHRpbWUiOiIyMDIyLTA2LTIyIDE0OjI1OjI5LjMzMTUyMyJ9.Xc8K_SVz7YOvk9XidzwPbk7DOP08yHvS9Wvtnjdgh4c', 'user': {'_id': '62b1badfed56dd79fb512e77', 'first_name': 'Mark', 'last_name': 'Zuck', 'email': 'zuck@mail.com', 'created': datetime.datetime(2022, 6, 21, 12, 34, 39, 273000)}}"



## Template CRUD ENDPOINTS

### Insert new Template

    URL : https://flaskeerapi.herokuapp.com/template

    Method : POST

    Headers : {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                'template_name': 'lorem',
                'subject': 'ipsum',
                'body': 'lorem ipsum is simply dummy text', 
                }  

### Response

    HTTP/1.1 201 CREATED
    Status: 201 CREATED
    Connection: close
    Content-Type: application/json
    "info": "Successfully created",
    "inserted_id": "62b1d9db568b87cb3937b9be"


### Get All Template

    URL : https://flaskeerapi.herokuapp.com/template

    Method : GET

    Headers : {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}  

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    "_id": "62b1d9db568b87cb3937b9be",
    "template_name": "lorem",
    "subject": "ipsum",
    "body": "lorem ipsum is simply dummy text"



### Get Single Template

    URL : https://flaskeerapi.herokuapp.com/template/<template_id>

    Method : GET

    Headers : {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}  

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    "_id": "62b1d9db568b87cb3937b9be",
    "template_name": "lorem",
    "subject": "ipsum",
    "body": "lorem ipsum is simply dummy text"


### Update Single Template

    URL : https://flaskeerapi.herokuapp.com/template/<template_id>

    Method : PUT

    Headers : {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                'template_name': ' ',
                'subject': ' ',
                'body': ' ',
            }     

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    "_id": "62b1d9db568b87cb3937b9be",
    "template_name": "",
    "subject": "",
    "body": ""
    "info": "Updated template successfully"



### Delete Single Template

    URL : https://flaskeerapi.herokuapp.com/template/<template_id>

    Method : DELETE

    Headers : {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}     

### Response

    HTTP/1.1 204 No Content
    Status: 204 No Content
    Connection: close
    Content-Type: application/json
    'info': 'Template deleted successfully'


