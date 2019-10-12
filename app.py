from telegram_stuff import write_json, get_json, menu

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        r = request.get_json()
        write_json(r)
        menu(r)
        return jsonify(get_json())

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
