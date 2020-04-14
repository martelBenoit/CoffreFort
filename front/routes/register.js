var express = require('express');
var request = require('request');
var router = express.Router();


// GET home page. http://localhost:3000/register 
// on affiche simplement la page contenant le formulaire d'inscription
router.get('/', function(req, res, next) {
    res.render('register');

});

// POST http://localhost:3000/register 
// on soumet le formulaire d'inscription
router.post('/', function(req, res) {

    // récupération des champs du formulaire
    var login = req.body.login;
    var password = req.body.password;
  
    if(login && password){

      var options = {
        uri: 'http://apiusers:5000/api/users',
        method: 'POST',
        json: {
          "LOGIN": login,
          "PASSWORD": password
        }
      };
      //appel à l'API user pour s'enregistrer
      request(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            result = JSON.parse(body)
            if(result.registration == true){ // si l'API nous répond vrai alors on redirige vers la page de connexion
              res.redirect('/');
              res.end();
            }
            else{
              res.send(result.reason); // sinon on affiche un message
              res.end();
            }
        }
        else{
            res.send("Invalid post");
            res.end();
        } 
      });
  
    }
    else{
        res.send("Please enter login and password");
        res.end();
    } 
    
  });

module.exports = router;
