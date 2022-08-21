import math
import sys
from http import server

import requests as requests
from flask import Flask, Response, request
import pandas as pd
from os.path import exists
from primePy import primes
from youtube_search import YoutubeSearch as ys
from enum import IntEnum
import json as js


class ConversationHandler(IntEnum):
    START = 0
    FIND = 1
    DOWNLOAD_OPTION = 2
    AUDIO = 3
    VIDEO = 4
    

df = pd.DataFrame()
conversation_db = pd.DataFrame()

app = Flask(__name__)

# ---------------------------For Yarden------------------------------------------
# TOKEN = '5350437246:AAGKH4QokVbN6u0-FEduXOiTVNrBbjS1GqE'
# TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
#                            'https://2871-82-80-173-170.ngrok.io/message'.format(TOKEN)
# --------------------------------------------------------------------------------

# ---------------------------For Eitan-------------------------------------------

TOKEN = '5661253066:AAEX2EQg95zFw8fONhnB5MSUmPFqtcsdFYM'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=' \
                            'https://80ac-82-80-173-170.eu.ngrok.io/message'. \
    format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

# --------------------------------------------------------------------------------


@app.route('/sanity')
def sanity(): return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    state = 0
    json_got = request.get_json()
    chat_id = json_got['message']['chat']['id']
    client_name = json_got['message']['chat']['first_name']

    if chat_id in conversation_db['id'].values:
        state = conversation_db.loc[conversation_db['id'] == chat_id, 'handler'].values[0]
    print(state)
    command = (json_got['message']['text']).split()[0].lower()
    # command = (json_got['message']['text']).split()
    # if len(command) == 1 and state == ConversationHandler.FIND and command[0].lower() == 'no':
    #     command = command[0].lower()
    # else:
    #     command = (json_got['message']['text']).split()[0].lower()

    match state:
        case ConversationHandler.START:
            if command != '/start' and chat_id not in conversation_db['id'].values:
                reply = "In order to start a conversation with the bot, please use '/start' command."
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, reply))
            elif command == '/start':
                conversation_db.loc[len(conversation_db.index)] = [chat_id, 0, None, None]
                print(conversation_db)
                reply = "hello " + str(client_name) + "! \nI am Boti-Bot and i provide youtube search " \
                                                      "and download services :D \n i support the following commands:" \
                                                      "\n1. find <video name> - gets a link to a video in youtube by name." \
                                                      "\n2. audio <youtube link> - receive audio file of the youtube link." \
                                                      "\n3. video <youtube link> - receive video file of the youtube link."
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, reply))

            elif command == 'find':
                conversation_db.loc[conversation_db['id'] == chat_id, 'handler'] = ConversationHandler.FIND
                user_input = (json_got['message']['text']).split()[1:]
                user_input = ' '.join([str(word) for word in user_input])
                results = ys(user_input, max_results=3).to_dict()
                conversation_db.loc[conversation_db['id'] == chat_id, 'data'] = js.dumps(results[1:])
                link = 'https://www.youtube.com' + results[0]['url_suffix']
                conversation_db.loc[conversation_db['id'] == chat_id, 'cur_data'] = link
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, link))
                reply = "Is this the video you have been looking for? Please reply 'yes' or 'no'."
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, reply))

        case ConversationHandler.FIND:
            if command != 'yes' and command != 'no':
                reply = 'Please answer yes or no.'
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, reply))

            elif command == 'yes':
                conversation_db.loc[conversation_db['id'] == chat_id, 'handler'] = ConversationHandler.DOWNLOAD_OPTION
                conversation_db.loc[conversation_db['id'] == chat_id, 'data'] = None
                reply = "Do you want to download it? reply 'audio' for audio file only and 'video' for the video itself."
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                             .format(TOKEN, chat_id, reply))

            elif command == 'no':
                data = js.loads(conversation_db.loc[conversation_db['id'] == chat_id, 'data'][0])
                if len(data) == 0:
                    reply = "I couldn't find your video. Please check your spellings and try again. bye-bye!"
                    conversation_db.drop(conversation_db.index[conversation_db['id'] == chat_id], inplace=True)
                    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                 .format(TOKEN, chat_id, reply))
                else:
                    link = 'https://www.youtube.com' + data[0]['url_suffix']
                    conversation_db.loc[conversation_db['id'] == chat_id, 'cur_data'] = link
                    conversation_db.loc[conversation_db['id'] == chat_id, 'data'] = js.dumps(data[1:])
                    reply = "I am sorry to hear that. i will give you another link:"
                    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                 .format(TOKEN, chat_id, reply))
                    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                 .format(TOKEN, chat_id, link))

        case ConversationHandler.DOWNLOAD_OPTION:
            return

        case _:
             requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                          .format(TOKEN, chat_id, 'bye-bye!'))
    # if command == "/palindrome":
    #     user_input = (json_got['message']['text']).split()[1]
    #     result = palindrome(user_input)
    #     add_to_db(user_input)
    #
    # elif command == "/factorial":
    #     user_input = (json_got['message']['text']).split()[1]
    #     result = factorial(user_input)
    #     add_to_db(user_input)
    #
    # elif command == "/sqrt":
    #     user_input = (json_got['message']['text']).split()[1]
    #     result = sqrt(user_input)
    #     add_to_db(user_input)
    #
    # elif command == "/prime":
    #     user_input = (json_got['message']['text']).split()[1]
    #     result = prime(user_input)
    #     add_to_db(user_input)
    #
    # elif command == "/popular":
    #     result = pd.to_numeric(df.loc[df['appearance'].idxmax()][0])
    #
    # elif command == "/exit":
    #     df.to_hdf('bot_db.h5', 'data')
    #     result = "Bye Bye"
    #
    # elif command == "find":
    #     user_input = (json_got['message']['text']).split()[1:]
    #     user_input = ' '.join([str(word) for word in user_input])
    #     results = ys(user_input, max_results=3).to_dict()
    #     for v in results:
    #         result = 'https://www.youtube.com' + v['url_suffix']
    #         break
    # else:
    #     result = "command not recognized"
    #
    # requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    #              .format(TOKEN, chat_id, result))
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
        df = pd.DataFrame(columns=['id', 'handler', 'cur_data', 'data'])
    if exists('conversation.csv'):
        conversation_db = pd.read_csv('conversation.csv')
    else:
        conversation_db = pd.DataFrame(columns=['id', 'handler', 'cur_data', 'data'])
    app.run(port=5002)
