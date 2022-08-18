import math
import sys
from http import server

import requests as requests
from flask import Flask, Response, request
import pandas as pd
from os.path import exists
from primePy import primes

df = pd.DataFrame()

app = Flask(__name__)

# ---------------------------For Yarden------------------------------------------
# TOKEN = '5350437246:AAGKH4QokVbN6u0-FEduXOiTVNrBbjS1GqE'
# TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
#                            'https://2871-82-80-173-170.ngrok.io/message'.format(TOKEN)
# --------------------------------------------------------------------------------

# ---------------------------For Eitan-------------------------------------------

TOKEN = '5661253066:AAEX2EQg95zFw8fONhnB5MSUmPFqtcsdFYM'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://5104-5-28-184-10.eu.ngrok.io/message'. \
    format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

# --------------------------------------------------------------------------------


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    json_got = request.get_json()
    chat_id = json_got['message']['chat']['id']
    command = (json_got['message']['text']).split()[0]

    if command == "/palindrome":
        user_input = (json_got['message']['text']).split()[1]
        result = palindrome(user_input)
        add_to_db(user_input)

    elif command == "/factorial":
        user_input = (json_got['message']['text']).split()[1]
        result = factorial(user_input)
        add_to_db(user_input)

    elif command == "/sqrt":
        user_input = (json_got['message']['text']).split()[1]
        result = sqrt(user_input)
        add_to_db(user_input)

    elif command == "/prime":
        user_input = (json_got['message']['text']).split()[1]
        result = prime(user_input)
        add_to_db(user_input)

    elif command == "/popular":
        result = pd.to_numeric(df.loc[df['appearance'].idxmax()][0])

    elif command == "/exit":
        df.to_hdf('bot_db.h5', 'data')
        result = "Bye Bye"

    else:
        result = "command not recognized"

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                 .format(TOKEN, chat_id, result))
    return Response("success")


def prime(num):
    """
    function to check if number is prime
    :param num: number to check
    :return: prime or not prime
    """
    return 'prime' if primes.check(int(num)) else 'not prime'


def palindrome(num):
    return 'Palindrome' if num == num[::-1] else 'Not Palindrome'


def factorial(num):
    num = int(num)
    i = 1
    while True:
        if num % i == 0:
            num //= i
        else:
            break
        i += 1

    return 'Factorial' if num == 1 else 'Not Factorial'


def sqrt(num):
    num = int(num)
    return 'False' if num < 0 else math.sqrt(num).is_integer()


def most_popular_num():
    max = 0
    max_key = 0
    for key, val in dict.items():
        if val > max:
            max = val
            max_key = key
    return f'The most popular number is {max_key}'


def add_to_db(user_input):
    if user_input in df['number'].values:
        df.loc[df['number'] == user_input, 'appearance'] += 1
    else:
        df.loc[len(df.index)] = [user_input, 1]


if __name__ == '__main__':
    if exists('bot_db.h5'):
        df = pd.read_hdf('bot_db.h5')
    else:
        df = pd.DataFrame(columns=['number', 'appearance'])
    app.run(port=5002)
