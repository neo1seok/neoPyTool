import paho.mqtt.client as mqtt
import time
import ssl

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" ########"+str(msg.payload))

client = mqtt.Client(client_id="cl3",protocol=mqtt.MQTTv31)

#client.tls_set(ca_certs='D:\PROJECT\RASPBERRY\ca.crt',tls_version=ssl.PROTOCOL_TLSv1)




client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.103", 1883, 60)

#client.loop_start()

#client.subscribe('paho/fuck2')

idx = 0
# while True:
# 	idx += 1

while True:
	client.publish("paho/fuck", "test publish %d"%idx)
	client.publish("paho/fuck3", "test publish %d" % idx)


	idx += 1
	time.sleep(1)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()