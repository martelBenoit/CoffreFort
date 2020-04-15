var express = require('express');
var request = require('request');

var router = express.Router();

// GET http://localhost:3000/resource
router.get('/', function(req, res) {

  // on vérifie que la session est active 
  if(req.session.loggedin){

    // appel à l'API APR avec le token de l'utilisateur stocké dans le cookie de session
    url = 'http://apiapr:5200/api/ressource?token='+req.session.token;

    request({url}, function (error, response, body) {
      result = JSON.parse(body)
      // si c'est ok alors on affiche la ressource protégé recu en retour d'appel sinon on afficher un message ou alors on redirige vers la page home
      if(result.pr){
       
        res.send(result.pr);
        res.end();
      }
      else{
        res.send(result.info);
        res.end();
      }
    });
  }

  else{
    res.redirect('/home');
    res.end();
  }
  
});

module.exports = router;