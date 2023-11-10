from getUuid import get_uuid
from connect import get_server
import paho.mqtt.client as mqtt
import json
from controller import buildGpio
from threading import Timer

buildGpio(True, False, True)

currentField = None

server, serverPort, browserPort = get_server()

ident = get_uuid()

metaTopic = f"displays/{ident}"
currentField = None

isDriver = True
isEnabled = False

currentTimer = None

alreadySubscribed = False

def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT server')
    global currentField
    currentField = None
    print('setting to disabled by default')
    buildGpio(True, False, True)
    print('subscribing to the meta topic')
    print(metaTopic)
    client.subscribe(metaTopic)

def handleMeta(payload):
    fieldId = payload['fieldId']
    global currentField
    if currentField != fieldId:
        print(f"Assigned to field {fieldId}")
        if currentField is not None:
            client.unsubscribe(f"fieldStatus/{currentField}")
        client.subscribe(f"fieldStatus/{fieldId}")
        currentField = fieldId

def handleFieldStatus(payload):
    global isDriver, currentTimer
    state = payload['state']
    if currentTimer:
        currentTimer.cancel()

    if state == 'PAUSED':
        print('Match paused')
        buildGpio(True, False, isDriver)
        buildGpio(True, False, True)
        isDriver = True
    elif state == 'AUTO' or state == 'PROG_SKILLS':
        print('Starting auto')
        buildGpio(True, False, False)
        buildGpio(True, True, False)
        delay = 60
        if state == "AUTO":
            delay = 15
        currentTimer = Timer(delay, lambda: buildGpio(True, False, True))
        isDriver = False
    elif state == 'DRIVER' or state == 'DRIVER_SKILLS':
        print('Starting teleop')
        buildGpio(True, False, True)
        buildGpio(True, True, True)
        delay = 60
        if state == "DRIVER":
            delay = 105
        currentTimer = Timer(delay, lambda: buildGpio(True, False, False))
        isDriver = True
    else:
        print('Disabling')
        buildGpio(True, False, isDriver)
        buildGpio(True, False, False)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode('utf-8'))
    if topic == metaTopic:
        handleMeta(payload)
    else:
        handleFieldStatus(payload)

client = mqtt.Client(transport='websockets')

client.on_connect = on_connect
client.on_message = on_message

client.connect(server, 1883, 60)

def doTheThing():
    global client
    client.loop_forever()

if __name__=='__main__':
   print('doing the thing')
   doTheThing()
