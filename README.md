# JVC2MQTT
Control JVC/Pioneer projector with serial and control it as switch in Home Assistant
This is tested with Pioneer Kuro KRF-9000FD which is rebranded version of JVC DLA-HD2. 

Create /home/pi/jvc2mqtt dir and place files there. 

Might have to install Paho. 
```
pip3 install paho-mqtt
```

Update jvc2mqtt.py with your environment
```
# Address of your MQTT broker server
broker_address="homeautomation"

# Homeassistant discovery topic (normally no need to change ) 
discovery_topic="homeassistant"

# This scripts own topic. No need to change. 
my_topic="JVC2MQTT"

# Serial port for your projector. I use udev to name ports
port="/dev/projector"

# Name of the projector. Can run several projectors in same environment
object_name="Living Room Projector"
object_id="living_room_projector"
```


Can run directly 
```
python3 jvc2mqtt.py
```
Or start as service
```
sudo cp jvc2mqtt.service /etc/systemd/system
systemctl enable jvc2mqtt
systemctl restart jvc2mqtt
systemctl status jvc2mqtt
```
