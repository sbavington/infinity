#!/usr/bin/python3

import os
import glob
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

demand = 75
device_list = (glob.glob(base_dir + '28*'))
device_file = ''

device_label = {"28-0416715ba3ff": "0", "28-0516712d26ff": "1", "28-041671088cff" : "2", "28-0416710b96ff" : "3", "28-051670df96ff" : "4"}


while True:
    for device in device_list:
        device_file = device + '/w1_slave'
        device_name = device.split('/')
        serial = device_name[5]
        device_tag = device_label[serial]
        #print ("label Number = {}".format(device_label.get(serial)))
        #print ('Read device {} file {}'.format(device, device_file))
        temp_data = open(device_file)
        lines = temp_data.readlines()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            demand_f = demand - temp_f
            print ('{} Temp C = {:.2f} Temp F = {:.2f}'.format(device_tag,round(temp_c,2),round(temp_f,2)))