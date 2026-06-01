import time
import random
import paho.mqtt.client as mqtt
import os

broker = os.getenv("MQTT_BROKER", "localhost")
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Simulateur_Moteur")

print(f"Connexion de la machine au réseau industriel (Broker: {broker})...")
client.connect(broker, 1883)

while True:
    temp = random.choice([random.randint(30, 45), random.randint(75, 95)])
    topic = "usine/moteur/temperature"

    client.publish(topic, str(temp))
    print(f"Capteur -> Donnée envoyée sur '{topic}' : {temp}°C")

    time.sleep(3)