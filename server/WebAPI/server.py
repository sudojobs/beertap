

from flask import Flask, jsonify, abort, request, render_template
from relaydefinitions import relays, relayIdToPin
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
from threading import Thread, Event
import requests
import json

__author__ = '--'
# defining the api-endpoint  
API_ENDPOINT = "https://dev-api.hk.eats365.net/o/oauth2/token"

RestaurantName  ="BeerTap" 
RestaurantCode  ="HK054042"
APIClientID     ="d3c345808af848adb6c89a43a48e18be"

APIClientSecret ="66f7456893ca4dce855bfa481a68aa9fe3a42b04a95d4ee2bbb385096cecded0"

# data to be sent to api 
data = {'client_id':APIClientID, 
        'client_secret':APIClientSecret, 
        'grant_type':"client_credentials"} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 

accessdata=r.json()
AccessToken= accessdata['access_token']
TokenType= accessdata['token_type']
#print AccessToken 
#print TokenType
# api-endpoint 
URL = "https://dev-opi.hk.eats365.net/v1/menu/init"
head= "Bearer %s" % AccessToken


PARAMS = { 'restaurant_code':RestaurantCode }
HEADER = { 'Authorization':head } 
### sending get request and saving the response as response object 
p = requests.get(url = URL, headers=HEADER, params = PARAMS) 
### extracting data in json format 
data = p.json()
#print data
#ProductID=data["restaurant_list"]
#print(json.dumps(ProductID, indent=4, separators=(". ", " = ")))

MQTT_PATH   =[ ("A4",0),("A6",0),("A1",0),("A3",0),("C1",0),("C2",0),("C3",0),("V1",0),("V2",0),("V4",0)]
MQTT_SERVER= "localhost" 

fa1 = PiGPIOFactory(host='192.168.1.116')
fa4 = PiGPIOFactory(host='192.168.1.111')
fa3 = PiGPIOFactory(host='192.168.1.107')
fa6 = PiGPIOFactory(host='192.168.1.109')
fc1 = PiGPIOFactory(host='192.168.1.110')
fc2 = PiGPIOFactory(host='192.168.1.113')
fc3 = PiGPIOFactory(host='192.168.1.103')
fv4 = PiGPIOFactory(host='192.168.1.114')
fv2 = PiGPIOFactory(host='192.168.1.117')
fv1 = PiGPIOFactory(host='192.168.1.105')


A1 = LED(24, pin_factory=fa1)
A4 = LED(24, pin_factory=fa4)
A3 = LED(24, pin_factory=fa3)
A6 = LED(24, pin_factory=fa6)
C1 = LED(24, pin_factory=fc1) 
C2 = LED(24, pin_factory=fc2) 
C3 = LED(24, pin_factory=fc3) 

V4 = LED(24, pin_factory=fv4) 
V2 = LED(24, pin_factory=fv2) 
V1 = LED(24, pin_factory=fv1) 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True

# turn the flask app into a socketio app
socketio = SocketIO(app)


@socketio.on('connect', namespace='/t0test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t0test')
def test_disconnect():
     print('Cient disconnected')


@socketio.on('connect', namespace='/t1test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t1test')
def test_disconnect():
     print('Cient disconnected')


@socketio.on('connect', namespace='/t2test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t2test')
def test_disconnect():
     print('Cient disconnected')


@socketio.on('connect', namespace='/t3test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t3test')
def test_disconnect():
     print('Cient disconnected')


@app.route('/table01')
def table01():
    return render_template('table01.html')

@app.route('/table02')
def table02():
    return render_template('table02.html')

@app.route('/table03')
def table03():
    return render_template('table03.html')

@app.route('/table04')
def table04():
    return render_template('table04.html')


#GPIO.setmode(GPIO.BCM)

#relayStateToGPIOState = {
#    'off' : GPIO.LOW,
#    'on' : GPIO.HIGH
#    }

def Setup():
    print("Setup Complete") 

#for relay in relays:
    #    GPIO.setup(relayIdToPin[relay['id']],GPIO.OUT)
    #    GPIO.output(relayIdToPin[relay['id']],relayStateToGPIOState[relay['state']])

@socketio.on('connect', namespace='/t0test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t0test')
def test_disconnect():
     print('Cient disconnected')


@socketio.on('connect', namespace='/t1test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t1test')
def test_disconnect():
     print('Cient disconnected')


@socketio.on('connect', namespace='/t2test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t2test')
def test_disconnect():
     print('Cient disconnected')


@socketio.on('connect', namespace='/t3test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t3test')
def test_disconnect():
     print('Cient disconnected')

def UpdatePinFromRelayObject(relay):
    if(relay['id'] ==1):  
       if(relay['state']=='on'): 
          A3.on()
       else:
          A3.off()
    elif(relay['id'] ==2):
       if(relay['state']=='on'): 
          A1.on()
       else:
          A1.off()
    elif(relay['id'] ==3):
       if(relay['state']=='on'): 
          A4.on()
       else:
          A4.off()
    elif(relay['id'] ==4):
       if(relay['state']=='on'): 
          A6.on()
       else:
          A6.off()
    elif(relay['id'] ==5):
       if(relay['state']=='on'): 
          C1.on()
       else:
          C1.off()
    elif(relay['id'] ==6):
       if(relay['state']=='on'): 
          C2.on()
       else:
          C2.off()
    elif(relay['id'] ==7):
       if(relay['state']=='on'): 
          C3.on()
       else:
          C3.off()
    elif(relay['id'] ==8):
       if(relay['state']=='on'): 
          V4.on()
       else:
          V4.off()
    elif(relay['id'] ==9):
       if(relay['state']=='on'): 
          V2.on()
       else:
          V2.off()
    elif(relay['id'] ==10):
       if(relay['state']=='on'): 
          V1.on()
       else:
          V1.off()

    #GPIO.output(relayIdToPin[relay['id']],relayStateToGPIOState[relay['state']])

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
    UpdatePinFromRelayObject(relay)
    return jsonify({'relay': relay})

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

  # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("%s %s" % (msg.topic,msg.payload))
    status=str(msg.payload.decode('utf-8','ignore'))
    sup=status.split(",")
    a=sup[0].split(":")
    b=sup[1].split(":")
    number1=a[1]
    temp=b[1] 
    number2=temp[:-1]
    data = {'tap1': number1, 'tap2': number2}
    print(data)
    if(msg.topic=='A1'): 
       socketio.emit('t01number', data, namespace='/t0test')
    elif(msg.topic=='A3'):
       socketio.emit('t02number', data, namespace='/t1test')
    elif(msg.topic=='A4'):
       socketio.emit('t03number', data, namespace='/t2test')
    elif(msg.topic=='A6'):
       socketio.emit('t04number', data, namespace='/t3test')


if __name__ == "__main__":
    print("starting...")
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
        #GPIO.cleanup()

