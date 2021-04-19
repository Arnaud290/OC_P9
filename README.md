++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# PROJET 9 : Développez une application Web en utilisant Django

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Contexte

Création d'une application web pérmettant à des utilisateurs de demander des critiques de livres ou d'articles en créant un ticket et de publiser des critiques d'articles ou de livres. 

## Installation


### 1 - Installation de Python3, l'outil d'environnement virtuel,  le gestionnaire de paquets et sqlite3 (sur Linux UBUNTU)
    

    $ sudo apt-get install python3 python3-venv python3-pip sqlite3


### 2 - Mise en place de l'environnement virtuel "env"


    1 - Accès au répertoire du projet :
            
            exemple cd /projet_litreview

    2 - Création de l'environnement virtuel :
            
            $ python3 -m venv env


### 3 - Ouverture de l'environnement virtuel et ajout des modules


            $ source env/bin/activate
            
            (env) $ pip install -r requirements.txt
            

### 4 - Modification du fichier litreview/litreview/settings_exemple.py

    1 - Renomer le fichier settings_exemple.py en settings.py

    2 - modifier la variable 'SECRET_KEY' afin d'ajouter une clé de sécurité
        (53 caractaires aléatoires avec majuscule,
        minuscule, chiffres et caractaires spéciaux) 

    3 - modifier la variable 'DATABASES' afin d'ajouter
        le chemin vers la base de données

## Utilisation du programme


### 1 - Lancement


        
### 2 - Utilisation

    Afin de tester le site, 5 utilisateurs fictifs sont enregistés dans la base de donnée db.sqlite3
    - leon28
    - jean35
    - pierre3
    - claude20
    - lucie38
    le mot de passe pour les utilisateurs : P@ssword1
