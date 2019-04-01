from flask import Flask, jsonify, abort, request, render_template
from time import sleep
import configuration1 as cfg
from flask_socketio import SocketIO
from threading import Thread, Event
import requests
import json
import os
import logging
import sqlite3 

logging.basicConfig(filename='beertap.log',level=logging.DEBUG)

db_table={}

__author__ = '--'
# defining the api-endpoint  
API_ENDPOINT = "https://api.hk.eats365.net/o/oauth2/token"

RestaurantName = "WOM Limited牛魔"
RestaurantCode = "HK059093"
APIClientID = "80aa2427eccf4b39b927dc60255a9e75"                
APIClientSecret = "37bceb1e2d164f72aebec76e535a0ac184cb5859e133430ebc9626d5e041b8a9"
                  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True

# turn the flask app into a socketio app
socketio = SocketIO(app)

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Cient connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Cient disconnected')

def Setup():
    print("Setup Complete") 

@app.route('/WebRelay/', methods=['GET'])
def index():
    return render_template('Index.html');

@app.route('/WebRelay/api/relays', methods=['GET'])
def get_relays():
    return jsonify({'relays': relays})

@app.route('/WebRelay/api/relays/<int:relay_id>', methods=['GET'])
def get_relay(relay_id):
    matchingRelays = [relay for relay in relays if relay['id'] == relay_id]
    if len(matchingRelays) == 0:
        abort(404)
    return jsonify({'relay': matchingRelays[0]})

@app.route('/WebRelay/api/relays/<int:relay_id>', methods=['PUT'])
def update_relay(relay_id):
    matchingRelays = [relay for relay in relays if relay['id'] == relay_id]

    if len(matchingRelays) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if not 'state' in request.json:
        abort(400)

    relay = matchingRelays[0]
    relay['state']=request.json.get('state')
    return jsonify({'relay': relay})

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

  # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print("%s %s" % (msg.topic,msg.payload))
    status=str(msg.payload.decode('utf-8','ignore'))


if __name__ == "__main__":
    print("Starting...")
    try:
        Setup()
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(MQTT_SERVER, 1883, 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_start()
        socketio.run(app,host='0.0.0.0',port=80,debug=False)
    finally:
print("cleaning up")
