import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import  sys
import time
import datetime
value =0

MQTT_SERVER = "192.168.43.27"
MQTT_PATH = "test_channel"
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(14 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(14, GPIO.BOTH, callback=sensorCallback, bouncetime=200)

def sensorCallback(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  if GPIO.input(channel):
    # No magnet
    print("Sensor HIGH " + stamp)
  else:
    # Magnet
    print("Sensor LOW " + stamp)

while True:
 try:
     if(GPIO.input(24)):
        publish.single(MQTT_PATH,value, hostname=MQTT_SERVER)
        value=value+5
        time.sleep(0.1)
 except KeyboardInterrupt:
        # Reset GPIO settings
        GPIO.cleanup()
