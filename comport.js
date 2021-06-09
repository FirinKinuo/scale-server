const SerialPort = require('serialport')
const Readline = require('@serialport/parser-readline')
const port = new SerialPort('/dev/ttyS2', {autoOpen: true, baudRate: 9600, parity: 'none', dataBits: 8, stopBits: 1})

// The open event is always emitted
port.on('open', function () {
  //console.log('Open com port: ', port.path);
})

var ves = [];
var input = "", inputline = ""
var count = 0


var freg = require('float-regex').source;
var capture = RegExp('\\b(' + freg + ')\\b', 'g');

const http = require('http')
const httpport = 3000

const requestHandler = (request, response) => {
  //console.log(request.url)
  if (!port.isOpen) {
    port.open(function (err) {
      if (err) {
        return console.log('Error opening port: ', err.message)
      }
    })
  }
  response.end(get_ves())

}
const server = http.createServer(requestHandler)

server.listen(httpport, '0.0.0.0', (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log(`server is listening on ${httpport}`)

  port.on('data', function (data) {
    getThisTime()

    inputline = data.toString('utf-8');
    inputline = inputline.replace(/\r?\n/g, "")
    //console.log('Данные полученные с COM: ', inputline)

    if (inputline.includes("ww") && inputline.includes("kg")) {
      input = inputline
      //console.log('-1-')
    } else if (inputline.includes("ww") && !inputline.includes("kg")) {
      input = inputline
      //console.log('-2-')
      return
    } else if (!inputline.includes("ww") && inputline.includes("kg")) {
      input = input + inputline
      //console.log('-3-')
    } else if (!inputline.includes("ww") && !inputline.includes("kg")) {
      input = ""
      //console.log('-4-')
      return
      //} else if (inputline.includes(String.fromCharCode(65533)) && inputline.includes("B")) {
      //	input = inputline
      //	console.log('-10-')
    } else {
      for (var i = 0; i < inputline.length - 1; i++) {
        //console.log(inputline.charCodeAt(i), ' ');
        // ещё какие-то выражения
      }
      //console.log('-5-')
      return
    }

    output = obrabotka(input)
    if (output == null) {
      return // ниче не делаем
    } else {
      //if (ves.length > 2) {
      //	ves.pop()
      //	ves.pop()
      //}
      ves.unshift(output)
      //ves.unshift(1)
      //array = [output];
    }

    //console.log(count)
    //console.log(input)
    input = ""
    //Ѓ    0.00 B

    //ves.push(Math.random() * (10 - 0) + 0) // test
    count++
  })
})

const requestHandler2 = (request, response) => {
  if (!port.isOpen) {
    port.open(function (err) {
      if (err) {
        return console.log('Error opening port: ', err.message)
      }

      //
    })
  }

  t = "<!DOCTYPE HTML PUBLIC />\
	<html>\
	<head>\
	<meta http-equiv=Refresh content=1 />\
	<title>auto</title>\
	<style> html, body { background-color: green; background: linear-gradient(to top, #648520, #8aa652); overflow: hidden;} \
	div {color:white;text-align: center;font-size: 30px;font-family:sans-serif;} </style>\
	</head>\
	<body>\
	<div id=subscribe>" + get_ves_light() + "</div>\
	</body>\
	</html>"
  response.end(t)

}
const server2 = http.createServer(requestHandler2)

server2.listen(3001, '0.0.0.0', (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log(`server is listening on 3001`)
})

/* var Static = require('node-static');
var WebSocketServer = new require('ws');

// подключенные клиенты
var clients = {};

// WebSocket-сервер на порту 8081
var webSocketServer = new WebSocketServer.Server({port: 8081});
webSocketServer.on('connection', function(ws) {

  var id = Math.random();
  clients[id] = ws;
  console.log("новое соединение " + id);

  ws.on('message', function(message) {
    console.log('получено сообщение ' + message);

    for(var key in clients) {
      //clients[key].send(message);
	  clients[key].send(get_ves());
    }
  });

  ws.on('close', function() {
    console.log('соединение закрыто ' + id);
    delete clients[id];
  });

});
 */

// tut schitaem ves
function get_ves() {
  //console.log(ves)
  return 'ves:' + Math.floor(ves[0])
}

function get_ves_light() {
  return Math.floor(ves[0])
}

function weighted_average(input) {
  var weights = [];
  var values = [];
  var weighted_total = 0;
  var total_weight = 0;

  /* if (input.length % 3 !== 0) {
      throw new Error("Input array length is not a multiple of 3.");
  } */

  for (var i = 0; i < input.length; i += 2) {
    weights.push(input[i]);
    values.push(input[i + 1]);
  }

  for (var i = 0; i < weights.length; i += 1) {
    weighted_total += weights[i] * values[i];
    total_weight += weights[i];
  }

  if (total_weight == 0) {
    return 0
  } else {
    return weighted_total / total_weight;
  }
}

function obrabotka(input) {

  if (input == "") {
    return 0;
  }

  input = input.replace("Ѓ", "");
  input = input.replace("!", "");
  input = input.replace("?", "");
  input = input.replace("B", "");
  input = input.replace(" ", "");
  input = input.replace("	", "");
  input = input.replace("-", "");
  input = input.replace("?", "");
  input = input.replace("WN", "");
  input = input.replace("ww", "");
  input = input.replace("kg", "");

  //console.log('Данные на входе для regexp: ', input)
  //console.log('Данные после regexp: ', input.match(capture));

  m = input.match(capture)
  if (!m) {
    return null
  } else {
    return parseFloat(m)
  }

}

function sleep(milliSeconds) {
  var startTime = new Date().getTime();
  while (new Date().getTime() < startTime + milliSeconds) ;
}

function getThisTime() {
  Data = new Date();
  Hour = Data.getHours();
  Minutes = Data.getMinutes();
  Seconds = Data.getSeconds();

  // Вывод
  //console.log("> "+Hour+":"+Minutes+":"+Seconds);
}
