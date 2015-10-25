var mongoose    =   require("mongoose");
var db = mongoose.connection;
db.on('error', console.error);
mongoose.connect('mongodb://robodb01.blieberman.me/test_robomussel/');
// create instance of Schema
var mongoSchema =   mongoose.Schema;
// create schema
var userScheme  = new mongoSchema({
                                  zone : String,
                                  biomimic : String,
                                  wave : String,
                                  subzone : String,
                                  site : String,
                                  location : String,
                                  country : String,
                                  data : String,
                                  }, { collection: 'posts' });


// create model if not exists.
module.exports = mongoose.model('mongoOp',userScheme);
