from flask import Flask, render_template, Response, request
from pymongo import MongoClient
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongodb_client = MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
    db = mongodb_client.company
    mongodb_client.server_info()  # trigger exception if it cant connect to db
except Exception as e:
    print("Unable to connect to database ", e)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


######################################################################################

@app.route('/users/<_id>', methods=['PATCH'])
def update_user(_id):
    try:

        if _id is None or _id == '':
            return Response(response=json.dumps({"Error": "Please provide id"}),
                            status=400,
                            mimetype='application/json')

        # ObjectId converts to mongodb-ish id
        dbResponse = db.users.update_one(
            {"_id": ObjectId(_id)}, {"$set": {'firstName': request.form['firstName']}}
        )

        if dbResponse.modified_count == 1:
            return Response(response=json.dumps({'info': 'User modified successfully'}),
                            status=201,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps({'info': 'Nothing modified'}),
                            status=200,
                            mimetype='application/json')

    except Exception as ex:
        print("Exception: ", ex)
        return Response(response=json.dumps({"Error": "An error occurred while updating user",
                                             'info': f'{ex}'}),
                        status=500,
                        mimetype='application/json')


######################################################################################

######################################################################################

@app.route('/users/<_id>', methods=['DELETE'])
def delete_user(_id):
    try:

        if _id is None or _id == '':
            return Response(response=json.dumps({"Error": "Please provide id"}),
                            status=400,
                            mimetype='application/json')

        # ObjectId converts to mongodb-ish id
        dbResponse = db.users.delete_one(
            {"_id": ObjectId(_id)}
        )

        if dbResponse.deleted_count == 1:
            return Response(response=json.dumps({'info': 'User deleted successfully'}),
                            status=201,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps({'info': 'User already deleted'}),
                            status=200,
                            mimetype='application/json')

    except Exception as ex:
        print("Exception: ", ex)
        return Response(response=json.dumps({"Error": "An error occurred while updating user",
                                             'info': f'{ex}'}),
                        status=500,
                        mimetype='application/json')


######################################################################################

@app.route('/users', methods=['GET'])
def get_users():
    try:
        data = list(db.users.find())
        print("data:", data)
        for user in data:
            user['_id'] = str(user['_id'])

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

@app.route('/create_user', methods=['POST'])
def create_user():
    user = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName']
    }
    print("data", request.data)
    dbResponse = db.users.insert_one(user)
    print("inserting user ", user)
    inserted_id = dbResponse.inserted_id
    print("inserted_id: ", inserted_id)

    # if data is None or data == {} or 'Document' not in data:
    #     return Response(response=json.dumps({"Error": "Please provide connection information"}),
    #                     status=400,
    #                     mimetype='application/json')

    return Response(response=json.dumps({'info': "Successfully created", 'inserted_id': f'{inserted_id}'}),
                    status=201,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
