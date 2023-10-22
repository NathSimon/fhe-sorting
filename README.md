# SR2I209 - Projet : Tri sur données chiffrées  

Projet réalisé dans le cadre de l'UE SR2I309 par Hamza Zarfaoui et Nathanaël SIMON.

Le but de ce projet est de mettre en place une communication client/serveur pour permettre le tri de données chiffrées. On putilisera pour se faire le chiffrement homomorphique.

Les opérations cryptographiques ont été réalisées en utilisant la bibliothèque de l'entreprise [Zama.ai](https://www.zama.ai/).

## Client

### Chiffrement des données

#### Création du circuit homomorphique

### Génération des clés

### Envoie du fichier des données chiffrées

### Récupération des données chiffrées

### Analyse du résultat

## Server

### Mise en place

### Calcul sur les données chiffrées

## Installation

Clone du projet puis intallation des dépendances

``` bash
git clone https://github.com/NathSimon/fhe-sorting.git
pip install -r requirements.txt
```

### Sur votre machine locale

Lancer dans deux terminaux différents :

``` bash
python3 server/app.py
```

``` bash
python3 client/client.py
```

Par défaut le serveur se lance sur [localhost](http://localhost:8080) mais ceci peut être modifié dans les paramètres du de server.py et dans l'url server dans client.py.

### Sur la VM

### TODO = Docker  
