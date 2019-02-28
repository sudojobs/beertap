from flask import Flask, jsonify, abort, request, render_template
from relaydefinitions import relays, relayIdToPin
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import paho.mqtt.client as mqtt
import configuration as cfg
from flask_socketio import SocketIO
from threading import Thread, Event
import requests
import json
import os
import threading

__author__ = '--'
# defining the api-endpoint  
API_ENDPOINT = "https://dev-api.hk.eats365.net/o/oauth2/token"

RestaurantName = "BeerTap"
RestaurantCode = "HK054042"
APIClientID = "d3c345808af848adb6c89a43a48e18be"
APIClientSecret = "66f7456893ca4dce855bfa481a68aa9fe3a42b04a95d4ee2bbb385096cecded0"

# data to be sent to api
data = {'client_id': APIClientID,
        'client_secret': APIClientSecret,
        'grant_type': "client_credentials"}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)

# extracting response text
pastebin_url = r.text

accessdata = r.json()
AccessToken = accessdata['access_token']
TokenType = accessdata['token_type']
# print AccessToken
# print TokenType
# api-endpoint
URL = "https://dev-opi.hk.eats365.net/v1/menu/init"
head = "Bearer %s" % AccessToken
# print head
# defining a params dict for the parameters to be sent to the API
PARAMS = {'restaurant_code': RestaurantCode}
HEADER = {'Authorization': head}

def print_square(num): 
    while True:
          print("ORDERA3")
          print(ordera3)
          print("ORDERA1")
          print(ordera1)
          print("ORDERA4")
          print(ordera4)
          print("ORDERA6")
          print(ordera6)
          time.sleep(0.5)   
    

def checkout(product_uid, quantity, remarks, table_ref_id):
    url_checkout = "https://dev-opi.hk.eats365.net/v1/order/checkout"
    data = {
        'restaurant_code': "HK054042",
        'order_mode': 'dine_in',
        'cart_item_list': [{"product_uid": product_uid, "quantity": quantity, "remarks": remarks, 'modifier_list': []}],
        'reference_type': "table",
        'reference_id': table_ref_id
    }
    try:
        p2 = requests.post(url=url_checkout, headers=HEADER, json=data)
        data_checkout = p2.json()
        return("Success")
    except Exception as e:
        print(str(e))
        return("Error")

MQTT_PATH   =[ ("A4",0),("A6",0),("A1",0),("A3",0),("C1",0),("C2",0),("C3",0),("V1",0),("V2",0),("V4",0)]
MQTT_SERVER= "localhost" 

#fa1 = PiGPIOFactory(host='192.168.1.116')
#fa4 = PiGPIOFactory(host='192.168.1.111')
#fa3 = PiGPIOFactory(host='192.168.1.107')
#fa6 = PiGPIOFactory(host='192.168.1.109')
#fc1 = PiGPIOFactory(host='192.168.1.110')
#fc2 = PiGPIOFactory(host='192.168.1.113')
#fc3 = PiGPIOFactory(host='192.168.1.103')
#fv1 = PiGPIOFactory(host='192.168.1.114')
#fv2 = PiGPIOFactory(host='192.168.1.117')
#fv4 = PiGPIOFactory(host='192.168.1.105')

fa1 = PiGPIOFactory(host=cfg.A1ip)
fa4 = PiGPIOFactory(host=cfg.A4ip)
fa3 = PiGPIOFactory(host=cfg.A3ip)
fa6 = PiGPIOFactory(host=cfg.A6ip)
fc1 = PiGPIOFactory(host=cfg.C1ip)
fc2 = PiGPIOFactory(host=cfg.C2ip)
fc3 = PiGPIOFactory(host=cfg.C3ip)
fv1 = PiGPIOFactory(host=cfg.V1ip)

retv2 = os.system("ping -q -c2 192.168.1.117")
if retv2 ==0:
   fv2 = PiGPIOFactory(host=cfg.V2ip)
   V2 = LED(24, pin_factory=fv2) 

fv4 = PiGPIOFactory(host=cfg.V4ip)

A1 = LED(24, pin_factory=fa1)
A4 = LED(24, pin_factory=fa4)
A3 = LED(24, pin_factory=fa3)
A6 = LED(24, pin_factory=fa6)
C1 = LED(24, pin_factory=fc1) 
C2 = LED(24, pin_factory=fc2) 
C3 = LED(24, pin_factory=fc3) 

V4 = LED(24, pin_factory=fv4) 
V1 = LED(24, pin_factory=fv1) 

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

@socketio.on('connect', namespace='/a4test')
def a4test_connect():
    print('Cient connected')

@socketio.on('disconnect', namespace='/a4test')
def a4test_disconnect():
    print('Cient disconnected')

@app.route('/a3')
def a3():
    return render_template('a3.html')

@app.route('/a1')
def a1():
    return render_template('a1.html')

@app.route('/a4')
def a4():
    return render_template('a4.html')

@app.route('/a6')
def a6():
    return render_template('a6.html')

@app.route('/c1')
def c1():
    return render_template('c1.html')

@app.route('/c2')
def c2():
    return render_template('c2.html')

@app.route('/c3')
def c3():
    return render_template('c3.html')

@app.route('/v1')
def v1():
    return render_template('v1.html')

@app.route('/v2')
def v2():
    return render_template('v2.html')

@app.route('/v4')
def v4():
    return render_template('v4.html')

def Setup():
    print("Setup Complete") 

def UpdatePinFromRelayObject(relay):
    if(relay['id'] ==1):  
       if(relay['state']=='on'): 
          A3.on()
          ordera3=0
       else:
          A3.off()
          ordera3=1
    elif(relay['id'] ==2):
       if(relay['state']=='on'): 
          A1.on()
          ordera1=0
       else:
          A1.off()
          ordera1=1
    elif(relay['id'] ==3):
       if(relay['state']=='on'): 
          A4.on()
          ordera4=0
       else:
          A4.off()
          ordera4=1
    elif(relay['id'] ==4):
       if(relay['state']=='on'): 
          A6.on()
          ordera6=0
       else:
          A6.off()
          ordera6=1
    elif(relay['id'] ==5):
       if(relay['state']=='on'): 
          C1.on()
          orderc1=0
       else:
          C1.off()
          orderc1=1
    elif(relay['id'] ==6):
       if(relay['state']=='on'): 
          C2.on()
          orderc2=0
       else:
          C2.off()
          orderc2=1
    elif(relay['id'] ==7):
       if(relay['state']=='on'): 
          C3.on()
          orderc3=0
       else:
          C3.off()
          orderc3=1
    elif(relay['id'] ==8):
       if(relay['state']=='on'): 
          V1.on()
          orderv1=0
       else:
          V1.off()
          orderv1=1
    elif(relay['id'] ==9):
       if(relay['state']=='on'): 
          V2.on()
          orderv2=0
       else:
          V2.off()
          orderv2=1
    elif(relay['id'] ==10):
       if(relay['state']=='on'): 
          V4.on()
          orderv4=0
       else:
          #qty1=v4data['tap1'] 
          #qty2=v4data['tap2']
          V4.off()
          orderv4=1

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
    #print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

  # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print("%s %s" % (msg.topic,msg.payload))
    status=str(msg.payload.decode('utf-8','ignore'))
    sup=status.split(",")
    a=sup[0].split(":")
    b=sup[1].split(":")
    number1=a[1]
    temp=b[1] 
    number2=temp[:-1]
    data = {'tap1': number1, 'tap2': number2}
    #print(data)
    if(msg.topic=='A3'):
       a3data=data 
       socketio.emit('a3number', a3data, namespace='/a3test')
    elif(msg.topic=='A1'):
       a1data=data
       socketio.emit('a1number', a1data, namespace='/a1test')
    elif(msg.topic=='A4'):
       a4data=data 
       socketio.emit('a4number', a4data, namespace='/a4test')
    elif(msg.topic=='A6'):
       a6data=data 
       socketio.emit('newnumber', a6data, namespace='/test')
    elif(msg.topic=='C1'):
       c1data=data 
       socketio.emit('c1number', c1data, namespace='/c1test')
    elif(msg.topic=='C2'):
       c2data=data 
       socketio.emit('c2number', c2data, namespace='/c2test')
    elif(msg.topic=='C3'):
       c3data=data 
       socketio.emit('c3number', c3data, namespace='/c3test')
    elif(msg.topic=='V1'):
       v1data=data 
       socketio.emit('v1number', v1data, namespace='/v1test')
    elif(msg.topic=='V2'):
       v2data=data 
       socketio.emit('v2number', v2data, namespace='/v2test')
    elif(msg.topic=='V4'):
       v4data=data 
       socketio.emit('v4number', v4data, namespace='/v4test')


if __name__ == "__main__":
    #print("starting...")
    try:
        Setup()
        t1 = threading.Thread(target=print_square, args=(10,))
        t1.start()
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
