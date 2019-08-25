from bme280 import Bme280
from bh1750 import Bh1750
from weathernews import Weathernews

def main():
    bme280 = Bme280(0x76, 1)
    temp, humid, press = bme280.get_data()
    print('Temp:', temp, 'C')
    print('Humid:', humid, '%')
    print('Pressure:', press, '[%]')

    lux = Bh1750.get_lux()
    print('lux:', lux, 'lx')

    #千代田区
    url = 'https://weathernews.jp/onebox/35.680030/139.762025/q=%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%8D%83%E4%BB%A3%E7%94%B0%E5%8C%BA&temp=c&lang=en'
    time, tenki, temp, humid, pres = Weathernews.get_weather(url)
    print('time:', time)
    print('tenki:', tenki)
    print('temp:', temp, 'C')
    print('humid:', humid, '%')
    print('pres:', pres, 'hPa')

if __name__ == '__main__':
    main()
