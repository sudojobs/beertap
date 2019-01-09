from flask import Flask, jsonify, abort, request, render_template
from relaydefinitions import relays, relayIdToPin
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
from threading import Thread, Event
from configuration import cfg 

__author__ = '--'


#MQTT_PATH   = "table_01"
#MQTT_SERVER= "192.168.0.122" 

tb01_fact = pigpiofactory(host=cfg.table01_ip)
tb01 = LED(cfg.relay, pin_factory=tb01_fact)

tb02_fact = pigpiofactory(host=cfg.table02_ip)
tb02 = LED(cfg.relay, pin_factory=tb02_fact)

tb03_fact = pigpiofactory(host=cfg.table03_ip)
tb03 = LED(cfg.relay, pin_factory=tb03_fact)

tb04_fact = pigpiofactory(host=cfg.table04_ip)
tb04 = LED(cfg.relay, pin_factory=tb04_fact)

tb05_fact = pigpiofactory(host=cfg.table05_ip)
tb05 = LED(cfg.relay, pin_factory=tb05_fact)

tb06_fact = pigpiofactory(host=cfg.table06_ip)
tb06 = LED(cfg.relay, pin_factory=tb06_fact)

tb07_fact = pigpiofactory(host=cfg.table07_ip)
tb07 = LED(cfg.relay, pin_factory=tb07_fact)

tb08_fact = pigpiofactory(host=cfg.table08_ip)
tb08 = LED(cfg.relay, pin_factory=tb08_fact)

tb09_fact = pigpiofactory(host=cfg.table09_ip)
tb09 = LED(cfg.relay, pin_factory=tb09_fact)

tb10_fact = pigpiofactory(host=cfg.table10_ip)
tb10 = LED(cfg.relay, pin_factory=tb10_fact)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True

# turn the flask app into a socketio app
socketio = SocketIO(app)


@socketio.on('connect', namespace='/t01test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t01test')
def test_disconnect():
     print('Cient disconnected')


#------------------------------------------------------
#Table Webpages
#------------------------------------------------------

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

@app.route('/table05')
def table05():
    return render_template('table05.html')

@app.route('/table06')
def table06():
    return render_template('table06.html')

@app.route('/table07')
def table07():
    return render_template('table07.html')

@app.route('/table08')
def table08():
    return render_template('table08.html')

@app.route('/table09')
def table09():
    return render_template('table09.html')

@app.route('/table10')
def table10():
    return render_template('table10.html')


def Setup():
    print("Setup Complete") 

@socketio.on('connect', namespace='/t01test')
def test_connect():
     print('Cient connected')

@socketio.on('disconnect', namespace='/t01test')
def test_disconnect():
     print('Cient disconnected')


def UpdatePinFromRelayObject(relay):
    print (relay)
    if(relay['id'] == 1):
      if(relay['state']=='on'): 
         tb01.on()
      else:
         tb01.off()
    elif(relay[id] ==2):
      if(relay['state']=='on'): 
         tb02.on()
      else:
         tb02.off()
    elif(relay[id] ==3):
      if(relay['state']=='on'): 
         tb03.on()
      else:
         tb03.off()
    elif(relay[id] ==4):
      if(relay['state']=='on'): 
         tb04.on()
      else:
         tb04.off()
    elif(relay[id] ==5):
      if(relay['state']=='on'): 
         tb05.on()
      else:
         tb05.off()
    elif(relay[id] ==6):
      if(relay['state']=='on'): 
         tb06.on()
      else:
         tb06.off()
    elif(relay[id] ==7):
      if(relay['state']=='on'): 
         tb07.on()
      else:
         tb07.off()
    elif(relay[id] ==8):
      if(relay['state']=='on'): 
         tb08.on()
      else:
         tb08.off()
    elif(relay[id] ==9):
      if(relay['state']=='on'): 
         tb09.on()
      else:
         tb09.off()
    elif(relay[id] ==10):
      if(relay['state']=='on'): 
         tb10.on()
      else:
         tb10.off()


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

def on_connect_table01(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_01")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table01(client, userdata, msg):
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
    #socketio.emit('newnumber', data, namespace='/test')
    socketio.emit('t01number', data, namespace='/t01test')


def on_connect_table02(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_02")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table02(client, userdata, msg):
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
    socketio.emit('t02number', data, namespace='/t02test')


def on_connect_table03(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_03")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table03(client, userdata, msg):
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
    socketio.emit('t03number', data, namespace='/t03test')


def on_connect_table04(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_04")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table04(client, userdata, msg):
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
    socketio.emit('t04number', data, namespace='/t04test')


def on_connect_table05(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_05")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table05(client, userdata, msg):
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
    socketio.emit('t05number', data, namespace='/t05test')


def on_connect_table06(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_06")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table06(client, userdata, msg):
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
    socketio.emit('t06number', data, namespace='/t06test')


def on_connect_table07(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_07")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table07(client, userdata, msg):
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
    socketio.emit('t07number', data, namespace='/t07test')


def on_connect_table08(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_08")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table08(client, userdata, msg):
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
    socketio.emit('t08number', data, namespace='/t08test')

def on_connect_table09(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_09")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table09(client, userdata, msg):
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
    socketio.emit('t09number', data, namespace='/t09test')

def on_connect_table10(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
    client.subscribe("table_10")

  # The callback for when a PUBLISH message is received from the server.
def on_message_table10(client, userdata, msg):
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
    socketio.emit('t10number', data, namespace='/t10test')


if __name__ == "__main__":
    print("starting...")
    try:
        Setup()
        table01 = mqtt.Client()
        table02 = mqtt.Client()
        table03 = mqtt.Client()
        table04 = mqtt.Client()
        table05 = mqtt.Client()
        table06 = mqtt.Client()
        table07 = mqtt.Client()
        table08 = mqtt.Client()
        table09 = mqtt.Client()
        table10 = mqtt.Client()
        table01.on_connect = on_connect_table01
        table01.on_message = on_message_table01
        table02.on_connect = on_connect_table02
        table02.on_message = on_message_table02
        table03.on_connect = on_connect_table03
        table03.on_message = on_message_table03
        table04.on_connect = on_connect_table04
        table04.on_message = on_message_table04
        table05.on_connect = on_connect_table05
        table05.on_message = on_message_table05
        table06.on_connect = on_connect_table06
        table06.on_message = on_message_table06
        table07.on_connect = on_connect_table07
        table07.on_message = on_message_table07
        table08.on_connect = on_connect_table08
        table08.on_message = on_message_table08
        table09.on_connect = on_connect_table09
        table09.on_message = on_message_table09
        table10.on_connect = on_connect_table10
        table10.on_message = on_message_table10
        #client.connect(MQTT_SERVER, 1883, 60)
        table01.connect(cfg.table01_ip, 1883, 60)
        table02.connect(cfg.table02_ip, 1883, 60)
        table03.connect(cfg.table03_ip, 1883, 60)
        table04.connect(cfg.table04_ip, 1883, 60)
        table05.connect(cfg.table05_ip, 1883, 60)
        table06.connect(cfg.table06_ip, 1883, 60)
        table07.connect(cfg.table07_ip, 1883, 60)
        table08.connect(cfg.table08_ip, 1883, 60)
        table09.connect(cfg.table09_ip, 1883, 60)
        table10.connect(cfg.table10_ip, 1883, 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        table01.loop_start()
        table02.loop_start()
        table03.loop_start()
        table04.loop_start()
        table05.loop_start()
        table06.loop_start()
        table07.loop_start()
        table08.loop_start()
        table09.loop_start()
        table10.loop_start()
        socketio.run(app,host='0.0.0.0',port=80,debug=False)
    finally:
        print("cleaning up")
        #GPIO.cleanup()

