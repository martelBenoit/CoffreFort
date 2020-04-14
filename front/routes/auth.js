var express = require('express');
var request = require('request');

var router = express.Router();

// Fonction redirigeant l'appel d'authentification via le form vers l'API users
router.post('/', function(req, res) {
  var login = req.body.login;
  var password = req.body.password;

  if(login && password){

    console.log('login and password filled')

    // ATTENTION : Bien prendre en compte que la requete est faite sur api/token
    url = 'http://' + login + ':' + password + '@apiusers:5000/api/token';

    request({url}, function (error, response, body) {
      result = JSON.parse(body)
      if(result.token != ""){
        req.session.loggedin = true;
        req.session.login = login;
        req.session.token = result.token
        res.redirect('/home');
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

module.exports = router;