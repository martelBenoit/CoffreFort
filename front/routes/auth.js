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
      console.log(body)
      result = JSON.parse(body)
      console.log(result.auth)
      console.log(result.reason)
    });

  
    console.log('end request')


  }

  else{
  	res.send('Please enter username and password !');
  }
  res.end();
});

module.exports = router;