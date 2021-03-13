import json
import logging
import paho.mqtt.client as mqtt
from time import sleep


class MatrixClient:

    def __init__(self, mqtt_server_host, mqtt_port=1883, main_topic="matrix"):
        connected = False
        self.main_topic = main_topic

        while not connected:
            try:
                self.client = mqtt.Client()
                self.client.connect(mqtt_server_host, mqtt_port)
                self.client.loop_start()
                connected = True
                print("Connected")
            except Exception as ex:
                print(f"Failed to connect to MQTT server {ex}")
                sleep(30)

    def _send_msg(self, topic, content):
        self.client.publish(f"{self.main_topic}/{topic}", json.dumps(content), 2)

    # value should always be false, if not, there is a problem
    def set_issue_state(self, device_id, key, has_issue):
        logging.debug(f"device_id: {device_id} key: {key} has_issue: {has_issue}")
        msg = {"key": key, "has_issue": has_issue, "device_id": device_id}
        self._send_msg(f"issue_state/{device_id}/{key}", msg)

    def set_sensor_state(self, device_id, key, value):
        logging.debug(f"SENSOR_STATE | device_id: {device_id}  {key}={value}")

        msg = {"key": key, "value": value, "device_id": device_id}
        self._send_msg(f"sensor_state/{device_id}/{key}", msg)

    def set_daily_measurement(self, device_id, date, key, value):
        logging.debug(f"DAILY_MEASUREMENT | device_id: {device_id} date: {date} {key}={value}")

        msg = {"key": key, "value": value, "date": date, "device_id": device_id}
        self._send_msg(f"daily_measurement/{device_id}/{key}", msg)
