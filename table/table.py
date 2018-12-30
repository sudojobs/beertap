import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import sys
import time
import datetime
import tableconfig as tcfg
global count
count = 0
start_counter = 0
flow1 = 0

def countPulse(channel):
   global count
   if (GPIO.input(tcfg.flow)):
       global count
       count = count + 1
       time.sleep(0.5)      

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(tcfg.relay,GPIO.OUT)
GPIO.setup(tcfg.flow , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(tcfg.flow, GPIO.RISING, callback=countPulse, bouncetime=300)


while True:
 try:
     if(GPIO.input(tcfg.relay)):
        flow = count
        flow1=flow #xx+ round(flow*14.4,2)
        print (flow1)
        publish.single(tcfg.TABLE_ID,flow1, hostname=tcfg.TABLE_IP)
     else:
        flow1 =0
        count =0
        publish.single(tcfg.TABLE_ID,flow1, hostname=tcfg.TABLE_IP)
 except KeyboardInterrupt:
        # Reset GPIO settings
        GPIO.cleanup()
