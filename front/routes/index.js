var express = require('express');
var router = express.Router();

// GET home page. http://localhost:3000
router.get('/', function(req, res, next) {
  res.render('index'); // on affiche la page index
});

module.exports = router;
