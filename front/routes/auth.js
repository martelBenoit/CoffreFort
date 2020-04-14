var express = require('express');
var request = require('request');

// on utilise le module Router du framework express
var router = express.Router();

//GET  http://localhost:3000/auth/
router.post('/', function(req, res) {

  // on récupère le login et le mot de passe depuis le formulaire de connexion 
  var login = req.body.login;
  var password = req.body.password;

  // si le login et le mot de passe sont saisis
  if(login && password){

    // appel a l'API USER pour auth l'utilisateur
    url = 'http://' + login + ':' + password + '@apiusers:5000/api/token';

    request({url}, function (error, response, body) {
      result = JSON.parse(body)
      // Si le résultat de l'appel produit un résultat de token non nul/non vide alors 
      if(result.token != ""){
        // on place la session a un été connecté
        req.session.loggedin = true;
        // on sauvegarde le login de l'utilisateur
        req.session.login = login;
        // et son token
        req.session.token = result.token
        // on redirige l'utilisateur vers la page home de l'app
        res.redirect('/home');
        // on ferme la reponse 
        res.end();
      }
      else{
        res.send(result.reason);
        res.end();
      }
    });
  }

  else{
    res.send('Please enter username and password !');
    res.end();
  }
  
});

module.exports = router; // on n'oublie pas d'exporter le module