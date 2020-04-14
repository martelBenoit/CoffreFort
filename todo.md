# Ce qu'il reste a faire :

- ajout d'un framework css (bootstrap ou materialize ) pour le front
- ajout des infos de l'utilisateur sur la page home (pas nécessaire mais pourquoi pas)
- ajout d'une image sur le docker de l'api apr, charger cette image au démarrage de l'api apr, passer en base64 si la ressource est demandé et traiter la réception côté front (app.py du dossier api_apr et resource.js du dossier front) 
- revue du code python (partout)
- faire l'apidoc pour l'api apr (reprendre ce qui a été fait côté api user)

## Benoît 
Possibilité de faire une inscription depuis le front
```
front/routes/register.js
front/views/register.jade
```

## Kieran
- Changement de mot de passe :
    - création d'une nouvelle page (\changePassword) contenant un formulaire ( ou directement un nouveau formulaire sur la page```\home``` -> plus pratique et plus simple)
    - ```front/routes/home.js & front/views/home.jade```
- Possibilité de se déconnecter :
    - renvoi vers une route pour se déconnecter par ex:```\logout``` 
    - supression du cookie de session dans le GET du ```\logout``` 
    - redirection page index

## Yoann
à définir


## Loïc
à définir




