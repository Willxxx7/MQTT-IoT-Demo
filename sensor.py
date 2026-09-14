import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "localhost"
TOPIC = "sensor/data"

# For this classroom demonstration, we send 30 readings and then stop.
# In a real IoT system, a sensor could continue sending data for hours,
# days, months or even years, depending on the application and power supply.

NUMBER_OF_READINGS = 30


def generate_sensor_data():
    temperature = round(random.uniform(18.0, 28.0), 1)
    humidity = random.randint(40, 80)
    light = random.randint(100, 900)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "light": light
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.connect(BROKER, 1883, 60)

    print("IoT Sensor started")
    print("Publishing to:", TOPIC)
    print(f"Sending {NUMBER_OF_READINGS} readings...")
    print()

    try:
        for reading in range(1, NUMBER_OF_READINGS + 1):

            sensor_data = generate_sensor_data()

            payload = json.dumps(sensor_data)

            client.publish(TOPIC, payload)

            print(f"Reading {reading}/{NUMBER_OF_READINGS}: {payload}")

            time.sleep(2)

        print("\nSensor finished.")

    except KeyboardInterrupt:
        print("\nSensor stopped.")

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
