
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import  sys
import time
MQTT_SERVER = "192.168.1.9"
MQTT_PATH = "test_channel"
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
while True:
 if(GPIO.input(18)):
    publish.single(MQTT_PATH, "values", hostname=MQTT_SERVER)
    time.sleep(2)
