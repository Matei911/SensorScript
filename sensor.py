#!/usr/bin/env python3

import random
import time
import json
import paho.mqtt.client as mqtt
import signal
import sys

# Function to simulate temperature readings
def simulate_temperature():
    return round(random.uniform(20.0, 25.0), 2)

# Function to simulate air quality readings
def simulate_air_quality():
    return round(random.uniform(0.0, 100.0), 2)

# MQTT Configuration
mqtt_broker = "82.78.81.188"
mqtt_port = 1883
mqtt_topic = "/training/device/Matei-Calugaru/"

client = mqtt.Client()

# Reconnect delay settings
initial_delay = 1
max_delay = 60
reconnect_delay = initial_delay

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        global reconnect_delay
        reconnect_delay = initial_delay  # Reset the reconnect delay on successful connection
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")
    try_reconnect(client)

def try_reconnect(client):
    global reconnect_delay
    while True:
        try:
            print(f"Attempting to reconnect in {reconnect_delay} seconds...")
            time.sleep(reconnect_delay)
            client.reconnect()
            break
        except Exception as e:
            print(f"Reconnect failed: {e}")
            reconnect_delay = min(reconnect_delay * 2, max_delay)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

def signal_handler(sig, frame):
    print('Disconnecting from MQTT broker...')
    client.disconnect()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()  # Start the loop

    while True:
        temperature = simulate_temperature()
        air_quality = simulate_air_quality()

        sensor_data = json.dumps({
            "temperature": temperature,
            "air_quality": air_quality
        })

        client.publish(mqtt_topic, sensor_data)
        print(f"Published: {sensor_data}")

        time.sleep(60)

except KeyboardInterrupt:
    signal_handler(None, None)

print("Simulation stopped")
