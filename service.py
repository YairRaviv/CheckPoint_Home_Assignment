from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import asyncio
import math
import time
import os
import json

app = Flask(__name__)
api = Api(app)

# keywords is a dictionary that holds every previous data
global keywords
CHECKPOINT = "checkpoint"
AVANAN = "avanan"
EMAIL = "email"
SECURITY = "security"


# this class is responsible for the entry - /localhost/api/v1/events
class Events(Resource):

    # posts requests handler
    def post(self):
        global keywords
        data = request.get_data().decode('UTF-8').split()

        # counting the occurrence of the key words in the given sentence
        tmp_words_counter = [0, 0, 0, 0]
        for word in data:
            if word.lower() == CHECKPOINT:
                tmp_words_counter[0] += 1
            elif word.lower() == AVANAN:
                tmp_words_counter[1] += 1
            elif word.lower() == EMAIL:
                tmp_words_counter[2] += 1
            elif word.lower() == SECURITY:
                tmp_words_counter[3] += 1

        # the current second is the key for the given post request
        time_in_sec = str(math.floor(time.time()))

        # checking if there is already data at the last second
        if time_in_sec not in keywords:
            keywords[time_in_sec] = {CHECKPOINT: 0, AVANAN: 0, EMAIL: 0, SECURITY: 0}

        # updating the keywords dictionary with the new data
        keywords[time_in_sec][CHECKPOINT] += tmp_words_counter[0]
        keywords[time_in_sec][AVANAN] += tmp_words_counter[1]
        keywords[time_in_sec][EMAIL] += tmp_words_counter[2]
        keywords[time_in_sec][SECURITY] += tmp_words_counter[3]

        # update the persistency json file
        f = open("words.json", "wt")
        json.dump(keywords, f)
        f.close()
        return "successful update"


# this class is responsible for the entry - /localhost/api/v1/stats
class Status(Resource):
    def get(self):
        global keywords

        # calculate the relevant time interval
        interval = request.args.get("interval")
        current_time = math.floor(time.time())
        start_time = current_time - int(interval)

        # iterate over the last 'interval' seconds as keys ,
        # and checks if there is previous data in this time interval
        ans = {"checkpoint": 0, "avanan": 0, "email": 0, "security": 0}
        for i in range(start_time, current_time):
            str_i = str(i)
            if str_i in keywords.keys():
                for item in keywords.get(str_i):
                    ans[item] += keywords[str_i][item]
        return ans


def main():
    global keywords
    keywords = load_words_from_json()
    api.add_resource(Events, '/api/v1/events')
    api.add_resource(Status, '/api/v1/stats')
    app.run(host="localhost", port=80, debug=True)


# this function checks if there is an exist file with previous data from previous posts
# if exist - loads it.
# else - create json file for persistence
def load_words_from_json():
    if not os.path.exists("words.json"):
        f = open("words.json", "wt")
        json.dump({}, f)
        f.close()
        return {}
    else:
        try:
            with open("words.json", "r") as file:
                data = json.load(file)
                return data
        except IOError as e:
            print(e)


main()
