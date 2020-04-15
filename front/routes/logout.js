var express = require('express');
var request = require('request');

var router = express.Router();

// Fonction redirigeant l'appel du bouton de deconnexion vers l'API users
router.get('/', function(req, res){
    var login = req.session.login;
    var token = req.session.token;

    if(login && req.session.loggedin==true) {
        console.log('Beginning logout')
        

          // La requete est faite vers /api/logout et retourne la validation ou non de la deconnexion
          // et la raison en cas d'echec
          request.post('http://apiuser:5000/api/logout',{json: {
            "LOGIN": login,
            "TOKEN": token
          }}, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                result = JSON.parse(body)
                if(result.logout == true){
                  req.session.loggedin = false;
                  res.redirect('/index');
                  res.end();
                }
                else{
                  res.send(result.reason);
                  res.end();
                }
            }
            else{
                res.send("Invalid post");
                res.end();
            } 
          });

    }

});

module.exports = router;