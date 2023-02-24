//const { toASCII } = require('punycode');

//var args = "staticCalculation.py 7f204286044f 7f204286044f 332.15 343.15 0.00181974681"
//var args = "7f204286044f 7f204286044f 332.15 343.15 0.00181974681"
var spawn = require('child_process').spawn;
var model = spawn('python3', ['staticCalculation.py',"7f204286044f","7f204286044f",332.15,343.15,0.00181974681]);

model.stdout.on('data', function(data) {

    // convert Buffer object to Float
    console.log("DATA");
    console.log(data.toString());
});
model.stdout.on('end', function(data) {

    // convert Buffer object to Float
    console.log("end");
    console.log("end:",(data));
    });

model.stdout.on("close", function(data) {

        // convert Buffer object to Float
        console.log("close");
        console.log("close:", (data));
        });
model.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });

model.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });