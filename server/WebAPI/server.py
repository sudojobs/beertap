from flask import Flask, jsonify, abort, request, render_template
from relaydefinitions import relays, relayIdToPin
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
from threading import Thread, Event

__author__ = '--'


MQTT_PATH   = "table_01"
MQTT_SERVER= "192.168.0.122" 


factory = PiGPIOFactory(host='192.168.0.122')
led = LED(21, pin_factory=factory)
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


@app.route('/table01')
def table01():
    return render_template('table01.html')

@app.route('/table02')
def table02():
    return render_template('table02.html')



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

@socketio.on('connect', namespace='/test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
     print('Cient disconnected')



def UpdatePinFromRelayObject(relay):
    print (relay)
    if(relay['state']=='on'): 
       led.on()
    else:
       led.off()
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
    #print("%s %s" % (msg.topic,msg.payload))
    status=str(msg.payload.decode('utf-8','ignore'))
    sup=status.split(",")
    a=sup[0].split(":")
    b=sup[1].split(":")
    number1=a[1]
    temp=b[1] 
    number2=temp[:-1]
    print(number1)
    print(number2)
    data = {'tap1': number1, 'tap2': number2}
    print(data) 
    socketio.emit('newnumber', data, namespace='/test')


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

