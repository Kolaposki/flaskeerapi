from flask import Flask, render_template, Response, request, jsonify
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_cors import CORS
import re
from decouple import config

app = Flask(__name__)
SECRET_KEY = config('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
DEBUG = config('DEBUG', default=False, cast=bool)

CORS(app, resources={r"/*": {"origins": "*"}})  # to avoid cors error
bcrypt = Bcrypt(app)
DB_URL = config('DB_URL')

try:
    if DEBUG:
        mongodb_client = MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
    else:
        print("connecting to db")
        mongodb_client = MongoClient(DB_URL)

    db = mongodb_client['templates']  # templates is the name of the db
    mongodb_client.server_info()  # trigger exception if it cant connect to db
except Exception as e:
    print("Unable to connect to database ", e)


######################################################################################

def token_required(f):
    # decorator for authentication
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return jsonify({"status": "fail", "message": "No token provided"}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = data['user']['_id']
                current_user = db.users.find_one({"_id": ObjectId(user_id)})

                if current_user is None:
                    return jsonify({"status": "fail", "message": "Invalid Authentication token"}), 401

            except Exception as er:
                return jsonify({"status": "fail", "message": "Invalid authorization token"}), 401
            return f(*args, **kwargs)
        else:
            print("No Authorization provided")
            return jsonify({"status": "fail", "message": "No authorization provided"}), 401

    return decorated


@app.route('/register', methods=['POST'])
def register():
    # register route
    try:
        code = 500
        status = "fail"
        message = ""

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'password': request.form['password'],
            'email': request.form['email'],
        }  # get data from request


        # regular expression for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, data['email']):
            # invalid email format
            return Response(response=json.dumps({"info": "Email is badly formatted"}),
                            status=403,
                            mimetype='application/json')

        # check uniqueness of email address
        if db.users.count_documents({"email": data['email']}) != 0:
            message = "user with that email exists"
            code = 401
            status = "fail"

        else:
            # hashing the password so it's not stored in the db as it was
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['created'] = datetime.now()

            res = db["users"].insert_one(data)
            if res.acknowledged:
                status = "successful"
                message = "user created successfully"
                code = 201

        return Response(response=json.dumps({'status': status, "message": message}),
                        status=code,
                        mimetype='application/json')

    except Exception as ex:
        print("Exception: ", ex)
        return Response(response=json.dumps({"Error": "An error occurred while registering",
                                             'info': f'{ex}'}),
                        status=500,
                        mimetype='application/json')


######################################################################################

@app.route('/users', methods=['GET'])
def get_users():
    # get users route
    try:
        data = list(db.users.find())
        for user in data:
            user['_id'] = str(user['_id'])
            user['created'] = str(user['created'])

        return Response(response=json.dumps(data),
                        status=200,
                        mimetype='application/json')
    except Exception as ex:
        print("Exception: ", ex)
        return Response(response=json.dumps({"Error": "An error occurred while getting users",
                                             'info': f'{ex}'}),
                        status=500,
                        mimetype='application/json')


######################################################################################


@app.route('/login', methods=['POST'])
def login():
    # login route

    try:
        data = {
            'password': request.form['password'],
            'email': request.form['email'],
        }
        user = db['users'].find_one({"email": f'{data["email"]}'})

        if user:
            user['_id'] = str(user['_id'])
            if user and bcrypt.check_password_hash(user['password'], data['password']):
                time = datetime.utcnow() + timedelta(hours=24)
                token = jwt.encode({
                    "user": {
                        "email": f"{user['email']}",
                        "_id": f"{user['_id']}",
                    },
                    "expiration time": str(time)
                }, SECRET_KEY, algorithm='HS256').decode('utf-8')

                del user['password']  # dont need the password when returning to client

                message = f"user authenticated"
                code = 200
                status = "successful"
                res_data['access_token'] = token
                res_data['user'] = user

            else:
                message = "wrong password"
                code = 401
                status = "fail"
        else:
            message = "Invalid login details"
            code = 401
            status = "fail"

        return Response(response=json.dumps({'status': f'{status}', 'message': f'{message}', 'data': f'{res_data}'}),
                        status=code,
                        mimetype='application/json')

    except Exception as ex:
        print("Exception: ", ex)
        return Response(response=json.dumps({"Error": "An error occurred during login",
                                             'info': f'{ex}'}),
                        status=500,
                        mimetype='application/json')


######################################################################################


@app.route('/template', methods=['GET', 'POST'])
@token_required
def templates():
    # templates route
    try:
        if request.method == 'POST':
            data = {
                'template_name': request.form['template_name'],
                'subject': request.form['subject'],
                'body': request.form['body']
            }

            dbResponse = db.templates.insert_one(data)
            inserted_id = dbResponse.inserted_id
            if not inserted_id:
                return Response(response=json.dumps({"Error": "An error occurred while creating template"}),
                                status=500,
                                mimetype='application/json')

            return Response(response=json.dumps({'info': "Successfully created", 'inserted_id': f'{inserted_id}'}),
                            status=201,
                            mimetype='application/json')

        elif request.method == 'GET':
            data = list(db.templates.find().sort("_id", -1)) # get all templates
            for template in data:
                template['_id'] = str(template['_id'])

            return Response(response=json.dumps(data),
                            status=200,
                            mimetype='application/json')
    except Exception as ex:
        print("Exception: ", ex)
        return Response(response=json.dumps({"Error": "An error occurred while getting templates",
                                             'info': f'{ex}'}),
                        status=500,
                        mimetype='application/json')


######################################################################################
@app.route('/template/<template_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def get_template(template_id):
    # get_template route with template_id from client
    try:
        if template_id:
            if request.method == 'GET':
                # get particular template
                template = db.templates.find_one({"_id": ObjectId(template_id)})
                if not template:
                    return Response(response=json.dumps({'info': 'Invalid template id'}),
                                    status=400,
                                    mimetype='application/json')

                template['_id'] = str(template['_id'])
                return Response(response=json.dumps(template),
                                status=200,
                                mimetype='application/json')

            elif request.method == 'PUT':
                # updating a template
                set_data = {
                    'template_name': request.form['template_name'],
                    'subject': request.form['subject'],
                    'body': request.form['body']
                }
                dbResponse = db.templates.find_one_and_update({'_id': ObjectId(template_id)},
                                                              {"$set": set_data})
                if not dbResponse:
                    return Response(response=json.dumps({'info': 'Invalid template id'}),
                                    status=400,
                                    mimetype='application/json')

                dbResponse['_id'] = str(dbResponse['_id'])
                dbResponse['info'] = 'Updated template successfully'
                return Response(response=json.dumps(dbResponse),
                                status=202,
                                mimetype='application/json')

            elif request.method == 'DELETE':
                # deleting a template

                dbResponse = db.templates.delete_one(
                    {"_id": ObjectId(template_id)}
                )

                if dbResponse.deleted_count == 1:
                    return Response(response=json.dumps({'info': 'Template deleted successfully'}),
                                    status=204,
                                    mimetype='application/json')
                else:
                    return Response(response=json.dumps({'info': 'Template already deleted or not found'}),
                                    status=202,
                                    mimetype='application/json')

        else:
            # No template_id
            return Response(response=json.dumps({'info': 'template_id not provided'}),
                            status=400,
                            mimetype='application/json')
    except Exception as ex:
        print("Exception: ", ex)
        return Response(response=json.dumps({"Error": "An error occurred while getting template",
                                             'info': f'{ex}'}),
                        status=500,
                        mimetype='application/json')


######################################################################################


@app.route('/')
def home():  # just for test sake
    return 'Hello'


######################################################################################

if __name__ == '__main__':
    app.run(debug=DEBUG)
