from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import moment

class Meetings_Worker():
    def __init__(self):
        load_dotenv()

        self.access_token = None
        self.meeting_param = {
                              "agenda": "Test757 Meeting", # Заголовок
                              "default_password": 'false', # Пароль по умолчанию
                              "duration": 30, # Продолжительность мин.
                              "password": "123456", # Пароль

                              "start_time": "2024-10-20T17:30:55", # Начало
                              "timezone": "Europe/Moscow", # Временная зона
                              "topic": "Test757 Meeting", # Тема
                              "type": 2 # Тип встречи (1 - Мгновенная встреча., 2 - Запланированная встреча., 3 - Повторяющаяся встреча без фиксированного времени. ,8 - Повторяющаяся встреча с фиксированным временем.)
                            }
        self.__get_token()

    def create_meeting(self):
        '''Создание встречи'''

        url=os.getenv("BASE_URL") + f'/users/me/meetings'
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        json_object = json.dumps(self.meeting_param, indent=4)
        try:
            response = requests.post(url, headers=headers, data=json_object)

            if not os.path.exists('meetings.csv') :
                with open('meetings.csv', 'x', encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Meeting ID', 'Join URL', 'Start Time'])

            with open('meetings.csv', "a", encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                req_data = response.json()
                writer.writerow([f'{req_data.get('id')}', f'{req_data.get('start_url')}', f'{req_data.get('start_time')}'])
            print('Meeeting создан ')
        except :
            print('Meeting не создан')


    def get_meeting_history(self):
        '''Получение прошедших встреч'''

        url = 'https://api.zoom.us/v2/users/me/meetings'
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        param = {
            'type' : 'previous_meetings',
            'from' : moment.date('1 week ago'),
            'to' : moment.now()
        }
        try:
            response = requests.get(url, headers=headers, params=param)
            data = response.json()['meetings']
            for meeting in data:
                print(meeting['topic'], meeting['start_time'], self.__get_meetings_ditail(meeting['id']))
        except:
            print('Не удалось получить прошедшие встречи')

    def __get_token(self):
        url = 'https://zoom.us/oauth/token'
        querystring = {
            'grant_type' :'account_credentials',
            'account_id' : f'{os.getenv("ACCOUNT_ID")}'
        }
        auth = HTTPBasicAuth(f'{os.getenv("CLIENT_ID")}', f'{os.getenv("CLIENT_SECRET")}')

        try:
            response = requests.post(url, params=querystring, auth=auth)
            self.access_token = response.json()['access_token']
        except:
            print('Не удается получить токен. Проверьте данные приложения')



    def __get_meetings_ditail(self, meetingId):
        url = os.getenv("BASE_URL") + f'/past_meetings/{meetingId}/'
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            return 0

        return response.json()['participants_count']



if __name__ == '__main__':
    worker = Meetings_Worker()
    worker.create_meeting()
    worker.get_meeting_history()



