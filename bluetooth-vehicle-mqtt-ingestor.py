import json
import paho.mqtt.client as mqtt
import datetime
import csv

column_names = ['rssi', 'datetime']

# Open configuration json file
with open('config.json', 'r') as configfile:
    # Reading from json file
    config_dict = json.load(configfile)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config_dict['mqtt_topic'])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    rssi_distance_data = {}
    rssi_distance_data['rssi'] = msg.payload
    rssi_distance_data['datetime'] = datetime.datetime.now()

    with open('rssi_distance_data.csv', 'a') as csv_file:
        dict_object = csv.DictWriter(csv_file, fieldnames=column_names)
        dict_object.writerow(rssi_distance_data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config_dict['mqtt_broker_ip'], 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
