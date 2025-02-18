var fs = require("fs"); 
var http = require("http");
var s="";
http.createServer(function (req, res) {
   var v="";
   var vv=req.url.toString();
   res.writeHead(200, {'Content-Type': 'html'});
   if ( vv == "/" ) vv="/main.html";
   vv="./" + vv;
   fs.readFile ( vv , function  ( err , s ){
    if (err) console.log(err);
    res.end ( s);
    });
   
}).listen(8080);

console.log('request server');
