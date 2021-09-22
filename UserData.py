from bson import ObjectId

from config import client, DATABASE
from app import app
from flask import jsonify , make_response
from flask import request
from bson.json_util import dumps


#user=[{'name':'ayush','age':'23'},
#      {'name':'khaniya','age':22}]



@app.route('/index')
def index():
    return("hello world")

@app.route('/users',methods=['GET'])
def getUsersData():
    users=DATABASE.collection.find()
    resp=dumps(users)
    return resp
@app.route('/users/<id>',methods=['GET'])
def getUserData(id):
    user=DATABASE.collection.find_one({'_id':ObjectId(id)})
    resp=dumps(user)
    return resp


@app.route('/createUser',methods=['POST'])
def createuser():
    tempjson=request.json
    name=tempjson['name']
    email=tempjson['email']
    age=tempjson['age']

    DATABASE.collection.insert({'name':name,'email':email,'age':age})
    resp=jsonify("user added successfully")
    resp.status_code=200
    return resp
@app.route('/deleteUser/<id>',methods=['DELETE'])
def deleteUser(id):
    DATABASE.collection.delete_one({'_id':ObjectId(id)})
    resp=jsonify("Deleted succesfully")
    resp.status_code=200
    return resp

@app.route('/updateUser/<id>',methods=['PUT'])
def updateUser(id):
    _id=id
    tempjson=request.json
    name=tempjson["name"]
    email=tempjson["email"]
    age=tempjson["age"]

    DATABASE.collection.update_one({'_id':ObjectId(_id['$old']) if '$old' in _id else ObjectId(_id)},{'$set':{'name':name,'email':email,'age':age}})

    resp=jsonify("User updated successfully")
    resp.status_code=200
    return resp
