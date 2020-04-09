var express = require('express');
var request = require('request');

var router = express.Router();

router.post('/', function(req, res) {
  var login = req.body.login;
  var password = req.body.password;

  if(login && password){

    console.log('login and password filled')

    url = 'http://' + login + ':' + password + '@apiusers:5000/api/auth';

    request({url}, function (error, response, body) {
      result = JSON.parse(body)
      if(result.auth == true){
        req.session.loggedin = true;
        req.session.login = login;
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