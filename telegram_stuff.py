from datetime import datetime
import json
from resources.credentials import main_url
from redis_stuff.main import redis_cli
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
                - Add CodeWars API
            
            Done
        """
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': 'Enter your username:'}
        resp = requests.get(main_url + method, params)
    elif message[0] != '/':
        """
            TODO:
                - Add verification if len of list is less than 1
                
            Done
        """
        try:
            telegram_user_id = data['message']['from']['id']

            codewars_nickname = message

            if len(redis_cli.lrange(telegram_user_id, 0, -1)) > 0:
                print('exists')
                pass
            else:
                get_codewars_user_url = f'https://www.codewars.com/api/v1/users/{codewars_nickname}/'
                codewars_user = requests.get(get_codewars_user_url).json()

                if codewars_user['success'] == False:
                    print('LOX')
                else:
                    honor = codewars_user['honor']
                    redis_cli.lpush(telegram_user_id, *[codewars_nickname, honor])
                    print('pushed')

                    method = 'sendMessage'
                    params = {'chat_id': chat_id, 'text': 'Nickname was added successfully.'}
                    resp = requests.get(main_url + method, params)

        except IndexError:
            method = 'sendMessage'
            params = {'chat_id': chat_id, 'text': 'Enter correct nickname.'}
            resp = requests.get(main_url + method, params)

    elif message == '/team_of_the_week':
        """
            TODO:
                - Create weekly rating
            Done
            
            TODO:
                - add else
                - create function which executes once a week
                - in other cases it shows cached statistics
            Done
            
        """

        with open('week_statistics.json', 'r') as f:
            week_statistics = json.load(f)

        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': week_statistics}
        resp = requests.get(main_url + method, params)

    elif message == '/best_warriors':
        """
            TODO:
                - Create total rating
                Retrieve total honor directly from CodeWars !! not from redis !!
                
            Done!!!
        """
        total_rating = {}

        telegram_users_id = redis_cli.keys("*")
        for i in telegram_users_id:
            i = i.decode('utf-8')
            codewars_nickname_encoded = redis_cli.lrange(i, -1, -1)[0]
            codewars_nickname = codewars_nickname_encoded.decode('utf-8')

            get_codewars_user_url = f'https://www.codewars.com/api/v1/users/{codewars_nickname}/'
            codewars_user = requests.get(get_codewars_user_url).json()
            total_honor = codewars_user['honor']

            total_rating.update({i: {'nick': codewars_nickname, 'total_honor': total_honor}})

        method = 'sendMessage'
        text = ''

        for i in total_rating:
            text += 'username: ' + i + 'nick: ' + total_rating[i]['nick'] + 'total_honor: ' + str(total_rating[i]['total_honor']) + '\n'

        params = {'chat_id': chat_id, 'text': text}
        resp = requests.get(main_url + method, params)
