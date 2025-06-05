import requests

OPENWEATHER_API_KEY = '0ad63bee2b070534eb175bea0f1b99f1'
SEOUL_AIR_API_URL = 'http://openapi.seoul.go.kr:8088/4978736c706d61733432476b6a4849/xml/ListAirQualityByDistrictService/1/5/111274/'

# 강동구 위도/경도
LAT = 37.5301
LON = 127.1238

def get_weather():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': LAT,
        'lon': LON,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'kr'
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        'temp': data['main']['temp'],
        'main': data['weather'][0]['main'],
        'desc': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }

def get_air_quality():
    resp = requests.get(SEOUL_AIR_API_URL)
    resp.raise_for_status()
    # XML 파싱
    import xml.etree.ElementTree as ET
    root = ET.fromstring(resp.text)
    item = root.find('.//row')
    if item is None:
        return None
    return {
        'pm10': item.findtext('PM10'),
        'pm25': item.findtext('PM25'),
        'o3': item.findtext('O3'),
        'co': item.findtext('CO'),
        'no2': item.findtext('NO2'),
        'so2': item.findtext('SO2'),
        'khai': item.findtext('KHAI'),
        'khai_grade': item.findtext('GRADE'),
        'district': item.findtext('MSRSTE_NM'),
        'data_time': item.findtext('MSRDT')
    } 