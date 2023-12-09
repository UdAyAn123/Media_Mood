import sys
sys.path.append('')
from scripts.get_everything import get_all
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util
from flask_cors import CORS, cross_origin
from twilio.rest import Client
from model import fun
import threading


app = Flask(__name__)
CORS(app, support_credentials=True)

# Replace this with your MongoDB URI:
app.config['MONGO_URI'] = "mongodb+srv://nandisaumya2004:mckYReHDCDzSBNFa@cluster0.24snpal.mongodb.net/"

# Initialize MongoDB client:
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.sih  # Replace 'mydatabase' with your database name
news = db.news

#SMS setup:
account_sid = 'AC467f69d0b372a258e6948588929cd6b1'
auth_token = '4ea41b2c32e137fcbc50b9fcf42a4e5c'
client = Client(account_sid, auth_token)
twilio_phone_number = '+13342343980'
# Recipient's phone number (including country code, e.g., +1 for the USA)
recipient_phone_number = '+918637831983'
# Message content
message_body = 'Hello, this is a test message from ssn!'

#Phone Number Map of PIB Officers:
phoneNumbers = {
    "rail":"+918637831983",
    "tech":"+918001172472"
}

# Define a global variable to control the task
stop_task = False

# Define your task function
def my_periodic_task():
    if not stop_task:
        # Your task logic here
        print("....................................Scheduler starts........................................")
        newsData = get_all()
        news.insert_many(newsData)
        print(newsData)
        # Schedule the task to run again
        threading.Timer(600, my_periodic_task).start()

# Function to stop the task
def stop_periodic_task():
    global stop_task
    stop_task = True

# Function to start the task
def start_periodic_task():
    global stop_task
    stop_task = False
    my_periodic_task()


@app.route('/')
def index():
    return "Helloo"

@app.route("/news")
def getAllnews():
    data = list(news.find())
    for i in data:
        print(i)
    serialized_data = json_util.dumps(data)
    return serialized_data

@app.route("/news", methods=['POST'])
def postNews():
    data1 =  request.get_json()
    print(data1['name'])
    if(data1['name']==''):
        newsData = get_all()
    else:
        newsData = get_all(data1['name'])
    news.insert_many(newsData)
    return "success"

@app.route("/send_mail")
def sendMail():
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )
    print(f"Message sent successfully with SID: {message.sid}")


@app.route('/start_task')
def start_task():
    start_periodic_task()
    return 'Task started.'

@app.route('/stop_task')
def stop_task_route():
    stop_periodic_task()
    return 'Task stopped.'


if __name__ == '__main__':
    app.run(debug=True)

