var express = require('express');
var router = express.Router();
var mongoOp     =   require('../model/mongo');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

/* Call back function for return JSON response     */
function callback(err, data, res){
	// Mongo command to fetch all data from collection.
    if(err) {
    	response = {"error" : true,"message" : "Error fetching data"};
    } else {
        response = {"error" : false,"message" : data};
    }
    res.json(response);   
}

/* Parse the request to find all query parameters */
function getCondition(req){
	 var condition = {}
	 // Add subzone to query
	 if(req.query.subzone != null){
     	condition.subzone=req.query.subzone
     }
	 // Add zone to query
     if(req.query.zone != null){
     	condition.zone=req.query.zone
     }
	 // Add biomimic to query
	 if(req.query.biomimic != null){
     	condition.biomimic=req.query.biomimic
     }     
	 // Add region to query
     if(req.query.region !=  null){
     	condition.region=req.query.region
     }
     // Add wavexp to query
     if(req.query.waveexp != null){
     	condition.waveexp=req.query.waveexp
     }
	 // Add site to query
     if(req.query.site != null){
     	condition.site=req.query.site
     }
	 // Add location to query
     if(req.query.location !=  null){
     	condition.location=req.query.location
     }
	 // Add country to query
     if(req.query.country !=  null){
     	condition.country=req.query.country
     }
	 // Add dates to query
     if(req.query.startDate != null){
      	condition.data.Time.gte =  new Date(req.query.startDate)
     	condition.data.Time.lt =  new Date(req.query.endDate)
        //time = {'data.Time': {'$gte': new Date("2007-01-01"),
        //				 			'$lt': new Date('2007-01-05')}}
     }
     
     return condition
}

/* Get the data entries using the request parameters */
router.get('/data', function(req,res){    
     var response = {}
     var condition = getCondition(req)
     mongoOp.find( condition,
				  function(err,data){ callback(err,data,res);});})

/* Get distinct filter options using the request paramaters */
router.get('/filter/:param', function(req,res){
     var condition = getCondition(req)
     var param = req.params.param
     var response = {}
     mongoOp.distinct( param, 
     				  condition,
     				  function(err,data){ callback(err,data,res);})});
  
module.exports = router;
