var express = require('express');
var router = express.Router();

// GET home page http://localhost:3000/
router.get('/', function(req, res, next) {
	// on regarde si la session est active (loggedin = true), si oui alors on demande a affiché la page home (sans redirection) et on passe un paramètre à la page home
	// le paramètre est title et vaut le login de l'utilisateur connecté
  if (req.session.loggedin) {
    res.render('home', { title: req.session.login });
  }
  else{
    res.redirect('/') // si la session est inactive pas d'utilisateur connecté alors redirection vers la page de connexion qui est dans notre app, la route /
  }
});

module.exports = router;
