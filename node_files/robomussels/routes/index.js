var express = require('express');
var router = express.Router();
var mongoOp     =   require('../model/mongo');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

/* GET Hello World page. */
router.get('/robomussels', function(req, res) {
           res.json({"error" : false,"message" : "Hello World"});
});

/* GET Userlist page. */
router.get('/data', function(req, res) {
           var db = req.db;
           var collection = db.get('test_robomussel');
           collection.find({},{},function(e,docs){
                           res.render('data', {
                                      "data" : docs
                                      });
                           });
           });

//router.route("/users")
//.get(function(req,res){
router.get('/robodata', function(req,res){
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

module.exports = router;
