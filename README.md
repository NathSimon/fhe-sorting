# SR2I209 - Projet : Calcul sur données chiffrées dans un cloud

Projet réalisé dans le cadre de l'UE SR2I309 par Hamza Zarfaoui et Nathanaël SIMON.

Le but de ce projet est de mettre en place une communication client/serveur pour permettre le tri de données chiffrées. On putilisera pour se faire le chiffrement homomorphique.

Les opérations cryptographiques ont été réalisées en utilisant la bibliothèque de l'entreprise [Zama.ai](https://www.zama.ai/).

## Circuit

### Particularité du chiffrement homomorphique pour la comparaison

### Création du circuit homomorphique

### Circuits implémentés

- Bubble Sort

## Server

### Mise en place

### Calcul sur les données chiffrées

## Client

### Chiffrement des données

### Génération des clés

### Envoie du fichier des données chiffrées

### Récupération des données chiffrées

### Analyse du résultat

## Installation

Clone du projet puis intallation des dépendances pour le client.

``` bash
git clone https://github.com/NathSimon/fhe-sorting.git
pip install -r client/requirements.txt
```

Pour le serveur la procédure est décrite ci dessous.

### Lancer l'application depuis votre machine locale  

Il est possible d'utiliser soit python directement soit docker pour lancer le serveur.

Lancer depuis python :

``` bash
pip install -r server/requirements.txt
python3 server/app.py
```

Par défaut le serveur se lance sur [localhost](http://localhost:8080) qu port 8080 mais ceci peut être modifié dans les paramètres du de server.py et dans l'url server dans client.py.

Il est également possible d'utiliser Docker pour lancer le serveur avec le Dockerfile fourni. Celui expose son port 8080, qu'il faudra mapper avec un port de la machine hôte, conformément à l'adresse donnée au client.

``` bash
docker build -t <name>:<version>  .
docker run docker run -p <port>:8080 -d --name <name> <name>:<version>
```

Example :

``` bash
docker build -t fhesorting:bubblesort  .
docker run docker run -p 8080:8080 -d --name fhe fhesorting:bubblesort
```

Ici sera créé une image fhesorting, puis un contenaire nommé fhe depuis l'image qui mappe son port 8080 au port 8080 de la machine. Il est par la suite possible de communiquer avec le serveur à l'adresse [localhost](http://localhost:8080) au port 8080.

Pour exécuter le client, il suffit de lancer le script suivant :

``` bash
python3 client/client.py
```

### Sur les VMs mise à disposition

Il faut avoir une clé ssh publique enregistrée sur une des deux VMs misent a disposition, ```ubuntu@fhe1.r2.enst.fr``` ou ```ubuntu@fhe2.r2.enst.fr```
Pour vous y connecter en ssh depuis le réseau de l'école ou bien son vpn :

Il faut par la suite upload les fichiers sources serveur du projet :

``` bash
scp -r server ubuntu@fhe1.r2.enst.fr:XXX 
```

Puis se connecter au serveur en ssh et lancer le serveur depuis une des précédentes méthodes.

``` bash
ssh ubuntu@fhe1.r2.enst.fr
docker ou pyton3
```

Enfin, changer l'addresse dans le client par :

```pyton
serveur_url = ubuntu@fhe1.r2.enst.fr:<port>
```
