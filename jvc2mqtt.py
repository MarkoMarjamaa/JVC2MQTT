import paho.mqtt.client as mqtt
import json
import serial

broker_address="homeautomation"
discovery_topic="homeassistant"
my_topic="JVC2MQTT"
port="/dev/projector"
object_name="Living Room Projector"
object_id="living_room_projector"

############
def on_message(client, userdata, message):
    command = str(message.payload.decode("utf-8"))
    if command == "ON":
            print("Opening")
            ser = serial.Serial(port=port,baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
            ser.write(b'\x21\x89\x01\x50\x57\x31\x0A')
            reply = ser.read(6)
            if reply == b'\x06\x89\x01\x50\x57\x0A': 
                client.publish(my_topic+"/switch/"+object_id+"/state","ON", retain=True)
            else:
                print("Wrong reply")
            ser.close()
    elif command == "OFF":
            print("Closing")
            ser = serial.Serial(port=port,baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
            ser.write(b'\x21\x89\x01\x50\x57\x30\x0A')
            reply = ser.read(6)
            if reply == b'\x06\x89\x01\x50\x57\x0A': 
                client.publish(my_topic+"/switch/"+object_id+"/state","OFF", retain=True)
            else:
                print("Wrong reply")
            ser.close()
    else:
            print("WTF")

########################################

print("creating new instance")
client = mqtt.Client(my_topic+"_"+ object_id)
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address)

print("Subscribing to topic",my_topic+"/switch/"+object_id+"/set")
client.subscribe(my_topic+"/switch/"+object_id+"/set")

print("Publishing discovery message to topic",discovery_topic+"/switch/"+object_id+"/config")
config_data = {
    "~": my_topic+"/switch/"+object_id, 
    "name": object_name, 
    "cmd_t": "~/set", 
    "stat_t": "~/state",
    "device": {
        "name": "Pioneer Kuro KRF-9000FD",
        "manufacturer": "Pioneer",
        "model": "KRF-9000FD", 
        "identifiers":["JVC2MQTT_"+port]
#	"connections": [ "port", port ]
        }
    }
print (json.dumps(config_data))
client.publish(discovery_topic+"/switch/"+object_id+"/config",json.dumps(config_data), retain=True)

print("connecting to projector")
ser = serial.Serial(port=port,baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
ser.write(b'\x21\x89\x01\x00\x00\x0A')
reply = ser.read(6)
if reply == b'\x06\x89\x01\x00\x00\x0A': 
    print("connection to projector OK")
else:
    print("connection to projector not OK")
print("Check state")
ser.write(b'\x3F\x89\x01\x50\x57\x0A')
reply = ser.read(6)
if reply == b'\x06\x89\x01\x50\x57\x0A': 
    print("Reply OK")
else:
    print("Reply not OK")
reply = ser.read(7)
if reply == b'\x40\x89\x01\x50\x57\x31\x0A': 
    print("Power on")
    client.publish(my_topic+"/switch/"+object_id+"/state","ON", retain=True)
elif reply == b'\x40\x89\x01\x50\x57\x30\x0A': 
    print("Standby")
    client.publish(my_topic+"/switch/"+object_id+"/state","OFF", retain=True)
else: 
    print("Wrong reply")
ser.close()

#print("Publishing message to topic",my_topic+"/switch/"+object_id+"/set")
#client.publish(my_topic+"/switch/"+object_id+"/set","ON")
#client.publish(my_topic+"/switch/"+object_id+"/set","OFF")

client.loop_forever()
