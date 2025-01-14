from src.subscriber import MQTTSubscriber

subscriber = MQTTSubscriber()
subscriber.connect()

try:
    subscriber.start()
except KeyboardInterrupt:
    subscriber.stop()