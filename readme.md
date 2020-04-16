# COFFRE FORT

## Installation 

### Installation de docker sur debian

C'est une installation type de docker sur une machine debian amd64.
Il faut bien sur adapter cette installation à l'environnement de travail que vous possédez.

```bash
sudo apt update

sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

sudo apt update

apt-cache policy docker-ce

sudo apt install docker-ce
```

### Installation de docker-compose

Etape d'installation de docker-compose. Cette installation fonctionne sur une machine debian.

```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

## Lancement du projet sur debian

> Les opérations suivantes se font sur la racine du projet.

- Pour lancer le projet la première fois :
```bash
sudo docker-compose build
sudo docker-compose up
```

- Si le projet à déja été construit une première fois uniquement faire :
```bash
sudo docker-compose up
```

- Pour arrêter les services du projet :
```bash
sudo docker-compose down
```

> Si vous modifiez un Dockerfile il faut absolument refaire un build du projet sinon vos modifications ne seront pas prises en comptes !

## Informations utiles

#### FRONT DE L'APP
http://localhost:3000

#### DOC API USER 
http://localhost:5000/apidocs

#### DOC API APR
http://localhost:5200/apidocs

#### TOKEN DEALER
PORT 7000 : accessible uniquement par les APIs

#### Pour aller sur le service mongo db une fois le projet lancé
```bash
sudo docker exec -it coffrefort_mongodb_1 bash
```

---
Auteurs : Yoann LE DREAN, Kieran LE PENDEVEN, Benoît MARTEL, Loïc TRAVAILLE