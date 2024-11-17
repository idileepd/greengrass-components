import time
import traceback
import json
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    PublishToIoTCoreRequest,
    SubscribeToIoTCoreRequest,
)
from logger_util import Logger

# Seconds
TIMEOUT = 10


class GreengrassTopicPublisher:
    def __init__(self, device_id, topic=None, qos=QOS.AT_LEAST_ONCE):
        self.topic = topic
        self.qos = qos
        self.ipc_client = awsiot.greengrasscoreipc.connect()
        self.logger = Logger(device_id)

    def set_default_topic(self, topic):
        self.topic = topic

    def publish(self, message, topic=None):
        try:
            if not topic:
                topic = self.topic
            if not topic:
                raise ValueError("Publish topic not provided")

            msgstring = json.dumps(message)
            pubrequest = PublishToIoTCoreRequest()
            pubrequest.topic_name = topic
            pubrequest.payload = bytes(msgstring, "utf-8")
            pubrequest.qos = self.qos
            operation = self.ipc_client.new_publish_to_iot_core()
            operation.activate(pubrequest)
            future = operation.get_response()
            future.result(TIMEOUT)
            self.logger.log(f"Published to {topic}: {message}")
        except Exception as e:
            self.logger.log(f"Failed to publish to {topic}: {e}")

class GreengrassTopicSubscriber:
    def __init__(self, device_id, topic=None, qos=QOS.AT_MOST_ONCE):
        self.topic = topic
        self.qos = qos
        self.ipc_client = awsiot.greengrasscoreipc.connect()
        self.logger = Logger(device_id)

    def set_default_topic(self, topic):
        self.topic = topic

    def subscribe(self, callback, topic=None):
        try:
            if not topic:
                topic = self.topic
            if not topic:
                raise ValueError("Subscribe topic not provided")

            handler = SubHandler(callback, self.logger)
            subrequest = SubscribeToIoTCoreRequest()
            subrequest.topic_name = topic
            subrequest.qos = self.qos
            operation = self.ipc_client.new_subscribe_to_iot_core(handler)
            future = operation.activate(subrequest)
            future.result(TIMEOUT)
            self.logger.log(f"Subscribed to {topic}")
        except Exception as e:
            self.logger.log(f"Failed to subscribe to {topic}: {e}")

class SubHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self, callback, logger):
        super().__init__()
        self.callback = callback
        self.logger = logger

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            message = str(event.message.payload, "utf-8")
            self.callback(event.message.topic_name, json.loads(message))
            self.logger.log(f"Received message on topic {event.message.topic_name}: {message}")
        except:
            self.logger.log("Error processing message")
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        self.logger.log(f"Stream error: {error}")
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        self.logger.log("Stream closed")
