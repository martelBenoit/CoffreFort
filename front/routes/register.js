var express = require('express');
var request = require('request');
var router = express.Router();


/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('register');

});

router.post('/', function(req, res) {
    var login = req.body.login;
    var password = req.body.password;
  
    if(login && password){

      var options = {
        uri: 'http://apiusers:5000/api/users',
        method: 'POST',
        json: {
          "LOGIN": login,
          "PASSWORD": password
        }
      };
      
      request(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            result = JSON.parse(body)
            if(result.registration == true){
              res.redirect('/');
              res.end();
            }
            else{
              res.send(result.reason);
              res.end();
            }
        }
        else{
            res.send("Invalid post");
            res.end();
        } 
      });
  
    }
    else{
        res.send("Please enter login and password");
        res.end();
    } 
    
  });

module.exports = router;
