# SR2I209 - Projet : Calcul sur données chiffrées dans un cloud

Projet réalisé dans le cadre de l'UE SR2I309 par Hamza Zarfaoui et Nathanaël SIMON.

Le but de ce projet est de mettre en place une communication client/serveur pour permettre le tri de données chiffrées. On putilisera pour se faire le chiffrement homomorphique.

Les opérations cryptographiques ont été réalisées en utilisant la bibliothèque de l'entreprise [Zama.ai](https://www.zama.ai/).

## Circuit

### Circuits implémentés

Lors de ce projet nous avons réalisé les implémentations des algorithmes de tris suivants, adaptés au chiffrement homomorphique.

- Bubble Sort
- Insertion Sort - todo
- Merge Sort - todo
- Quick Sort - todo
- Tim Sort - todo
- Tree Sort - todo
- Heap Sort - todo

### Compilation des circuits

Pour compiler un circuit il suffit d'executer son script python correspondant. Ce dernier enregistrera un fichier .zip de ce circuit sous `circuits/compiled_circuits`, ainsi que dans le répertoire `server/ciruits` pour faciliter le portage des fichiers sources.

Exemple :

```bash
pyton3 circuits/bubble_sort_circuit_chunked.py
```

### Particularité du chiffrement homomorphique pour la comparaison

L'opération la plus couteuse en lors du calcul sur données chiffrées est la comparaison entre deux élements. Celle-ci s'effectue principalement autour de Table Look Ups (TLU) et zama propose plusieurs stratégies pour utiliser ces TLU.

Nous en utiliserons 3 en démonstration sur le bubble sort:

- Chuncked
  - Stratégie par défaut
  - Fonctionne avec tous les integers sans augmentation de l'expension de chiffrement
  - Très couteux, entre 5 et 13 TLU par comparaison
- ONE_TLU_PROMOTED
  - Minimise à un TLU par comparaison
  - Augmente la taille des données chiffrées, ce qui peut ralentir d'autres opérations et augmente l'espace de stockage nécessaire
- THREE_TLU_CASTED
  - Entre 1 et 3 TLU par comparaison
  - N'augmente pas la taille des données chiffrées

Zama propose également d'autres stratégies qui vont proposer d'autres avatanges et inconvénients compris entre les 3 stratégies testées ici.

### Comparaison entre les stratégies

Pour notre cas d'usage ou nous allons seulement trier les données et pas effectuer d'autres opération dessus, l'exepention du chiffrement ne représente pas une contrainte importante, si ce n'est pour la taille des fichiers que nous allons échanger avec le serveur. Nous allons donc choisir de favoriser la performance des différents algorithmes de tris en utilsant la stratégie ONE_TLU_PROMOTED, mais celle-ci est a adapter en fonction du cas d'usage et des contraites du système développé.

Le détail des résultats des comparaisons entre les stratégies de comparaisons peut être trouvé dans le rapport du projet.

## Déroulement de l'opération de tri entre un client et un serveur

- Côté client
  - Génération des données à trier
  - Demande au serveur des specification cryptographiques nécessaires
  - Envoie d'une clé d'évaluation
  - Chiffrement des données et envoie d'un fichier chiffré

- Côté serveur
  - Récéption du fichier chiffré
  - Exécution du circuit chargé au lancement du serveur
  - Enregistrement des résultats dans un autre fichier chiffré
  - Informe le client de la fin de l'execution du tri

- Côté client
  - Téléchargement du fichier des résultats
  - Déchiffrement
  - Vérification du tri

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
docker run docker run -p <port>:8080 -d --name <nameOfContainer> <name>:<version>
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
scp -r server/* ubuntu@fhe1.r2.enst.fr:XXX 
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
