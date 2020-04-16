var express = require('express');
const axios = require('axios');
const https = require('https');

var router = express.Router();

// GET http://localhost:3000/resource
router.get('/', function(req, res) {

  // on vérifie que la session est active 
  if(req.session.loggedin){

    var options = {
        httpsAgent: new https.Agent({
          rejectUnauthorized: false
        })
    };

    // appel à l'API APR avec le token de l'utilisateur stocké dans le cookie de session
    url = 'https://apiapr:5200/api/ressource?token='+req.session.token;

    const getRes = async () => {
      try {
        const resultat = await axios.get(url,options)
        // si c'est ok alors on affiche la ressource protégé recu en retour d'appel sinon on afficher un message ou alors on redirige vers la page home
        if(resultat.data.pr){
        
          imageData = "data:image/jpeg;base64, " + resultat.data.pr;
          res.render('resource', {image:imageData});
          res.end();
        }
        else{
          res.send(resultat.data.info);
          res.end();
        }
      } catch (error) {
        console.error(error)
        res.send(error)
        res.end()
      }
    }
    getRes()
  }

  else{
    res.redirect('/home');
    res.end();
  }
  
});

module.exports = router;