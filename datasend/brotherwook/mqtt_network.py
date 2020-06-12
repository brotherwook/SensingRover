from datasend.brotherwook.publisher import MqttPublisher
from datasend.brotherwook.subscriber import MqttSubscriber

publisher = MqttPublisher("192.168.3.179", topic="/sensor")
subscriber = MqttSubscriber("192.168.3.179", topic="/command")

publisher.start()
subscriber.start()