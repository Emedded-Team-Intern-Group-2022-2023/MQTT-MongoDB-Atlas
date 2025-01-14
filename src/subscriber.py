import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from . import config

class MQTTSubscriber:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        # Initialize MongoDB connection
        self.mongo_client = MongoClient(config.MONGODB_URI)
        self.db = self.mongo_client[config.DATABASE_NAME]
        self.collection = self.db[config.COLLECTION_NAME]
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.client.subscribe(config.TOPIC)
        else:
            print(f"Failed to connect, return code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            # Parse the JSON message
            payload = json.loads(msg.payload.decode())
            
            # Add timestamp
            payload['timestamp'] = datetime.utcnow()
            payload['topic'] = msg.topic
            
            # Insert into MongoDB
            self.collection.insert_one(payload)
            print(f"Stored message in MongoDB: {payload}")
            
        except json.JSONDecodeError:
            print(f"Error decoding JSON message: {msg.payload.decode()}")
        except Exception as e:
            print(f"Error storing message in MongoDB: {str(e)}")

    def connect(self):
        self.client.connect(config.BROKER_ADDRESS, config.BROKER_PORT, config.KEEPALIVE)

    def start(self):
        self.client.loop_forever()

    def stop(self):
        self.client.disconnect()
        self.mongo_client.close()