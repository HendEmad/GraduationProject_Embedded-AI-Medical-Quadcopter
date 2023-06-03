import math
import sys
import time
import os
import smtplib
import time
from time import sleep
from Adafruit_IO import MQTTClient, Client, Feed, Data

smtpUser = 'user1.python@gmail.com'
smtpPass = 'hwwa fgzb pkag lifk'
toAdd = ['hendegypt7@gmail.com']
fromAdd = smtpUser
ADAFRUIT_IO_KEY = 'aio_XChs65H9SBO5uE7xnqVxAtcGbt2J'

ADAFRUIT_IO_USERNAME = 'HendEmad'

current_state = 0

a, b = 0, 0


def connected(client):
    print('Connected to Adafruit IO!  Listening for changes...')
    client.subscribe('loc-lng')
    client.subscribe('loc-lat')
    client.subscribe('drone-deploy')


def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)
def message(client, feed_id, payload):
    global current_state, a, b
    if feed_id == 'drone-deploy':
        current_state = payload
    elif feed_id == 'loc-lng':
        a = payload
        print("Feed {0} received new value: {1}".format(feed_id, a))
    elif feed_id == 'loc-lat':
        b = payload
        print("Feed {0} received new value: {1}".format(feed_id, b))


client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

client.connect()
client.loop_background()
while True:
    if current_state == '1':
        R = 6371000
        # lat ==> b, long ==> a
        x = R * math.cos(float(b)) * math.cos(float(a))
        y = R * math.cos(float(b)) * math.sin(float(a))
        subject = 'Sudden Cardiac Arrest Case'
        header = "To : " + str(toAdd) + "\n" + "From : " + str(fromAdd) + "\n" + "Subject: " +  str(subject)
        body= "there is a sudden cardiac arrest case located in: https://www.google.com/maps/dir//"+str(y)+","+str(x)+" \nthat was happened at"+ time.ctime()
        print (header + '\n' + body)

        s= smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.ehlo()

        s.login(smtpUser , smtpPass)
        s.sendmail(fromAdd, toAdd, header + '\n\n' + body)
        # s.quit()
        # sys.exit(1)
        break
print("x = ", x, "y = ", y)