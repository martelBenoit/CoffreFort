var express = require('express');
const axios = require('axios');
const https = require('https');

// on utilise le module Router du framework express
var router = express.Router();

//GET  http://localhost:3000/auth/
router.post('/', function(req, res) {

  // on récupère le login et le mot de passe depuis le formulaire de connexion 
  var login = req.body.login;
  var password = req.body.password;

  var options = {
    httpsAgent: new https.Agent({
      rejectUnauthorized: false
    })
  };

  // si le login et le mot de passe sont saisis
  if(login && password){
    const getAuth = async () => {
      try {
        const resultat = await axios.get('https://' + login + ':' + password + '@apiusers:5000/api/token',options)
        if (resultat.data.token != "") {
          // on place la session a un été connecté
          req.session.loggedin = true;
          // on sauvegarde le login de l'utilisateur
          req.session.login = login;
          // et son token
          req.session.token = resultat.data.token
          // on redirige l'utilisateur vers la page home de l'app
          res.redirect('/home');
          // on ferme la reponse 
          res.end();
        } 
        else{
          res.render('index', { error: resultat.data.reason });
          res.end();
        } 
      } catch (error) {
      
        res.render('index', { error: error });
        res.end()
      }
    }
    getAuth()
  } 

  else{
    res.render('index', { error: 'Please enter username and password !' });
    res.end();
  }
  
});

module.exports = router; // on n'oublie pas d'exporter le module