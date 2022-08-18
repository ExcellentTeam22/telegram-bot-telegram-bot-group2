import requests as requests
from flask import Flask, Response, request

app = Flask(__name__)

TOKEN = '5350437246:AAGKH4QokVbN6u0-FEduXOiTVNrBbjS1GqE'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            ' https://807f-82-80-173-170.eu.ngrok.io\/message'. \
    format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                       .format(TOKEN, chat_id, "Got it"))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
