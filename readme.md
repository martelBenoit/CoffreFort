# C'est le coffre fort !!!

## Installation docker sur debian

```bash
sudo apt update

sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

sudo apt update

apt-cache policy docker-ce

sudo apt install docker-ce
```

## Installation de docker-compose

```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

## Lancement du projet sur debian

Pour lancer le projet la première fois (sur la racine du repo git) :
```bash
sudo docker-compose build
sudo docker-compose up
```

Les fois suivantes uniquement faire (toujours sur la racine du repo git) :
```bash
sudo docker-compose up
```
## Aller sur le service mongo db une fois le projet lancé
```bash
sudo docker exec -it coffrefort_mongodb_1 bash
```