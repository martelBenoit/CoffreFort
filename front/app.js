var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var session = require('express-session')

// la définition des routes
var indexRouter = require('./routes/index');
var authRouter = require('./routes/auth');
var homeRouter = require('./routes/home');
var resourceRouter = require('./routes/resource');
var registerRouter = require('./routes/register');
var logoutRouter = require('./routes/logout')

var app = express();

// définition de la session 
app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// définition des routes à utiliser
app.use('/', indexRouter);
app.use('/auth',authRouter);
app.use('/home', homeRouter);
app.use('/resource', resourceRouter);
app.use('/register', registerRouter);
app.use('/logout',logoutRouter);



// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
