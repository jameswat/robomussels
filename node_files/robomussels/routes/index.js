var express = require('express');
var router = express.Router();
var mongoOp     =   require('../model/mongo');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});


/* GET all robo data*/
router.get('/roboall', function(req,res){
     var response = {};
     mongoOp.find({},function(err,data){
                  // Mongo command to fetch all data from collection.
                  if(err) {
                  response = {"error" : true,"message" : "Error fetching data"};
                  } else {
                  response = {"error" : false,"message" : data};
                  }
                  res.json(response);
                  });
     });


/* GET robomussel */
router.get('/robomussel', function(req,res){
     var response = {};
     mongoOp.find({"biomimic":"robomussel"},function(err,data){
                  // Mongo command to fetch all data from collection.
                  if(err) {
                  response = {"error" : true,"message" : "Error fetching data"};
                  } else {
                  response = {"error" : false,"message" : data};
                  }
                  res.json(response);
                  });
     });
     
/* GET robomussel- USA */
router.get('/robomussel/USA/', function(req,res){
     var response = {};
     mongoOp.find({"biomimic":"robomussel","country":"USA"},function(err,data){
                  // Mongo command to fetch all data from collection.
                  if(err) {
                  response = {"error" : true,"message" : "Error fetching data"};
                  } else {
                  response = {"error" : false,"message" : data};
                  }
                  res.json(response);
                  });
     });
     
/* GET robomussel- USA - Alegria */
router.get('/robomussel/USA/Alegria', function(req,res){
     var response = {};
     mongoOp.find({"biomimic":"robomussel","country":"USA", "location":"Alegria"},function(err,data){
                  // Mongo command to fetch all data from collection.
                  if(err) {
                  response = {"error" : true,"message" : "Error fetching data"};
                  } else {
                  response = {"error" : false,"message" : data};
                  }
                  res.json(response);
                  });
     });
     

module.exports = router;
