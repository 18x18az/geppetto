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
            client.unsubscribe(f"fieldControl/{currentField}")
        client.subscribe(f"fieldControl/{fieldId}")
        currentField = fieldId

def handleFieldStatus(payload):
    mode = payload['mode']
    endTime = payload['endTime']
    print(mode)
    print(endTime)
    isDriver = mode == 'DRIVER'
    isEnabled = endTime != None
    buildGpio(True, isEnabled, isDriver)

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
