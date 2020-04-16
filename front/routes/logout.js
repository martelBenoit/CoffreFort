var express = require('express');
const axios = require('axios');
const https = require('https');

var router = express.Router();

// Fonction redirigeant l'appel du bouton de deconnexion vers l'API users
router.get('/', function(req, res){
    var login = req.session.login;
    var token = req.session.token;

    if(login && req.session.loggedin==true) {
      
      // La requete est faite vers /api/logout et retourne la validation ou non de la deconnexion
      // et la raison en cas d'echec

      const options = {
        headers: {'Content-Type': 'application/json'},
        httpsAgent: new https.Agent({
          rejectUnauthorized: false
        })
      };

      const logout = async () => {
        try {
          const resultat = await axios.post('https://apiusers:5000/api/logout',
          {
            "LOGIN": login,
            "TOKEN": token
          },
          options
          )
          if(resultat.data.logout == true){
            req.session.loggedin = false;
            res.redirect('/');
            res.end();
          }
          else{
            res.send(resultat.data.reason);
            res.end();
          }
        } catch (error) {
          res.send(error)
          res.end()
        }
      }
      logout()

    }
    else{
      res.send("already deconnected");
      res.end();
    } 

});

module.exports = router;