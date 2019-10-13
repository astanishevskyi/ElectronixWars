from datetime import datetime
from telegram_stuff import write_json, get_json, menu
from weekly_stat import weekly_differ_rating
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        r = request.get_json()
        write_json(r)
        menu(r)
        if datetime.today().weekday() == 6:
            if datetime.now().hour == 1:
                if datetime.now().minute == 1:
                    weekly_differ_rating()

        return jsonify(get_json())

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
