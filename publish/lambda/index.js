index.js
const request = require('request');

exports.handler = function(event, context) {
    const message = '部屋の温度が上昇しています。室温:' + event.sensor.temp + '℃、外気温:' + event.weather.temp + '℃'; 
    const options = {
        uri: "https://api.line.me/v2/bot/message/push",
        headers: {
            "Content-type": "application/json; charset=utf-8",
            "Accept-Language": "jp",
            "Authorization": "Bearer {xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=}"
        },
        json: {
            "to": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "messages": [{
                "type": "text",
                "text": message
            }]
        }
    };
    request.post(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            context.done(null, body);
        } else {
            console.log('error: ' + response.statusCode);
            context.done(null, 'error');
        }
    });
};