import os
import requests
from datetime import datetime
from database import get_db_connection
from common.logger import setup_logger
import json

logger = setup_logger('environment_service')

class EnvironmentService:
    def __init__(self):
        # API 키 설정
        self.weather_api_key = '0ad63bee2b070534eb175bea0f1b99f1'
        self.air_api_key = '4978736c706d61733432476b6a4849'
        self.location = {
            'lat': '37.5301',  # 강동구 위도
            'lon': '127.1238'  # 강동구 경도
        }
        self.sse_clients = set()

    def fetch_weather(self):
        """날씨 정보 조회"""
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': self.location['lat'],
                'lon': self.location['lon'],
                'appid': self.weather_api_key,
                'units': 'metric',
                'lang': 'kr'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temp': data['main']['temp'],
                'main': data['weather'][0]['main'],
                'weather_desc': data['weather'][0]['description']
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"날씨 정보 조회 실패: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"날씨 정보 파싱 실패: {str(e)}")
            return None

    def fetch_air_quality(self):
        """대기질 정보 조회"""
        try:
            url = f"http://openapi.seoul.go.kr:8088/{self.air_api_key}/xml/ListAirQualityByDistrictService/1/5/111274/"
            response = requests.get(url)
            response.raise_for_status()
            
            # XML 파싱
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.text)
            item = root.find('.//row')
            if item is None:
                logger.error("대기질 데이터를 찾을 수 없습니다.")
                return None
                
            return {
                'pm10': item.findtext('PM10'),
                'pm25': item.findtext('PM25'),
                'khai_grade': item.findtext('GRADE')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"대기질 정보 조회 실패: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"대기질 정보 파싱 실패: {str(e)}")
            return None

    def save_environment_data(self, weather_data, air_data):
        """환경 정보 저장"""
        if not weather_data or not air_data:
            logger.error("날씨 또는 대기질 데이터가 없어 저장할 수 없습니다.")
            return False
            
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO environment_data 
                    (temp, main, weather_desc, pm10, pm25, khai_grade)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (
                    weather_data['temp'],
                    weather_data['main'],
                    weather_data['weather_desc'],
                    air_data['pm10'],
                    air_data['pm25'],
                    air_data['khai_grade']
                ))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"환경 정보 저장 실패: {str(e)}")
            return False
        finally:
            conn.close()

    def get_latest_environment(self):
        """최신 환경 정보 조회"""
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT temp, main, weather_desc, pm10, pm25, khai_grade, created_at
                    FROM environment_data
                    ORDER BY created_at DESC
                    LIMIT 1
                ''')
                result = cursor.fetchone()
                logger.info(f"환경 정보 조회 결과: {result}")
                
                if not result:
                    logger.warning("환경 정보가 없습니다.")
                    return None
                
                return {
                    'temp': result['temp'],
                    'main': result['main'],
                    'weather_desc': result['weather_desc'],
                    'pm10': result['pm10'],
                    'pm25': result['pm25'],
                    'khai_grade': result['khai_grade'],
                    'timestamp': result['created_at'].isoformat() if result['created_at'] else None
                }
        except Exception as e:
            logger.error(f"환경 정보 조회 실패: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    def update_environment_data(self):
        """환경 정보 업데이트 및 저장"""
        try:
            weather_data = self.fetch_weather()
            air_data = self.fetch_air_quality()

            if weather_data and air_data:
                if self.save_environment_data(weather_data, air_data):
                    self.notify_clients({
                        'temp': weather_data['temp'],
                        'main': weather_data['main'],
                        'weather_desc': weather_data['weather_desc'],
                        'pm10': air_data['pm10'],
                        'pm25': air_data['pm25'],
                        'khai_grade': air_data['khai_grade'],
                        'timestamp': datetime.now().isoformat()
                    })
                    return True
            return False
        except Exception as e:
            logger.error(f"환경 정보 업데이트 실패: {str(e)}")
            return False

    def get_current_environment(self):
        """현재 환경 정보 조회"""
        try:
            # 먼저 최신 데이터 조회
            env = self.get_latest_environment()
            
            # 데이터가 없거나 10분 이상 지난 경우 새로운 데이터 조회
            if not env or (env.get('timestamp') and 
                (datetime.now() - datetime.fromisoformat(env['timestamp'])).total_seconds() > 600):
                logger.info("환경 정보가 없거나 오래되어 새로운 데이터를 조회합니다.")
                if self.update_environment_data():
                    env = self.get_latest_environment()
            
            return env
        except Exception as e:
            logger.error(f"현재 환경 정보 조회 실패: {str(e)}")
            return None

    def add_sse_client(self, client):
        """SSE 클라이언트 추가"""
        self.sse_clients.add(client)

    def remove_sse_client(self, client):
        """SSE 클라이언트 제거"""
        self.sse_clients.discard(client)

    def notify_clients(self, data):
        """SSE 클라이언트에게 데이터 전송"""
        for client in self.sse_clients:
            try:
                client.send(f"data: {json.dumps(data)}\n\n")
            except Exception as e:
                logger.error(f"SSE 클라이언트 알림 실패: {str(e)}")
                self.remove_sse_client(client)

# 싱글톤 인스턴스
environment_service = EnvironmentService() 