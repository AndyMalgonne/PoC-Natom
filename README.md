# NOTOM - POC Edge AI & Convergence OT/IT

Ce projet est un Démonstrateur (Proof of Concept) illustrant le déploiement d'une architecture Edge-to-Cloud intelligente. Il simule une chaîne de transmission de données industrielles en temps réel, couplée à une intelligence artificielle générative pour la détection et la qualification d'anomalies.

## Objectifs du Projet

1. **Convergence OT/IT :** Relier le monde physique de l'usine (Operation Technology) aux systèmes d'information (Information Technology) via un standard industriel.
2. **Edge AI :** Déployer une passerelle intelligente capable de filtrer la donnée en périphérie de réseau et d'interroger un LLM en cas de besoin critique.
3. **Infrastructure as Code (IaC) :** Garantir un déploiement agnostique, répétable et automatisé de l'ensemble de la stack.

---

## Architecture Technique

L'architecture repose sur 3 composants principaux conteneurisés et orchestrés de manière autonome :

* **Le Simulateur (OT) :** Un script Python (`sim.py`) simulant un capteur de température de moteur industriel. Il publie des données à fréquence régulière sur le réseau.
* **Le Réseau Industriel (IT) :** Un broker **MQTT (Mosquitto)**, véritable système nerveux de l'architecture, assurant une communication asynchrone, légère et en temps réel.
* **L'Agent IA (Edge/Cloud) :** Un script Python (`agent.py`) souscrivant aux données du capteur. En cas de dépassement de seuil (> 50°C), l'agent interroge l'API Hugging Face (modèle *Qwen2.5-72B-Instruct* avec routage dynamique `provider="auto"`) pour générer une alerte sémantique contextualisée.

---

## Stack Technologique & DevOps

Afin de répondre aux exigences de production, l'application est entièrement packagée et orchestrée :

* **Langage :** Python 3.11
* **Messagerie :** Eclipse Mosquitto (MQTT v2)
* **Intelligence Artificielle :** Hugging Face Inference API (Serverless, évitant le vendor lock-in)
* **Conteneurisation :** Docker (Création d'une image standardisée `notom-app`)
* **Orchestration / IaC :** Pulumi (Déploiement du réseau virtuel et des conteneurs via Python)

---

## Guide de Déploiement

Grâce à Pulumi, l'infrastructure complète se déploie en une seule ligne de commande.

### 1. Prérequis
* Docker Desktop en cours d'exécution.
* Pulumi installé et configuré (`pulumi login`).
* Une clé API Hugging Face dans un fichier `.env` (`HUGGINGFACE_API_KEY=hf_...`).

### 2. Démarrage de l'usine (Déploiement IaC)
Dans le dossier `infra` (avec l'environnement virtuel Pulumi activé) :
```bash
pulumi up