from flask import Flask, redirect, request, Response, jsonify, send_file 
#from flask.json import jsonify
from werkzeug.wrappers import response
import json
import pymongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt



#mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=100000)
mongo = pymongo.MongoClient(connection_string)
mongo.server_info()
db = mongo.get_database("swep-be")
user_check = db.stage_one_vps
user_info  = db.users


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app) 
app.config["SECRET_KEY"] ="youcannotguessit"
secret_key = "youcannotguessit"

#@app.route("/", methods=["POST", "GET"])
@app.route("/card", methods=["POST", "GET"])
def card():
    
    if request.method =="GET":
        #reg_number = request.form.get("reg_number")
        reg_number = request.args[("RegistrationNumber")]
        user= user_info.find_one({"registrationNumber":reg_number})
        
        if user :
            stage_one = user_check.find_one({"user":(user.get("_id"))})
            #return (json.dumps(stage_one), 200)
            if stage_one["status"]=="complete" :

                message = {"Status":stage_one["status"], "Name":user["firstName"]+" "+user["lastName"], "Registration Number":user["registrationNumber"], "health center id":user["health_center_id"], "passport":stage_one["passport"]}
                return json.dumps(message), 200
            else:
                return Response(response=("status isn/'t complete"), status=401)
        else: 
            return Response(response= ("user not found"), status=404)
    return "this is the work in progress"
    
            


if __name__ =="__main__":
    app.run()
