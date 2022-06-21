# Flask REST API application

This is an application providing a REST API.

The entire application is contained within the `app.py` file.

Code is hosted on  [Heroku](https://flaskeerapi.herokuapp.com/) and database at mongodb

## Installation and Running the app

- pip install -r requirements.txt
- pyhton3 app.py

# REST API

The REST API to the app is described below.

## Get list of Things

### Register

`POST /register`

    curl -i -H 'Accept: application/json' https://flaskeerapi.herokuapp.com/register

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

