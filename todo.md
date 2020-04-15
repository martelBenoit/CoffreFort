# Ce qu'il reste a faire :

## Benoît 
- [x] Possibilité de faire une inscription depuis le front
```
front/routes/register.js
front/views/register.jade
```

## Kieran
- [ ] Changement de mot de passe :
    - création d'une nouvelle page (\changePassword) contenant un formulaire ( ou directement un nouveau formulaire sur la page```\home``` -> plus pratique et plus simple)
    - ```front/routes/home.js & front/views/home.jade```
- [x] Possibilité de se déconnecter :
    - renvoi vers une route pour se déconnecter par ex:```\logout``` 
    - supression du cookie de session dans le traitement du GET du ```\logout``` 
    - redirection page index a la fin de la supression du cookie de session

## Yoann

- [ ] ajout d'une image sur le docker de l'api apr, charger cette image au démarrage de l'api apr, passer en base64 si la ressource est demandé et traiter la réception côté front (app.py du dossier api_apr et resource.js du dossier front)


- [ ] faire l'apidoc pour l'api apr (reprendre ce qui a été fait côté api user)

## Loïc

- [x] ajout d'un framework css (bootstrap ou materialize ) pour le front

- [ ] revue du code python (partout)