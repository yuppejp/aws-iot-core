import urllib.request
import cchardet
# import re
# from datetime import datetime
from bs4 import BeautifulSoup

class Weathernews():
    def get_weather(url):
        with urllib.request.urlopen(url) as res:
            byte = res.read()
            html = byte.decode(cchardet.detect(byte)['encoding'])
            soup = BeautifulSoup(html, 'html.parser')
            #print('[soup]:', soup, '\n')

            #title = soup.head.title
            #print('[title]:', title.text, '\n')

            #for block in soup.find_all('div', {'class':{'text_box'}}):
            for block in soup.find_all('div', {'class':{'weather-now__cont'}}):
                items = block.text.split()
                #print('[items]:', items, '\n')
                #['14:30', 'WeatherCloudy', 'Temp.31.4℃', 'RH68%', 'Pres.999hPa', 'Wind', 'S', '3m/s', 'Sunrise', '05:05', '|', 'Sunset', '18:27']
                #  0        1                2             3        4              5       6     7      8          9        10   11        12
    
        time = items[0]
        weather = items[1].replace('Weather', '')
        temp = items[2].replace('Temp.', '').replace('℃', '')
        humid = items[3].replace('RH', '').replace('%', '')
        pres = items[4].replace('Pres.', '').replace('hPa', '')
        #wind = items[6] + ' ' + items[7].replace('/', '')

        return time, weather, temp, humid, pres

def main():
    #千代田区
    url = 'https://weathernews.jp/onebox/35.680030/139.762025/q=%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%8D%83%E4%BB%A3%E7%94%B0%E5%8C%BA&temp=c&lang=en'
    time, weather, temp, humid, pres = Weathernews.get_weather(url)
    print('time:', time)
    print('weather:', weather)
    print('temp:', temp)
    print('humid:', humid)
    print('pres:', pres)

if __name__ == '__main__':
    main()