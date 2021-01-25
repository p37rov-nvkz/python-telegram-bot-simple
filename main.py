import os 
import requests
import json

from parser import get_alarm
from parser import AVR_URL

token = os.getenv('TOKEN')
URL = f"https://api.telegram.org/bot{token}/"


def get_updates() -> dict:
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()

# Получить данные обновлений
def get_last_message(d: dict) -> dict:
    results: list = d['result']
    last_result = results[-1]
    message = last_result['message']
    chat = message['from']
    chat_id = chat['id']
    text = message['text']
    return {'chat_id':chat_id, 'text':text}


def send_message(chat_id: int, text: str):
    url = URL + 'sendMessage?chat_id='+str(chat_id)+'&text='+text
    print(url)
    r = requests.get(url)


def main():
    try:
        updates = get_updates()
        last_message = get_last_message(updates)
    except:
        updates = dict()
        last_message = dict()
    while(True):
        try:
            updates = get_updates()
            updated_last = get_last_message(updates)
            if last_message != updated_last:
                #print(updated_last['chat_id'])
                #print(updated_last['text'])
                alarms = get_alarm(AVR_URL)
                for alarm in alarms:
                    text = ''
                    for row in alarm:
                        text += row + '\n'
                    send_message(updated_last['chat_id'], text)
                last_message = updated_last

        except:
            continue


if __name__ == '__main__':
    main()
