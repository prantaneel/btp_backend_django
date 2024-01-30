import os
from django.conf import settings
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to broker
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)  # Enforce TLS 1.2 or newer
        self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
        self.client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print("Failed to connect, return code %d\n", rc)
    @staticmethod
    def on_message(client, userdata, message):
        print("Received message:", message.payload.decode())
        # Process received messages here
        
    def publish(self, topic, message, retain=False):
        print(message)
        self.client.publish(topic=topic, payload=message, retain=retain, qos=1)

    def subscribe(self, topic):
        self.client.subscribe(topic)
    
    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()