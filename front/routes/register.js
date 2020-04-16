var express = require('express');
const axios = require('axios');
const https = require('https');

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

      const options = {
        headers: {'Content-Type': 'application/json'},
        httpsAgent: new https.Agent({
          rejectUnauthorized: false
        })
      };

      const register = async () => {
        try {
          const resultat = await axios.post('https://apiusers:5000/api/users',
          {
            "LOGIN": login,
            "PASSWORD": password
          },options
          )
          if(resultat.data.registration == true){
            res.redirect('/');
            res.end();
          }
          else{
            res.render('register', { error: resultat.data.reason });
            res.end();
          }
        } catch (error) {
          res.render('register', { error: error });
          res.end()
        }
      }
      register()
  
    }
    else{
        res.render('register', "Please enter login and password");
        res.end();
    } 
    
  });

module.exports = router;
