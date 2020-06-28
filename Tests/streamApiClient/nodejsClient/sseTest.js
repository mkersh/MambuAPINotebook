var EventSource = require('eventsource')

// Event stream from a test SSE server in python that works
var url = 'http://127.0.0.1:5000/stream'

//var url = 'https://michaelgbp.mambu.com/api/v1/subscriptions/d38a66b9-b9c7-41d3-98cc-0221792813f2/events';
//var url = 'https://michaelgbp.mambu.com/api/v1/subscriptions/1aab926c-bc33-46a2-b392-1d47c29d8f70/events?batch_flush_timeout=10&batch_limit=1';

var headers = { 
    headers: {
        'apikey': 'sAi1D7J82uDMD8gxQApR693jp3NfT4OG',
        'content-type': 'application/x-json-stream' }
}

var source = new EventSource(url, headers);
console.log("Start EventSource test");
source.onmessage = function(e) {
      console.log(e.data);
    };

source.addEventListener("mrn.event.michaelgbp.streamingapi.client_activity", function(event) {
    console.log(event.data);
});

source.onerror = function(e) {
        console.log("Something has gone wrong!!: ", e)
      };
console.log("END EventSource test");
