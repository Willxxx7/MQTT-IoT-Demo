import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "localhost"
TOPIC = "sensor/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, 1883, 60)

print("IoT Sensor started")
print("Publishing to:", TOPIC)
print()

try:
    while True:

        temperature = round(random.uniform(18.0, 28.0), 1)
        humidity = random.randint(40, 80)
        light = random.randint(100, 900)

        sensor_data = {
            "temperature": temperature,
            "humidity": humidity,
            "light": light
        }

        payload = json.dumps(sensor_data)

        client.publish(TOPIC, payload)

        print("Published:", payload)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nSensor stopped.")

finally:
    client.disconnect()