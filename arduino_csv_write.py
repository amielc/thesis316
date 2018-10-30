import serial
import time
import csv
import json
import numpy
import logging
import requests
from time import strftime, sleep
from datetime import datetime, time
from spl_meter import listen
from apscheduler.schedulers.background import BackgroundScheduler


start = datetime.now()
startTime = start.replace(microsecond=0)
ser = serial.Serial("/dev/ttyUSB0",9600)
ser.flushInput()
sensor_data = {}
decibel = ''
winddirection =''
currentDirection =''
currentSpeed = ''
windspeed = ''
humidity =''
temp = ''
pressure ='' 
dailyrain = ''
rainRate = ''
            
def sound():
    decibel=(float(listen())) #dB level
    
def running_mean(x,N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N])/float(N)

def write_and_POST():
    #POST
    headers = {'content-type': 'application/json'}
    url = "http://167.99.65.237/api"
    request = requests.post(url, data = str_data, headers=headers) 
    #write csv
	with open("sensor_data.csv","a") as outfile:
            writer=csv.writer(outfile,delimiter=",")
            writer.writerow([startTime2,temp,humidity,pressure,windspeed,currentSpeed,winddirection,currentDirection,dailyrain,rainrate,decibel])
    print("-----------------data printed and sent-----------------------")
    print(request.text)


if __name__ == "__main__":

    logging.basicConfig()
    scheduler = BackgroundScheduler()
    scheduler.add_job(write_and_POST, 'interval', minutes=1)
    scheduler.start()
    while 1:
        sound()
        if ser.inWaiting():
            try:
                startTime = datetime.now()
                startTime2 = startTime.replace(microsecond=0)
                decibel = float(listen()) #dB level
                
                sensors = ser.readline()
                data = json.loads(sensors)
                                
                winddirection = data["windDirection"]
                currentDirection = data["currentDirection"]
                currentSpeed = data["currentSpeed"]
                windspeed = data["windSpeed"]
                humidity = data["humidity"]
                temp = data["temperature"]
                pressure = data["pressure"]
                dailyrain = data["dailyRain"]
                rainrate = data["rainRate"]
                data["decibel"] = decibel
                str_data = json.dumps(data)
                
                sensors=''
         
            except KeyboardInterrupt:
                    print ("\ndone")
            except ValueError as e:
                    print ("No JSON string read")

