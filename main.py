from ultralytics import YOLO
import requests
import time

import serial
import string

#GPS data from arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

#Line notify
def line(txt):
	url = 'https://notify-api.line.me/api/notify'
	token = 'FXkSbQJioSr5nZhb0HcZCIDz0zQdrltgmFcYgQ0o2YN'
	headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
	
	#GPS data
	while True:
		line = ser.readline().decode('utf-8').rstrip()
		if line.find("GPS") != -1:
			txt += '\n'
			txt += line
			break
	#Send line text
	r = requests.post(url, headers=headers , data = {'message':txt})
	print(r.text)

#Predictation
model = YOLO("best.pt")
results = model.predict(source="0", stream=True, show=True, conf=0.7) # source already setup
names = model.names

for r in results:
    for c in r.boxes.cls:
        print(names[int(c)])
        n = names[int(c)]
        if n.find('BLACKPOD') != -1  or n.find('FROSTYPOD') != -1 or n.find('MIRID') != -1:
            line(n)
time.sleep(2)
