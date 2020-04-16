var express = require('express');
const axios = require('axios');

var router = express.Router();

// GET page http://localhost:3000/update
// On affiche la page de changement de mot de passe
router.get('/', function(req,res,next){
    if(req.session.loggedin){
        res.render('update');
        res.end();
    }
    else{
        res.redirect('/home');
        res.end();
    }

});

// POST page http://localhost:3000/update
// On fait la requete vers l'api users et on affiche le succes ou non de la requete
router.post('/', function(req,res){
    if(req.session.loggedin){
        // recuperation des elements necessaires au changement de mdp
        var login = req.session.login;
        var current = req.body.current;
        var newpass = req.body.new;
        var verif = req.body.verif;

        const options = {
            headers: {'Content-Type': 'application/json'}
        };

        if(login && current && newpass && verif){
            if(newpass === verif){ // on verifie que le nouveau mdp et sa confirmation sont bien identiques
                const update = async () => {
                    try {
                        // La requete effectuee est PUT sur apiusers:5000/api/users/<login> avec auth BASIC
                        const resultat = await axios.put('http://'+login+':'+current+'@apiusers:5000/api/users/'+login,
                        {
                            'PASSWORD' : newpass
                        },options
                        )
                        if(resultat.data.update == true){
                            res.render('update',{ success: "Password successfully updated !" });
                            res.end();
                        }
                        else{
                            res.render('update', { error: resultat.data.reason });
                            res.end();
                        }
                    }
                    catch (error) {
                        res.render('update', { error: error });
                        res.end;
                    }
                }
                update()
            }
            else {
                res.render('update',{ error: 'Wrong password confirm.' });
                res.end();
            }
        }
    }

});

module.exports = router;
