import pulumi
import pulumi_docker as docker

network = docker.Network("notom-network", name="notom-network")

app_image = docker.Image("notom-app-image",
    build=docker.DockerBuildArgs(
        context="..",
    ),
    image_name="notom-app:latest",
    skip_push=True
)

mosquitto = docker.Container("mosquitto",
    image="eclipse-mosquitto:1.6.15",
    name="mosquitto", # Ce nom devient officiellement son "adresse IP" dans le réseau virtuel !
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    ports=[docker.ContainerPortArgs(internal=1883, external=1883)]
)

agent = docker.Container("agent-ia",
    image=app_image.image_name,
    command=["python", "-u", "agent.py"],
    envs=["MQTT_BROKER=mosquitto"], # On injecte l'adresse du broker
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    opts=pulumi.ResourceOptions(depends_on=[mosquitto]) # Pulumi doit attendre que le broker soit allumé
)

simulateur = docker.Container("simulateur-moteur",
    image=app_image.image_name,
    command=["python", "-u", "sim.py"],
    envs=["MQTT_BROKER=mosquitto"],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    opts=pulumi.ResourceOptions(depends_on=[agent]) # On allume le simulateur en tout dernier
)

influxdb = docker.Container("influxdb",
    image="influxdb:1.8",
    name="influxdb",
	envs=["INFLUXDB_DB=usine"],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    ports=[docker.ContainerPortArgs(internal=8086, external=8086)]
)

grafana = docker.Container("grafana",
    image="grafana/grafana:latest",
    name="grafana",
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(name=network.name)],
    ports=[docker.ContainerPortArgs(internal=3000, external=3000)],
    opts=pulumi.ResourceOptions(depends_on=[influxdb])
)

pulumi.export("nom_du_reseau_cree", network.name)