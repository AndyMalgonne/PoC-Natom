import os
import paho.mqtt.client as mqtt
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

#IA Config
load_dotenv()
hf_token = os.getenv("HUGGINGFACE_API_KEY")
if not hf_token:
    raise ValueError("Erreur : HUGGINGFACE_API_KEY manquante.")

hf_client = InferenceClient(
    model="Qwen/Qwen2.5-72B-Instruct",
    token=hf_token,
    provider="auto"
)

def on_message(client, userdata, msg):
    temperature = int(msg.payload.decode())
    print(f"\nAgent <- Nouvelle donnée reçue : {temperature}°C")

    if temperature > 50:
        print("⚠️ Surchauffe détectée ! Interrogation de l'IA...")
        prompt = (
            f"Tu es un agent de maintenance industriel. "
            f"Un capteur indique {temperature}°C au lieu de 40°C. "
            f"Rédige une seule phrase d'alerte technique très courte."
        )
        try:
            reponse = hf_client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=40
            )
            print("ALERTE GÉNÉRÉE PAR L'IA :")
            print(reponse.choices[0].message.content.strip())
        except Exception as e:
            print(f"Erreur réseau ou API : {e}")
    else:
        print("Statut normal, aucune action IA requise.")

broker = os.getenv("MQTT_BROKER", "localhost")
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Agent_IA")
mqtt_client.on_message = on_message

print(f"Connexion de l'Agent IA au réseau (Broker: {broker})...")
mqtt_client.connect(broker, 1883)

mqtt_client.subscribe("usine/moteur/temperature")

print("👂 L'Agent écoute le réseau en temps réel (Ctrl+C pour quitter)...")
mqtt_client.loop_forever()