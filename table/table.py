import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import sys
import time
import datetime
import tableconfig as tcfg
import json 
global t1count
global t2count

t1count = 0
t2count = 0
tap1 = 0
tap2 = 0
flag = 0 
lastval1 = 0
lastval2 = 0

def tap1Pulse(channel):
   global t1count
   if (GPIO.input(tcfg.tap1)):
       global t1count
       t1count = t1count + 1

def tap2Pulse(channel):
   global t2count
   if (GPIO.input(tcfg.tap2)):
       global t2count
       t2count = t2count + 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(tcfg.relay,GPIO.OUT)
GPIO.setup(tcfg.tap1 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(tcfg.tap2 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(tcfg.tap1, GPIO.RISING, callback=tap1Pulse, bouncetime=300)
GPIO.add_event_detect(tcfg.tap2, GPIO.RISING, callback=tap2Pulse, bouncetime=300)

while True:
 try:
     if(GPIO.input(tcfg.relay)):
        tap1 = t1count
        tap2 = t2count
        if(lastval1!=tap1 or lastval2!=tap2):
           message= {}
           message['tap2']=tap2
           message['tap1']=tap1
           fullmessage=json.dumps(message) 
           print(fullmessage) 
           publish.single(tcfg.TABLE_ID,fullmessage, hostname=tcfg.TABLE_IP)
           lastval1=tap1
           lastval2=tap2
           flag= 1
     else:
      if(flag==1):
        flag    = 0
        tap1    = 0
        t1count = 0
        tap2    = 0
        t2count = 0
        message= {}
        message['tap2']=tap2
        message['tap1']=tap1
        fullmessage=json.dumps(message)
        print(fullmessage) 
        publish.single(tcfg.TABLE_ID,fullmessage, hostname=tcfg.TABLE_IP)
 except KeyboardInterrupt:
        # Reset GPIO settings
        GPIO.cleanup()
