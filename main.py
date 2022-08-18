import math
from re import split
import sympy.ntheory as nt
import requests as requests
from flask import Flask, Response, request

app = Flask(__name__)

TOKEN = '5350437246:AAGKH4QokVbN6u0-FEduXOiTVNrBbjS1GqE'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://3b2f-82-80-173-170.ngrok.io/message'. \
    format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    json_got = request.get_json()
    chat_id = json_got['message']['chat']['id']
    result = None
    command = (json_got['message']['text']).split()[0]
    user_input = (json_got['message']['text']).split()[1]

    if command == "/palindrome":
        result = palindrome(user_input)

    if command == "/factorial":
        result = factorial(user_input)

    if command == "/sqrt":
        result = sqrt(user_input)
    if command == "/prime":
        result = prime(user_input)

    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, result))
    return Response("success")


def prime(num):
    """
    function to check if number is prime
    :param num: number to check
    :return: prime or not prime
    """
    return 'prime' if nt.isprime(num) else 'not prime'


def palindrome(num):
    result = True if num == num[::-1] else False
    return result


def factorial(num):
    num = int(num)
    i = 1
    while True:
        if num % i == 0:
            num //= i
        else:
            break
        i += 1

    return True if num == 1 else False


def sqrt(num):
    num = int(num)
    return False if num < 0 else math.sqrt(num).is_integer()


if __name__ == '__main__':
    app.run(port=5002)
