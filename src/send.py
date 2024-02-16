import ujson
import urequests
from umqtt.simple import MQTTClient

# LINE通知設定
LINE_NOTIFY_TOKEN = "R7WNHLMFeN1WhDyF7xEilffbE2Imqyzg9QylqZMcxcs"

# MQTT設定
MQTT_BROKER = "192.168.3.6"
MQTT_TOPIC = b"sensor_data"

def send_line_notification(message):
    endpoint = 'https://notify-api.line.me/api/notify'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
    data = f'message={message}'.encode('utf-8')
    response = urequests.post(endpoint, headers=headers, data=data)
    response.close()

def send_mqtt_data(temperature, co2_level):
    client = MQTTClient("pico", MQTT_BROKER)
    #client.connect()
    
    try:
        client.connect()
        print("Connected to broker")
        data = {"temperature": temperature, "co2_level": co2_level}
        client.publish(MQTT_TOPIC, ujson.dumps(data))
        client.disconnect()
        print("Disconnected from broker")
    except OSError as e:
        print("Couldn't connect to broker:", e)
    
    
