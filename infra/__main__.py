import pulumi
import pulumi_docker as docker

network = docker.Network("notom-network", name="notom-network")

mosquitto = docker.Container("mosquitto",
    image="eclipse-mosquitto:1.6.15",
    name="mosquitto", # Ce nom devient officiellement son "adresse IP" dans le réseau virtuel !
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    ports=[docker.ContainerPortArgs(internal=1883, external=1883)]
)

agent = docker.Container("agent-ia",
    image="notom-app:latest",
    command=["python", "-u", "agent.py"],
    envs=["MQTT_BROKER=mosquitto"], # On injecte l'adresse du broker
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    opts=pulumi.ResourceOptions(depends_on=[mosquitto]) # Pulumi doit attendre que le broker soit allumé
)

simulateur = docker.Container("simulateur-moteur",
    image="notom-app:latest",
    command=["python", "-u", "sim.py"],
    envs=["MQTT_BROKER=mosquitto"],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    opts=pulumi.ResourceOptions(depends_on=[agent]) # On allume le simulateur en tout dernier
)

pulumi.export("nom_du_reseau_cree", network.name)