const mqtt = require('mqtt')
//const lib = require("./lib");

function DynamicCompute (msgArgs, cmdInstance, cmdId){
  try{
    if (!msgArgs.hasOwnProperty("Duration")){
      throw new ReferenceError("Incomplete arg data: no Duration is detected");
    }
    else{var Duration = msgArgs.Duration;};
    
    if (!msgArgs.hasOwnProperty("InitialData")){
      throw new ReferenceError("Incomplete arg data: no InitialData is detected");
    }
    else{
      if (!msgArgs.InitialData.hasOwnProperty("Tgas_out_1_5")){
        throw new ReferenceError("Incomplete arg data: no Tgas_out_1_5 is detected");
      }
      else{var Tgas_out_1_5 = msgArgs.InitialData.Tgas_out_1_5;};

      if (!msgArgs.InitialData.hasOwnProperty("Tgas_out_6_7")){
        throw new ReferenceError("Incomplete arg data: no Tgas_out_6_7 is detected");
      }
      else{var  Tgas_out_6_7= msgArgs.InitialData.Tgas_out_6_7;};

      if (!msgArgs.InitialData.hasOwnProperty("Tgas_out_8_9")){
        throw new ReferenceError("Incomplete arg data: no Tgas_out_8_9 is detected");
      }
      else{var  Tgas_out_8_9= msgArgs.InitialData.Tgas_out_8_9;};

      if (!msgArgs.InitialData.hasOwnProperty("Twater_out_1_5")){
        throw new ReferenceError("Incomplete arg data: no Twater_out_1_5 is detected");
      }
      else{var  Twater_out_1_5= msgArgs.InitialData.Twater_out_1_5;};

      if (!msgArgs.InitialData.hasOwnProperty("Twater_out_6_7")){
        throw new ReferenceError("Incomplete arg data: no Twater_out_6_7 is detected");
      }
      else{var Twater_out_6_7 = msgArgs.InitialData.Twater_out_6_7;};

      if (!msgArgs.InitialData.hasOwnProperty("Twater_out_8_9")){
        throw new ReferenceError("Incomplete arg data: no Twater_out_8_9 is detected");
      }
      else{var Twater_out_8_9 = msgArgs.InitialData.Twater_out_8_9;};
    };
    
    if (!msgArgs.hasOwnProperty("SystemInputs")){
      throw new ReferenceError("Incomplete arg data: no Vgas is detected");
    }
    else{
      if (!msgArgs.SystemInputs.hasOwnProperty("Twater_in")){
        throw new ReferenceError("Incomplete arg data: no Twater_in is detected");
      }
      else{var Twater_in = msgArgs.SystemInputs.Twater_in;};

      if (!msgArgs.SystemInputs.hasOwnProperty("Vgas")){
        throw new ReferenceError("Incomplete arg data: no Duration is detected");
      }
      else{var Vgas = msgArgs.SystemInputs.Vgas;};
    };
  } catch(error) {
    console.error(error.message);
  }


  //dynamicCalculation.py InstanceID duration T_g_out_1_5 T_g_out_6_7 T_w_out_1_5 T_w_out_6_7 T_g_out_8_9 T_w_out_8_9 T_w_in_6_9 V_ng
  //cmdInstance, cmdId, Duration, Tgas_out_1_5, Tgas_out_6_7, Twater_out_1_5, Twater_out_6_7, Tgas_out_8_9, Twater_out_8_9, Twater_in, Vgas
  var spawn = require('child_process').spawn;
  var model = spawn('python3', ['dynamicCalculation.py',cmdInstance, cmdId, Duration, Tgas_out_1_5, Tgas_out_6_7, Twater_out_1_5, Twater_out_6_7, Tgas_out_8_9, Twater_out_8_9, Twater_in, Vgas]);
  
  
  model.stdout.on('data', function(data) {
    console.log(data.toString());
  });
  // model.stdout.on('end', function(data) {
  //   console.log("end:",(data));
  //   });
  // model.stdout.on("close", function(data) {
  //   console.log("close:", (data));
  // });
  model.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
  model.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
}

function staticCompute (msgArgs, cmdInstance, cmdId){
  try{
    if (!msgArgs.hasOwnProperty("Twater_in")){
      throw new ReferenceError("Incomplete arg data: no Twater_in is detected");
    }
    else{var Twater_in = msgArgs.Twater_in;};
    
    if (!msgArgs.hasOwnProperty("Twater_out")){
      throw new ReferenceError("Incomplete arg data: no command is detected");
    }
    else{var Twater_out = msgArgs.Twater_out;};
    
    if (!msgArgs.hasOwnProperty("Vgas")){
      throw new ReferenceError("Incomplete arg data: no Vgas is detected");
    }
    else{var Vgas = msgArgs.Vgas;};
  } catch(error) {
    console.error(error.message);
  }

  var spawn = require('child_process').spawn;
  var model = spawn('python3', ['staticCalculation.py',cmdInstance,cmdId,Twater_in,Twater_out,Vgas]);
  
  
  model.stdout.on('data', function(data) {
    console.log(data.toString());
  });
  model.stdout.on('end', function(data) {
    console.log("end:",(data));
    });
  model.stdout.on("close", function(data) {
    console.log("close:", (data));
  });
  model.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
  model.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
}

function instanceCheck(instanceId){
  const fs = require('fs');
  // directory to check if exists
  const dir = './instancesData/' + instanceId;
  // check if directory exists
  if (fs.existsSync(dir)) {
  return true;
  } else {
  return false;
  }
}

function commandCheck (msg, c_id){
  var logger = [];
  var result = 0;
  // Check if it is destination controller
  //!msgArgs.hasOwnProperty(
  try {
    if (!msg.hasOwnProperty("command")){
      throw new SyntaxError("Incomplete data: no destination command founded");
    }
    if (!msg.hasOwnProperty("object")){
      throw new SyntaxError("Incomplete data: no destination object founded");
    }

    if (!msg.command.hasOwnProperty("controller_id")){
      throw new SyntaxError("Incomplete data: no destination controller ID founded");
    }
    if (msg.command.controller_id == c_id){
      logger.push([Date.now(), "Id is accepted"]);
      
      // Check if command, instance ID, command ID are present
      if (!msg.command.type){
        throw new SyntaxError("Incomplete data: no command detected");
      }
      else{var cmdType = msg.command.type; logger.push([Date.now(), "Command detected"]);};
      
      if (!msg.object.hasOwnProperty("instance")){
        throw new SyntaxError("Incomplete data: no instance unic id detected");
      }
      else{var cmdInstance = msg.object.instance; logger.push([Date.now(), "Instance unic id detected"]);};
      
      if (!msg.command.hasOwnProperty("id")){
        throw new SyntaxError("Incomplete data: no command unic id detected");
      }
      else{var cmdId = msg.command.id; logger.push([Date.now(), "Command unic id detected"]);};

      if (!msg.hasOwnProperty("args")){
        throw new SyntaxError("Incomplete data: no arguments are detected");
      }
      else{var msgArgs = msg.args; logger.push([Date.now(), "Arguments are detected"]);};

      console.log ("obj: ",cmdInstance," command: ",cmdType, "command ID: ",cmdId)

      // Check if command == add_instance

      switch(cmdType){
        case 'add_instance':
          if (!instanceCheck(cmdInstance)){

            result = 1;

          } else{
            throw new SyntaxError("Incorrect data: instance with current id exist");
          }
        break;

        // Check if command != add_instance
        default:
          if (instanceCheck(cmdInstance)){
            // Select command and check args
            switch(cmdType){
              case 'compute_static': //STATIC
                  staticCompute(msgArgs, cmdInstance, cmdId);
                  result = 1;
              break;

              case 'compute_dynamic':
                  DynamicCompute(msgArgs, cmdInstance, cmdId);
                  result = 1;
              break;

              default:
                throw new SyntaxError("Incorrect data: command `" + cmdType + "` in unknown");
            }

          } else{
            throw new SyntaxError("Incorrect data: instance with current id don`t exist");
          }
        };

    
    };


  } catch (error) {
    console.log(err.message);
    logger.push([Date.now(), err.message]);
    result = -1;
  }
  
return [result, logger]

};




contrId = "ksajdejj111";

const host = '185.233.116.83';
const port = '1885';
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`;
const username = 'nzakharchenko';
const password = 'mqttPython';

const connectUrl = `mqtt://${host}:${port}`;
const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: username,
  password: password,
  reconnectPeriod: 1000,
});

const topic = "Computation/Control";
client.on('connect', () => {
  console.log('Connected')
  client.subscribe([topic], () => {
    console.log(`Subscribe to topic '${topic}'`);
  })
});
client.on('message', function onMsg (topic, payload) {
  var msg_log = [];
  try {
    var command = JSON.parse(payload.toString())
    console.log('Received Message:', topic, payload.toString())
  } catch (error) {
    console.log('Can not read JSON')
  }
  if (command){
  const res = commandCheck(command,"ksajdejj111");
  console.log(res.toString())
  }
});

