import json
import time
from datetime import datetime
from bme280 import Bme280
from bh1750 import Bh1750
from weathernews import Weathernews

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def support_datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()

def get_data():
    bme280 = Bme280(0x76, 1)
    temp, humid, pres = bme280.get_data()
    
    temp = round(temp, 1)
    humid = int(humid)
    pres = int(pres)
    print('temp:', temp, 'C')
    print('humid:', humid, '%')
    print('pres:', pres, '[%]')
    
    lux = Bh1750.get_lux()
    print('lux:', lux, 'lx')

    #千代田区
    url = 'https://weathernews.jp/onebox/35.680030/139.762025/q=%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%8D%83%E4%BB%A3%E7%94%B0%E5%8C%BA&temp=c&lang=en'
    wt_time, wt_tenki, wt_temp, wt_humid, wt_pres = Weathernews.get_weather(url)
    
    wt_temp = float(wt_temp)
    wt_humid = int(wt_humid)
    wt_pres = int(wt_pres)
    
    print('time:', wt_time)
    print('tenki:', wt_tenki)
    print('temp:', wt_temp, 'C')
    print('humid:', wt_humid, '%')
    print('pres:', wt_pres, 'hPa')
    
    sensor = {}
    sensor['temp'] = temp
    sensor['humid'] = humid
    sensor['pres'] = pres
    sensor['lux'] = lux
    
    weather = {}
    weather['time'] = wt_time
    weather['tenki'] = wt_tenki
    weather['temp'] = wt_temp
    weather['humid'] = wt_humid
    weather['pres'] = wt_pres

    message = {}
    #message['sensor_temp'] = temp
    #message['sensor_humid'] = humid
    #message['sensor_pres'] = pres
    message['timestamp'] = datetime.now()
    message['sensor'] = sensor
    message['weather'] = weather
    messageJson = json.dumps(message, default=support_datetime_default)

    #message = {}
    #message['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #message['temp'] = temp
    #message['humid'] = humid
    #message['pres'] = pres
    #message['lux'] = lux
    #messageJson = json.dumps(message)

    print(messageJson)
    return messageJson

def main():    
    # For certificate based connection
    myMQTTClient = AWSIoTMQTTClient("myClientID")
    # For Websocket connection
    # myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
    # Configurations
    # For TLS mutual authentication
    myMQTTClient.configureEndpoint("xxxxxxxxxxxxxxxxx.iot.ap-northeast-1.amazonaws.com", 8883)
    # For Websocket
    # myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
    # For TLS mutual authentication with TLS ALPN extension
    # myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
    myMQTTClient.configureCredentials("AmazonRootCA1.pem", "xxxxxxxxxx-private.pem.key", "xxxxxxxxxx-certificate.pem.crt")
    # For Websocket, we only need to configure the root CA
    # myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    myMQTTClient.connect()
    
    while True:
        messageJson = get_data()
        myMQTTClient.publish("myTopic", messageJson, 1)
        print('wait...')
        time.sleep(60)
 
    #messageJson = get_data()
    #myMQTTClient.publish("myTopic", messageJson, 1)
    
    myMQTTClient.disconnect()

if __name__ == '__main__':
    main()
