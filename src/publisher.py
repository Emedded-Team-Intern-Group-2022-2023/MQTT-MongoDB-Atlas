import paho.mqtt.client as mqtt
from datetime import datetime
from . import config

class MQTTPublisher:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_publish = self._on_publish
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    def _on_publish(self, client, userdata, mid):
        print(f"Message ID {mid} published")

    def connect(self):
        self.client.connect(config.BROKER_ADDRESS, config.BROKER_PORT, config.KEEPALIVE)
        self.client.loop_start()

    def publish(self, topic, message):
        result = self.client.publish(topic, message, qos=config.QOS_LEVEL)
        result.wait_for_publish()
        return result.is_published()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()