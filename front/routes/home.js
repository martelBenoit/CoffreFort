var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  if (req.session.loggedin) {
    res.render('home', { title: req.session.login });
  }
  else{
    res.redirect('/')
  }
});

module.exports = router;
