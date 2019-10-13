import json
from redis_stuff.main import redis_cli
import requests


def weekly_differ_rating():
    """
        TODO:
            - make it asynchronous
    """

    with open('week_statistics.json', 'w') as f:
        telegram_users_id = redis_cli.keys("*")

        for i in telegram_users_id:
            i = i.decode('utf-8')
            codewars_nickname_encoded = redis_cli.lrange(i, -1, -1)[0]
            codewars_nickname = codewars_nickname_encoded.decode('utf-8')
            old_honor_encoded = redis_cli.lrange(i, 0, 0)[0]
            old_honor = int(old_honor_encoded)

            get_codewars_user_url = f'https://www.codewars.com/api/v1/users/{codewars_nickname}/'
            codewars_user = requests.get(get_codewars_user_url).json()
            current_honor = codewars_user['honor']
            differ_honor = current_honor - old_honor

            json.dump({i: {'nickname': codewars_nickname, 'honor': differ_honor}}, fp=f, indent=4)
