var express = require('express');
var request = require('request');

var router = express.Router();

router.get('/', function(req, res) {

  if(req.session.loggedin){

    url = 'http://apiapr:5200/api/ressource?token='+req.session.token;

    request({url}, function (error, response, body) {
      result = JSON.parse(body)
      if(result.pr){
       
        res.send(result.pr);
        res.end();
      }
      else{
        res.send(result.info);
        res.end();
      }
    });
  }

  else{
    res.redirect('/home');
    res.end();
  }
  
});

module.exports = router;