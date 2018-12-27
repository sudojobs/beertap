import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import  sys
import time
import datetime
value =0


global count
count = 0
start_counter = 0
flow1 = 0

def countPulse(channel):
   global count
   if start_counter == 1:
      count = count + 1
      flow = count / (60 * 7.5)
  

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

MQTT_SERVER = "192.168.43.27"
MQTT_PATH = "test_channel"
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(14 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(14, GPIO.BOTH, callback=countPulse, bouncetime=200)


while True:
 try:
     if(GPIO.input(24)):
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        flow = (count * 16)
        flow1=flow1 + flow
        print (flow1)
        count = 0
        time.sleep(0.5)    
        publish.single(MQTT_PATH,flow1, hostname=MQTT_SERVER)
     else:
        flow1 = 0
 except KeyboardInterrupt:
        # Reset GPIO settings
        GPIO.cleanup()
