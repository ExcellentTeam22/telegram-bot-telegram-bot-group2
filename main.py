import requests
from flask import Flask, Response, Request

app = Flask(__name__)

TOKEN = '5350437246:AAGKH4QokVbN6u0-FEduXOiTVNrBbjS1GqE'
TELEGRAM_INIT_WEBHOOK_URL ='https://api.telegram.org/bot{}/setWebhook?url=https://45bd-82-80-173-170.eu.ngrok.io/message'.format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

# 'https://api.telegram.org/bot5350437246:AAGKH4QokVbN6u0-FEduXOiTVNrBbjS1GqE/setWebhook?url=https://008d-5-28-184-223.eu.ngrok.io/message'

# @app.route('/sanity')
# def sanity():return "Server is running"

# @app.route('/message', methods=["POST"])
# def handle_message():
#     print("got message")
#     chat_id = Request.get_json()['message']['chat']['id']
#     res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
#                        .format(TOKEN, chat_id, "Got it!!!! :) "))
#     return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
