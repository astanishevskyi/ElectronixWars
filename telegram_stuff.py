import json
from resources.credentials import main_url
import requests


def write_json(data):
    with open('response.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_json():
    with open("response.json", "r") as read_file:
        data = json.load(read_file)
        return data


def menu(data):
    message = data['message']['text']
    chat_id = data['message']['chat']['id']
    if message == '/help':
        """
            TODO:
                - Write Help docs
        """
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': 'Help docs'}
        resp = requests.get(main_url + method, params)

    elif message == '/add_username':
        """
            TODO:
                - Add nickname in redis db
        """
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': 'Nickname was added successfully.'}
        resp = requests.get(main_url + method, params)

    elif message == '/team_of_the_week':
        """
            TODO:
                - Create weekly rating
        """
        pass

    elif message == '/best_warriors':
        """
            TODO:
                - Create total rating
        """
        pass
