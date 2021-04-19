++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# PROJET 9 : Développez une application Web en utilisant Django

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Contexte

Création d'une application web permettant à des utilisateurs de demander des critiques de livres ou d'articles en créant un ticket et de publier des critiques d'articles ou de livres. 

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

    2 - Modifier la variable 'SECRET_KEY' afin d'ajouter une clé de sécurité
        (53 caractères aléatoires avec majuscule,
        minuscule, chiffres et caractères spéciaux) 

    3 - Modifier la variable 'DATABASES' afin d'ajouter
        le chemin vers la base de données

            exemple:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
                }
            }

## Utilisation du programme


### 1 - Lancement

    1 - activation de l'environnement virtuel dans le répertoire de base:

        source env/bin/activate

    2 - accès au répertoire litreview:

        cd litreview/

    3 - Lancement du serveur Django

        ./manage.py runserver

    4 - Ouverture d'une page web
    
        Adresse: 127.0.0.1:8000

### 2 - Utilisation

    Afin de tester le site, 5 utilisateurs fictifs sont enregistrés avec quelques tickets et critiques
    dans la base de donnée "db.sqlite3" mise à disposition dans le repository : 

        - leon28
        - jean35
        - pierre3
        - claude20
        - lucie38

        le mot de passe pour les utilisateurs : P@ssword1


    Pour avoir une base de donnée initiale:

        1 - Arrêter le serveur Django en effectuant la combinaison :
                
                 control + c 

        2 - Supprimer le fichier "db.sqlite3"

        3 - effectuer la migration vers la nouvelle base

                ./manage.py makemigrations => Cela crée un fichier dans litreview/review/migrations 

                ./manage.py migrate => Création des tables dans le fichier "db.sqlite" (crée directement)
              
####  Création d'un utilisateur

    Sur la page 'Connexion' accessible depuis l'adresse "127.0.0.1:8000", un bouton "s'inscrire" permet 
    d'accéder à la page 'Inscription'.

    Sur cette page, on inscrit un nom qui sera l'identifiant et un mot de passe deux fois pour le confirmer.
    Ce mot de passe devra avoir au moins 8 caractères, une majuscule, un chiffre et un caractère spécial.

####  Utilisation du site

    - La page Flux :

        Une fois l'utilisateur connecté, la page "flux" s'affiche.

        L'utilisateur peut créer un ticket pour demander la critique d'un livre ou
        directement effectuer une critique en créant le ticket suivie de la critique.

        Un flux des tickets et critiques s'affiche selon les dates de création en ordre décroissant.
        il s'agit des tickets et critiques de l'utilisateur ou ceux des utilisateurs suivis.

        Si un ticket n'a pas de critique correspondant, il est possible d'en effectuer une.

        Lorsqu'un ticket a eu une critique, celui-ci n'apparaît plus dans le flux. Il apparaît directement dans la critique.
        Il n'est alors plus possible d'ajouter une critique à ce ticket.


    - La page Post :

        Cette page affiche tous les tickets et critiques de l'utilisateur.
        Il est alors possible de modifier ces posts ou de les supprimer.

        Si un ticket contenant une critique est supprimée, alors la critique est également supprimé.

        Si une critique est supprimé, il sera alors possible d'effectuer une critique à nouveau.


    - La page Abonnement :

        Cette page permet la gestion des utilisateurs suivis.

        On peut y ajouter un utilisateur en inscrivant son nom ou se désinscrire de cet utilisateur.

        En suivant un utilisateur, on voit les posts créés par cet utilisateur et ainsi répondre aux tickets.
