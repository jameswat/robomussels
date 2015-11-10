var mongoose    =   require("mongoose");
var db = mongoose.connection;
db.on('error', console.error);
mongoose.connect('mongodb://robodb01.blieberman.me/robo_data/');
// create instance of Schema
var mongoSchema =   mongoose.Schema;
// create schema
var roboScheme  = new mongoSchema({
                                  zone : String,
                                  biomimic : String,
                                  wave : String,
                                  subzone : String,
                                  site : String,
                                  location : String,
                                  country : String,
                                  data : {time: Date, temperature: Number},
                                  }, { collection: 'temp' });

// create model if not exists.
module.exports = mongoose.model('mongoOp',roboScheme);
