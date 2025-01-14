from src.publisher import MQTTPublisher
from src.config import TOPIC_BASE
import time

publisher = MQTTPublisher()
publisher.connect()

try:
    for i in range(5):
        message = f"Hello World {i}"
        publisher.publish(TOPIC_BASE, message)
        time.sleep(1)
finally:
    publisher.disconnect()