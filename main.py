from marshmallow import Schema, fields, ValidationError
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from datetime import datetime
from flask_cors import CORS
from json import loads
from pytz import datetime
import pytz
import pyowm 

def first8(s):
    return s[:8]

def specTime(s):
    return s[11:19]


app = Flask(__name__)
CORS(app)


mongo_uri = "mongodb+srv://nashhq:N.hamilton@cluster0.7pkmk.mongodb.net/SWS?ssl=true&ssl_cert_reqs=CERT_NONE"
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

APIKEY="2bb5d6bcd8576573247f90e6d1667307"                  #your API Key here as string
OpenWMap=pyowm.OWM(APIKEY)                   # Use API key to get data

Weatherforecast = OpenWMap.three_hours_forecast("Kingston") # give the city where you need to forecast

class timeValidation(Schema):
    time = fields.String(required = True)
    

class SoilValidation(Schema):
    moisture = fields.Integer(required = True)
    sensor_id = fields.Integer(required = True)

class SprinklerSchema(Schema):
    sprinklers_name = fields.String(required=True)
    sprinklers_location  = fields.String(required=True)
    sprinklers_id = fields.String(required=True)

class WeatherPrediction(Schema):
    rain_data = fields.Boolean(required = True)
    sun_data = fields.Boolean(required = True)
    Date=fields.String(Required = True)


@app.route("/")
def home():
    
    return render_template ('main_page.html')

@app.route("/add_Sprinkler")
def add_sprinkler():
    
    return render_template ('add_Sprinkler.html')

@app.route("/weather")

def data_weather():
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    spec= specTime(tVartoString)
    day = first8(tVartoString)
    time_second= "8:30:00+00"
    time = day + "26 " +time_second
    rain=Weatherforecast.will_be_rainy_at(time) # forecast rain
    sun=Weatherforecast.will_be_sunny_at(time) # forecast sun

    # print("There will be rain :",rain) # print details
    # print("There will be sun :",sun) #print details
    # print(day + "22 "+time_second) 
    
    database = {
        "rain_data" : rain,
        "sun_data" : sun,
        "Date": day + "26 ("+ spec +")"
    }
  
    try:
        # print(database)
        weatherTemp = WeatherPrediction().load(database)
        mongo.db.weathers.insert_one(weatherTemp)

    except ValidationError as ve:
        return ve.messages, 400
    return render_template ('weather.html')

@app.route("/set_time")
def set_time():
    
    return render_template ('set_time.html',)

@app.route("/individual")
def individual():
    
    return render_template ('individual_info.html',)

    
###############################################################################
## ADHOC  ROUTES

@app.route("/weathers") 
def get_weather_data():
    weather_data = mongo.db.weathers.find({}, {'_id': False, 'Date':False}).sort([('Date', -1)]).limit(1)
    
    return jsonify(loads(dumps(weather_data))) 

@app.route("/time") 
def get_time_data():
    time = mongo.db.times.find({}, {'_id': False}).sort([('time', -1)]).limit(1)
    
    return jsonify(loads(dumps(time))) 

@app.route("/time", methods=["POST"])
def post_time_data():
    
    print("TIME ADDED")
    try:
        time = request.json["time"]
        

        jsonBody = {
            "time": time
            
        }

        print(jsonBody)

        time = timeValidation().load(jsonBody)
        mongo.db.times.insert_one(time)

        return{
            "success": True,
            "message": "Time Added Successfully"
        }
    except ValidationError as e:
        return e.messages, 400


@app.route("/esp") 
def esp_data():
    weather_data = mongo.db.weathers.find({}, {'_id': False, 'Date': False}).sort([('Date', -1)]).limit(1)
    sensor_reading = mongo.db.soil_moisture.find({}, {'_id': False}).sort([('Date', -1)]).limit(1)
    time = mongo.db.times.find({}, {'_id': False}).sort([('time', -1)]).limit(1)
    result = {}
    result["weather"] = weather_data
    result["Sensor"] = sensor_reading
    result["Time"] = time
    print(result)
    return jsonify(loads(dumps(result))) 

    
###############################################################################
## Soil Moisture  ROUTES

@app.route("/sensor") 
def sensor_data():
    sensor = mongo.db.soil_moisture.find()
    return jsonify(loads(dumps(sensor))) 

@app.route("/sensor", methods = ["POST"])
def data_post():
    req = request.json
    moisture = req["moisture"] 
    percentage = moisture
    
    database = {
        "sensor_id" : req["sensor_id"],
        "moisture" : percentage
    }
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    try:
        print(database)
        sensorTemp = SoilValidation().load(database)
        mongo.db.soil_moisture.insert_one(sensorTemp)
        return {"success": "true","msg": "Data Saved In Database Successfully", "Date": tVartoString}

    except ValidationError as ve:
        return ve.messages, 400

@app.route("/sensor/<ObjectId:id>", methods=["PATCH", "DELETE"])
def sensor_methods(id):
    if request.method == "PATCH":
        mongo.db.soil_moisture.update_one({"_id": id}, {"$set": request.json})
        sensors = mongo.db.soil_moisture.find_one(id)
        
        return loads(dumps(sensors))    

    elif request.method == "DELETE":
        result = mongo.db.soil_moisture.delete_one({"_id": id})

        if result.deleted_count == 1:
            return {
                "success": True
            }
        else:
            return {
                "success": False
            }, 400



   
    
###############################################################################
## SMART WATERING SYSTEM ROUTES


@app.route("/sprinklers") 
def get_sprinkler_data():
    sprinklers = mongo.db.sprinklers.find()
    return jsonify(loads(dumps(sprinklers))) 

@app.route('/sprinklers/<ObjectId:id>')
def patient_data_id (id):
    spec_sprinklers = mongo.db.sprinklers.find_one(id)
    return loads(dumps(spec_sprinklers))  

@app.route("/sprinklers", methods=["POST"])
def post_sprinkler_data():
    
    print("Sprinkler ADDED")
    try:
        sprinklers_name = request.json["sprinklers_name"]
        sprinklers_location = request.json["sprinklers_location"]
        sprinklers_id = request.json["sprinklers_id"]

        jsonBody = {
            "sprinklers_name": sprinklers_name,
            "sprinklers_location": sprinklers_location,
            "sprinklers_id": sprinklers_id
        }

        print(jsonBody)

        sprinkler_data = SprinklerSchema().load(jsonBody)
        mongo.db.sprinklers.insert_one(sprinkler_data)

        return{
            "success": True,
            "message": "Sprinkler Added Successfully"
        }
    except ValidationError as e:
        return e.messages, 400


  
@app.route('/sprinklers/<ObjectId:id>', methods=["PATCH", "DELETE"])
def sprinkler_methods(id):
    if request.method == "PATCH":
        mongo.db.sprinklers.update_one({"_id": id}, {"$set": request.json})

        sprinklers = mongo.db.sprinklers.find_one(id)
        
        return loads(dumps(sprinklers))    
    elif request.method == "DELETE":
        result = mongo.db.sprinklers.delete_one({"_id": id})

        if result.deleted_count == 1:
            return {
                "success": True
            }
        else:
            return {
                "success": False
            }, 400


if __name__ == "__main__":
    app.run(
        debug=True, host= "0.0.0.0",
        port = 5500
    )
   