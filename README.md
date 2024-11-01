#mettre a jour paquet
apt-get update
#installer gnome
sudo apt install gnome-terminal
#installer Docker
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

#Ajoutez la clé GPG de Docker :
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#Ajoutez le dépôt Docker :
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
#Mettez à jour à nouveau la liste des paquets :
sudo apt-get update
#Installez Docker: Vous le pouvez maintenant installer Docker avec la commande suivante :
sudo apt-get install docker-ce
#Installer kubernetes
 curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
# creer le projet dans service (srv)
cd /srv/projet-kubernetes


# Créer les dossiers principaux
mkdir -p manifests/deployments
mkdir -p manifests/services
mkdir -p manifests/ingress
mkdir -p configs/nginx
mkdir -p configs/db
mkdir scripts
mkdir volumes

# Créer un fichier README.md
touch README.md

# Créer un fichier .gitignore
touch .gitignore

docker image prune
#pour supprimer images non utilisees par un conteneur
docker image prune

#.1 Appliquer le Namespace
kubectl apply -f YAML-STANDARD/namespace.yaml

#.2 Appliquer les Secrets
kubectl apply -f YAML-STANDARD/secret-postgres.yaml
#.3 Appliquer les Déploiements
kubectl apply -f YAML-STANDARD/deployments/deployment-postgres.yaml
kubectl apply -f YAML-STANDARD/deployments/deployment-pgadmin.yaml
kubectl apply -f YAML-STANDARD/deployments/deployment-fastapi.yaml

#.4 Appliquer les Services
kubectl apply -f YAML-STANDARD/services/service-postgres.yaml
kubectl apply -f YAML-STANDARD/services/service-pgadmin.yaml
kubectl apply -f YAML-STANDARD/services/service-fastapi.yaml#
#.5 Appliquer l'Horizontal Pod Autoscaler (HPA) (si nécessaire)
kubectl apply -f YAML-STANDARD/deployments/hpa-fastapi.yaml

#.6 Appliquer l'Ingress (si nécessaire)
kubectl apply -f YAML-STANDARD/deployments/ingress-fastapi.yaml

#. Vérifier l'État des Ressources
Après avoir appliqué toutes les configurations, vérifiez l'état des pods et des services pour vous assurer qu'ils fonctionnent correctement :
kubectl get pods --namespace=standard
kubectl get services --namespace=standard
 
1. PostgreSQL Deployment

Rôle : Ce fichier définit le déploiement de la base de données PostgreSQL.

    apiVersion: Définit la version de l'API Kubernetes utilisée pour ce déploiement (ici, apps/v1).
    kind: Indique le type de ressource à créer (ici, Deployment).
    metadata: Contient des informations sur le déploiement, comme son nom (postgres).
    spec: Définit les spécifications du déploiement, notamment :
        replicas: Nombre d'instances de PostgreSQL à exécuter (ici, 1).
        selector: Labels utilisés pour sélectionner les pods gérés par ce déploiement.
        template: Modèle pour créer les pods, qui inclut :
            containers: Définit le conteneur PostgreSQL, y compris son image, les variables d'environnement (utilisateur, mot de passe, base de données, méthode d'authentification) et les ports exposés.
            volumeMounts: Monte un volume pour stocker les données de manière persistante.
    volumes: Définit un volume nommé qui utilise un PersistentVolumeClaim (PVC) pour la persistance des données.

2. PostgreSQL Service

Rôle : Ce fichier définit le service qui exposera PostgreSQL à d'autres applications dans le cluster.

    apiVersion: Version de l'API Kubernetes pour le service (v1).
    kind: Type de ressource (ici, Service).
    metadata: Informations sur le service, comme son nom (postgres).
    spec: Spécifications du service, y compris :
        ports: Définit le port sur lequel le service écoutera (5432).
        selector: Correspond à des pods ayant un label spécifique (ici, app: postgres) pour diriger le trafic vers le bon déploiement.

3. FastAPI Deployment

Rôle : Ce fichier définit le déploiement de l'application FastAPI.

    apiVersion: Version de l'API Kubernetes utilisée pour ce déploiement (ici, apps/v1).
    kind: Type de ressource (ici, Deployment).
    metadata: Contient des informations sur le déploiement, comme son nom (fastapi).
    spec: Définit les spécifications du déploiement, notamment :
        replicas: Nombre d'instances de FastAPI à exécuter (ici, 1).
        selector: Labels utilisés pour sélectionner les pods gérés par ce déploiement.
        template: Modèle pour créer les pods, qui inclut :
            containers: Définit le conteneur FastAPI, y compris son image, les ports exposés, et la variable d'environnement DATABASE_URL pour se connecter à PostgreSQL.

4. FastAPI Service

Rôle : Ce fichier définit le service qui exposera l'application FastAPI à l'extérieur du cluster ou à d'autres services internes.

    apiVersion: Version de l'API Kubernetes pour le service (v1).
    kind: Type de ressource (ici, Service).
    metadata: Informations sur le service, comme son nom (fastapi).
    spec: Spécifications du service, y compris :
        type: Type de service (LoadBalancer ou NodePort), qui détermine comment le service sera exposé.
        ports: Définit le port sur lequel le service écoutera (5000) et le port cible sur le pod (également 5000).
        selector: Correspond à des pods ayant un label spécifique (ici, app: fastapi) pour diriger le trafic vers le bon déploiement.

5. PersistentVolumeClaim pour PostgreSQL

Rôle : Ce fichier définit une demande de volume persistant qui sera utilisé par PostgreSQL pour stocker ses données de manière durable.

    apiVersion: Version de l'API Kubernetes utilisée pour le PVC (v1).
    kind: Type de ressource (ici, PersistentVolumeClaim).
    metadata: Informations sur le PVC, comme son nom (postgres-pvc).
    spec: Spécifications du PVC, y compris :
        accessModes: Définit comment le volume peut être utilisé (ici, ReadWriteOnce, ce qui signifie que le volume peut être monté en lecture-écriture par un seul nœud).
        resources: Indique les ressources demandées, ici, une capacité de stockage de 1 GiB.
Pour déployer vos configurations Kubernetes, voici les étapes à suivre :

    Vérifiez votre configuration de cluster : Assurez-vous que votre cluster Kubernetes est prêt et fonctionne. Vous pouvez vérifier en listant les nœuds du cluster :

    bash

kubectl get nodes

Créer les objets Kubernetes : Utilisez kubectl apply -f <chemin_du_fichier> pour appliquer vos fichiers de configuration. Vous pouvez appliquer chaque fichier individuellement ou bien appliquer tout un répertoire.

Par exemple, pour le rou d'eau, tous les fichiers sous le répertoiremanifests et le volume PostgreSQL :

bash

kubectl apply -f /srv/projet-kubernetes/volumes/persistentVolumeClaim-postgreSQL.yaml
kubectl apply -f /srv/projet-kubernetes/manifests/deployments/fastapi-deployment.yaml
kubectl apply -f services/postgreSQL-service.yaml
kubectl apply -f services/fastapi-service.yaml
kubectl apply -f services/PGAdmin-service.yaml


érifier le statut des déploiements et services : Une fois les fichiers appliqués, vérifiez que les déploiements et services sont correctement créés.

bash

kubectl get deployments
kubectl get services

Vous pouvez aussi inspecter les pods pour vous assurer qu’ils sont bien créés et qu’ils n’ont pas d’erreurs :

bash

kubectl get pods
docker images
REPOSITORY      TAG       IMAGE ID       CREATED        SIZE
fastapi-image   latest    69a63e0b5077   10 hours ago   486MB



#se placer dans app pour acceder au Dockerfile
docker login -u julh62

#«Construire l'image
docker build -t julh62/exam-kubernetes_fastapi:latest .

#Pousse
docker push julh62/exam-kubernetes_fastapi:latest

#changer le nom de l'imge dans le fichier de deployment de fastapi
containers:
- name: fastapi
  image: docker.io/library/fastapi-image:latest 
#appliquer les changeemnts et redeployer
 kubectl apply -f /srv/projet-kubernetes//manifests/deployments/fastapi-deployment.yaml

# verifier connexion à la base de données
kubectl exec -it <nom_du_pod_postgresql> -- /bin/bash

#Tester la Connexion : Une fois à l'intérieur,
# vous pouvez essayer de vous connecter à PostgreSQL avec le client psql :
psql -h localhost -U admin storedb
