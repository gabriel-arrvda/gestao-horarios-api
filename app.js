// import express JS module into app 
// and creates its variable. 
var express = require('express'); 
var app = express(); 
const { spawn } = require('child_process');
const cors = require('cors');

app.use(cors());
// Creates a server which runs on port 3000 and  
// can be accessed through localhost:3000 
app.listen(3000, function() { 
    console.log('server running on port 3000'); 
} ) 
  
// Function callName() is executed whenever  
// url is of the form localhost:3000/name 
app.get('/generate', callName); 
  
function callName(req, res) { 
      
    const {
        qtdTotalC,
        qtdTotalE,
        qtdNecessariaC1,
        qtdNecessariaC2,
        qtdNecessariaC3,
        qtdNecessariaE1,
        qtdNecessariaE2,
        qtdNecessariaE3
    } = req.query;

    // Spawn the Python process with the query parameters as arguments
    const process = spawn('python', [
        './generator.py',
        qtdTotalC,
        qtdTotalE,
        qtdNecessariaC1,
        qtdNecessariaC2,
        qtdNecessariaC3,
        qtdNecessariaE1,
        qtdNecessariaE2,
        qtdNecessariaE3
    ]);

    let output = '';
    // Capture stdout from Python script
    process.stdout.on('data', function (data) {
        output += data.toString();
        console.log(`stdout: ${data}`);
    });

    // Handle any errors from Python process
    process.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
  
    // Takes stdout data from script which executed 
    // with arguments and send this data to res object 
    process.on('close', function (code) {
        try {
            const jsonResponse = JSON.parse(output);
            res.json(jsonResponse);
        } catch (error) {
            console.error('Error parsing JSON from Python script', error);
            res.status(500).send('Error processing request');
        }
    });
} 