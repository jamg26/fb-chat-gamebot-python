import subprocess
# from google.cloud.speech import types
# from google.cloud.speech import enums
from google.cloud import speech
from google.cloud import translate
# from google.cloud.vision import types
# from google.cloud import vision
# import sys
# import re
import io
# import argparse
# import fbchat
import requests
import base64
import random
from time import sleep
from random import shuffle
from fbchat import Client
from fbchat.models import *
import lyricwikia
from lyricwikia import LyricsNotFound
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from math import *
import urllib.request
# from urllib.parse import quote

# from urllib.parse import quote
# import mysql.connector
import os
# import getpass
from pythonping import ping
# import time
# from pprint import pprint
# import base64
import wikipedia
import lyricsgenius
# ==== MY OWN ORGANIZED FUNCTION ====
from fb_normal.define import *
from fb_normal.meme import *


# face recognition
# import face_recognition as fr
# import os
# import cv2
# import face_recognition
# import numpy as np


# mongodb
import pymongo
mclient = pymongo.MongoClient(
    "mongodb+srv://jamg:jamuel26@jamg-cluster-ccgrf.gcp.mongodb.net/test?retryWrites=true")


# Imports the Google Cloud client library

# speech recognition


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "json/YoutubeAPI-8315fef19e56.json"

# my_db = mysql.connector.connect(
#     host="35.187.240.251",
#     user="jamg",
#     passwd="jamuel26",
#     database="bot"
# )

# my_cursor = my_db.cursor()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def speechtotext(path):
    res = "audio/converted.wav"
    subprocess.call(["ffmpeg", "-y", "-i", path, res])

    client = speech.SpeechClient()

    speech_file = os.path.join(
        os.path.dirname(__file__),
        './',
        res)

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US',
        audio_channel_count=1,)

    response = client.recognize(config, audio)

    return response.results[0].alternatives[0].transcript


# image recognition
# def get_encoded_faces():
#     """
#     looks through the faces folder and encodes all
#     the faces

#     :return: dict of (name, image encoded)
#     """
#     encoded = {}

#     for dirpath, dnames, fnames in os.walk("./faces"):
#         for f in fnames:
#             if f.endswith(".jpg") or f.endswith(".png"):
#                 face = fr.load_image_file("faces/" + f)
#                 encoding = fr.face_encodings(face)[0]
#                 encoded[f.split(".")[0]] = encoding

#     return encoded


# def unknown_image_encoded(img):
#     """
#     encode a face given the file name
#     """
#     face = fr.load_image_file("faces/" + img)
#     encoding = fr.face_encodings(face)[0]

#     return encoding


# def classify_face(im):
#     """
#     will find all of the faces in a given image and label
#     them if it knows what they are

#     :param im: str of file path
#     :return: list of face names
#     """
#     faces = get_encoded_faces()
#     faces_encoded = list(faces.values())
#     known_face_names = list(faces.keys())

#     img = cv2.imread(im, 1)
#     #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
#     #img = img[:,:,::-1]

#     face_locations = face_recognition.face_locations(img)
#     unknown_face_encodings = face_recognition.face_encodings(
#         img, face_locations)

#     face_names = []
#     for face_encoding in unknown_face_encodings:
#         # See if the face is a match for the known face(s)
#         matches = face_recognition.compare_faces(faces_encoded, face_encoding)
#         name = "Unknown"

#         # use the known face with the smallest distance to the new face
#         face_distances = face_recognition.face_distance(
#             faces_encoded, face_encoding)
#         best_match_index = np.argmin(face_distances)
#         if matches[best_match_index]:
#             name = known_face_names[best_match_index]

#         face_names.append(name)

#         for (top, right, bottom, left), name in zip(face_locations, face_names):
#             # Draw a box around the face
#             cv2.rectangle(img, (left-20, top-20),
#                           (right+20, bottom+20), (255, 0, 0), 2)

#             # Draw a label with a name below the face
#             cv2.rectangle(img, (left-20, bottom - 15),
#                           (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(img, name, (left - 20, bottom + 15),
#                         font, 1.0, (255, 255, 255), 2)

#     # Display the resulting image
#     cv2.imwrite(f"output/{face_names[0]}.jpg", img)
#     return face_names
#     # while True:

#     # cv2.imshow('Video', img)
#     # if cv2.waitKey(1) & 0xFF == ord('q'):
#     #     return face_names

# image recognition end


def synonyms(word):
    r = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
    r = r.json()
    res = []
    for x in r:
        res.append(x['word'])
    res = "\n".join(res)
    return res


def removebg(path):
    p = 'image/no-bg.png'
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(path, 'rb')},
        data={'size': 'auto', 'bg_color': 'ffffff'},
        headers={'X-Api-Key': 'tipKyv76Xbda34JRGhicRqnm'},
    )
    if response.status_code == requests.codes.ok:
        with open(p, 'wb') as out:
            out.write(response.content)
            return p
    else:
        if(response.status_code == 402):
            response2 = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(path, 'rb')},
                data={'size': 'auto', 'bg_color': 'ffffff'},
                headers={'X-Api-Key': 'vzzrFNN27Whhc4UqE4a3kenv'},
            )
            if response2.status_code == requests.codes.ok:
                with open(p, 'wb') as out:
                    out.write(response2.content)
                    return p
            else:
                if(response.status_code == 402):
                    response2 = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        files={'image_file': open(path, 'rb')},
                        data={'size': 'auto', 'bg_color': 'ffffff'},
                        headers={'X-Api-Key': 'JZtho2oJ5Nfp29t6nM8W13zS'},
                    )
                    if response2.status_code == requests.codes.ok:
                        with open(p, 'wb') as out:
                            out.write(response2.content)
                            return p
                    else:
                        print("Error:", response2.status_code, response2.text)
                        return 'error'
        else:
            print("Error:", response.status_code, response.text)
            return 'error'


def suggestquery(query):
    headers = {'Content-Type': 'application/json'}
    r = requests.get(
        f"http://suggestqueries.google.com/complete/search?output=toolbar&client=firefox&hl=en&q={query}", headers=headers)
    r = r.json()
    return r[1][0]


def imgsearch(query):
    r = requests.get("https://api.qwant.com/api/search/images",
                     params={
                         'count': 50,
                         'q': query,
                         't': 'images',
                         'safesearch': 1,
                         'locale': 'en_US',
                         'uiv': 4
                     },
                     headers={
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                     }
                     )
    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response]
    return random.choice(urls)


def translation(text):
    # Instantiates a client
    translate_client = translate.Client()
    # The target language
    target = 'tl'
    # Translates some text
    translation = translate_client.translate(
        text,
        target_language=target)
    return translation['translatedText']


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    texts = response.text_annotations
    return texts[0].description


def vtotal(urls):
    params = {
        'apikey': '9d353804f5e793903b4b5b22ab85af3f81baede416146974ed5538b59c260481', 'url': urls}
    response = requests.post(
        'https://www.virustotal.com/vtapi/v2/url/scan', data=params)
    json_response = response.json()

    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "gzip,  My Python requests library example client or username"
    }
    params = {
        'apikey': '9d353804f5e793903b4b5b22ab85af3f81baede416146974ed5538b59c260481', 'resource': urls}
    response = requests.post('https://www.virustotal.com/vtapi/v2/url/report',
                             params=params, headers=headers)
    json_response = response.json()
    return f"detected {json_response['positives']} out of {json_response['total']} viruses."


def sms(num, msg):
    url = 'https://www.itexmo.com/php_api/api.php'
    params = {'1': num, '2': f'{msg}\n\n\n\n\n\n\n',
              '3': 'TR-JAMUE321619_FPVNQ'}
    requests.post(url, data=params, verify=False)


def mac_address(mac):
    url = f"https://api.macaddress.io/v1?apiKey=at_uLSLgGGS1cqXlILgyCPyGC561SLf5&output=json&search={mac}"
    get = requests.get(url)
    data = get.json()
    return data


def mobile_prefixes(number):
    smart_tnt = ["0813", "0907", "0908", "0909", "0910", "0911", "0912", "0913", "0914", "0918", "0919", "0920", "0921",
                 "0928", "0929", "0930", "0938", "0939", "0940", "0946", "0947", "0948", "0949", "0950", "0951", "0970",
                 "0981", "0989", "0992", "0998", "0999"]
    globe_tm = ["0817", "0905", "0906", "0915", "0916", "0917", "0926", "0927", "0935", "0936", "0945", "0955", "0956",
                "0965", "0966", "0967", "0975", "0977", "0994", "0995", "0997"]
    sun = ["0922", "0923", "0924", "0925", "0931", "0932",
           "0933", "0934", "0941", "0942", "0943", "0944"]
    if number in smart_tnt:
        return "Smart or Talk N' Text"
    if number in globe_tm:
        return "Globe or TM"
    if number in sun:
        return "Sun Cellular"


def define(word):
    app_id = '0d6c4d8a'
    app_key = '642dd9bb994eb786bea9ac1453dedb07'
    language = 'en'
    url = f'https://od-api.oxforddictionaries.com:443/api/v2/entries/{language}/{word.lower()}'
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

    if r.status_code == 404:
        return "No data"
    else:
        da = r.json()
        try:
            res = da['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['definitions']
            return "".join(res)
        except KeyError:
            return "No data"


def rand_a():
    a = random.randint(0, 999)
    return a


def rand_b():
    b = random.randint(0, 999)
    return b


def encode_files(file_names):
    files_encoded = []
    for file_name in file_names:
        with open(file_name, "rb") as file:
            files_encoded.append(base64.b64encode(
                file.read()).decode("ascii"))
    return files_encoded


def identify_plant(file_names):
    images = encode_files(file_names)
    # see the docs for more optional attributes
    params = {
        "api_key": "MSyWuuFiIc3L57qGlBhUlHxqwl18GYXn7h5CUf1ihduwvePzdM",
        "images": images,
        "modifiers": ["crops_fast", "similar_images"],
        "plant_language": "en",
        "plant_details": ["common_names",
                          "url",
                          "name_authority",
                          "wiki_description",
                          "taxonomy",
                          "synonyms"],
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.plant.id/v2/identify",
                             json=params,
                             headers=headers)

    return response.json()


class BadBot(Client):

    thread_id = ""
    thread_type = ""
    admin_uid = "100005766793253"  # admin uid

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)
        self.sendMessage("Hello! You added me.", from_id,
                         thread_type=ThreadType.USER)

    def post_msg(self, msg):
        client.setTypingStatus(
            TypingStatus.TYPING, thread_id=self.thread_id, thread_type=self.thread_type)
        sleep(1)
        client.send(
            Message(text=f"{msg}"), thread_id=self.thread_id, thread_type=self.thread_type)

    def post_msg_b(self, msg):
        client.send(
            Message(text=f"{msg}"), thread_id=self.thread_id, thread_type=self.thread_type)

    def badbot_get(self, msg):
        db = mclient.bot
        col = db.badbot
        res = col.find({"question": msg})
        return res

    def badbot_add(self, question, msg):
        db = mclient.bot
        col = db.badbot
        data = {"question": question, "response": msg}
        col.insert_one(data)

        # sql = f"INSERT INTO badbot (question, answer) VALUES ('{question}', '{msg}')"
        # my_cursor.execute(sql)
        # my_db.commit()

    def onQprimer(self, **kwargs):
        client.changeNickname(
            "BadBot", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)

    def onMessage(self, author_id, message_object, thread_id, thread_type, metadata, msg, **kwargs):
        self.thread_id = thread_id
        self.thread_type = thread_type
        if author_id != self.uid:
            msg = message_object.text
            com = msg.lower()
            question = list(self.badbot_get(msg))

            ans = []
            count = 0
            for x in question:
                ans.append(x["response"])
                count += 1

            if ans != []:
                # cls()
                u_sender = self.fetchUserInfo(author_id)[author_id]
                ran = random.randint(0, count - 1)
                ans_send = ans[ran]
                if "{user}" in ans_send:
                    bot_post = ans_send.replace("{user}", u_sender.first_name)
                    self.post_msg(bot_post)
                else:
                    self.post_msg(ans_send)

            if "!add" in com:
                try:
                    com = com.split()
                    com = " ".join(com[1:])
                    com = com.split('#')
                    q = com[0]
                    a = com[1]
                except IndexError:
                    self.reactToMessage(message_object.uid, MessageReaction.NO)
                if not q:
                    self.reactToMessage(message_object.uid, MessageReaction.NO)
                elif not a:
                    self.reactToMessage(message_object.uid, MessageReaction.NO)
                else:
                    self.reactToMessage(message_object.uid,
                                        MessageReaction.YES)
                    self.post_msg_b(f"salamat sa pagturo!")
                    self.badbot_add(q, a)

            if "!help" in com:
                self.reactToMessage(message_object.uid, MessageReaction.YES)
                self.post_msg_b("COMMAND:\n\n!add hi#hello {user} im bot")

            if "!about" in com:
                self.post_msg_b("Facebook Bot: bad mode on")
                self.post_msg_b("Created by: Jamuel Galicia")

            if "!bad off" in com:
                # if author_id == self.admin_uid:
                self.reactToMessage(message_object.uid, MessageReaction.YES)
                self.post_msg_b("BadBot OFF")
                client.changeNickname(
                    "assistant", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)
                start_bot()
                # else:
                #     self.reactToMessage(message_object.uid, MessageReaction.NO)


class GameBot(Client):
    # main variables
    answer = ""  # game answer
    thread_id = ""  # game room id
    rounds = 1  # rounds
    users = {}  # list of users
    users_count = 1  # count of users
    joined = 0  # if user is joined
    question = ""  # game question
    admin_uid = "100005766793253"  # admin uid

    # game options default
    game_math = 0
    game_tt = 0
    game_all = 1
    game_opm = 0
    game_bugtong = 0
    game_lyrics = 0
    game_title = ""

    # misc
    game_tt_check = 0

    # next_game manager
    next_game = -1
    next_game_name = ""
    max_game_rounds = 50

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)
        self.sendMessage("Hello! You added me.",
                         from_id, thread_type=ThreadType.USER)

    def set_defaults(self):
        self.answer = ""  # game answer
        self.rounds = 1  # rounds
        self.question = ""  # game question

    def post_msg(self, msg):
        client.send(Message(text=f"{msg}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)

    def join_user(self, id, name):
        self.users[self.users_count] = [id, name, 0]
        self.users_count += 1

    def shuffle(self):
        x = [i for i in range(leng)]
        shuffle(x)
        shuff = []
        for y in x:
            shuff.append(word[y])
        shuff = "".join(shuff)
        self.question = f"{shuff}"
        self.repeat()

    def next_gamemode(self, game):
        if self.next_game > 0:
            self.next_game -= 1
        if self.next_game == 0:
            self.post_msg(f"Game changing to {game}")
            self.next_game = -1
            self.game_changer(game)

    def max_rounds(self):
        if self.rounds > self.max_game_rounds:
            self.post_msg("Congratulations!")
            high_score = 0
            for x in self.users:
                if self.users[x][2] > high_score:
                    high_score = self.users[x][2]
                    high_name = self.users[x][1]
            self.post_msg(f"{high_name} = {high_score}")
            self.post_msg(f"{high_name} is a genius!")
            for x in self.users:
                self.users[x][2] = 0
            self.set_defaults()
            # self.game_changer("all")
            sleep(3)
            self.changeNickname(
                "assistant", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)
            start_bot()

    def game_manager(self):
        self.next_gamemode(self.next_game_name)
        self.max_rounds()
        # main
        if self.game_math == 1:
            self.game_tt_check = 0
            m_pick = random.randint(1, 2)
            if m_pick == 1:
                self.game_title = "ADDITION\n"
                return self.math_add()
            if m_pick == 2:
                self.game_title = "SUBTRACTION\n"
                return self.math_difference()

        if self.game_tt == 1:
            self.game_tt_check = 1
            self.game_title = "ENGLISH\n"
            return self.text_twist()

        if self.game_opm == 1:
            self.game_tt_check = 0
            self.game_title = "GUESS THE ARTIST\n"
            return self.opm()

        if self.game_bugtong == 1:
            self.game_title = "BUGTONG\n"
            self.game_tt_check = 0
            return self.bugtong()

        if self.game_lyrics == 1:
            self.game_title = "FILL THE LYRICS\n"
            self.game_tt_check = 0
            return self.lyric()

        if self.game_all == 1:
            a_pick = random.randint(1, 5)
            if a_pick == 1:
                self.game_tt_check = 0
                m_pick = random.randint(1, 2)
                if m_pick == 1:
                    self.game_title = "ADDITION\n"
                    return self.math_add()
                if m_pick == 2:
                    self.game_title = "SUBTRACTION\n"
                    return self.math_difference()
            if a_pick == 2:
                self.game_title = "ENGLISH\n"
                self.game_tt_check = 1
                return self.text_twist()
            if a_pick == 3:
                self.game_title = "GUESS THE ARTIST\n"
                self.game_tt_check = 0
                return self.opm()
            if a_pick == 4:
                self.game_tt_check = 0
                self.game_title = "BUGTONG\n"
                return self.bugtong()
            if a_pick == 5:
                self.game_title = "FILL THE LYRICS\n"
                self.game_tt_check = 0
                return self.lyric()

    def bugtong(self):
        with open('bugtong.txt', encoding="utf8") as f:
            bugtong = []
            for x in f:
                bugtong.append(x)
        ran = random.randint(0, 158)
        bugtong = bugtong[ran]
        bugtong = bugtong.split('#')
        self.question = bugtong[0]
        self.answer = bugtong[1].rstrip()
        client.send(Message(text=f"ROUND {self.rounds}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.repeat()

    def lyric(self):
        with open('lyrics.txt', encoding="utf8") as f:
            lyric = []
            count = 0
            for x in f:
                count += 1
                lyric.append(x)
        ran = random.randint(0, count - 1)
        lyric = lyric[ran]
        lyric = lyric.split('#')
        self.question = lyric[0]
        self.answer = lyric[1].rstrip()
        client.send(Message(text=f"ROUND {self.rounds}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.repeat()

    def opm(self):
        with open('opm.txt', 'r') as f:
            opm = []
            for x in f:
                opm.append(x)
        ran = random.randint(0, 551)
        opm = opm[ran]
        opm = opm.split(',')
        self.question = f"{opm[1]}"
        self.answer = opm[2].rstrip()
        client.send(Message(text=f"ROUND {self.rounds}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.repeat()

    def text_twist(self):
        global leng
        global word
        # opening file putting word in words
        with open('words.txt', 'r') as f:
            words = []
            for x in f:
                words.append(x)
        # generating random line in words.txt
        ran = random.randint(0, 2047)
        # getting a line of word
        word = words[ran]  # answer

        # getting length of a word
        leng = len(word) - 1
        # rumbling range of number
        x = [i for i in range(leng)]

        shuffle(x)

        # referencing numbers in every char
        shuff = []
        for y in x:
            shuff.append(word[y])

        # joining array of letters
        shuff = "".join(shuff)
        self.question = f"{shuff}"
        self.answer = word.rstrip()
        client.send(Message(text=f"ROUND {self.rounds}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.repeat()

    def math_add(self):
        a = rand_a()
        b = rand_b()
        self.answer = f"{a+b}"
        self.question = f"{a} + {b} = ?"
        client.send(Message(text=f"ROUND {self.rounds}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.repeat()

    def math_difference(self):
        a = rand_a()
        b = rand_b()
        self.answer = f"{a-b}"
        self.question = f"{a} - {b} = ?"
        client.send(Message(text=f"ROUND {self.rounds}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.repeat()

    def repeat(self):
        client.send(Message(text=f"{self.game_title}{self.question}"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        cls()
        print(self.answer)

    def onQprimer(self, **kwargs):
        client.changeNickname(
            "GameMaster", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        client.send(Message(text="Gamebot ON!"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.game_manager()

    def game_reset(self):
        self.game_all = 1
        self.game_tt = 0
        self.game_math = 0
        self.game_opm = 0
        self.game_bugtong = 0
        self.game_lyrics = 0

    def game_changer(self, game):
        self.game_reset()
        if game == "bugtong":
            self.game_bugtong = 1
        if game == "opm":
            self.game_opm = 1
        if game == "math":
            self.game_math = 1
        if game == "tt":
            self.game_tt = 1
        if game == "lyrics":
            self.game_lyrics = 1

    def next_game_name_changer(self, name):
        self.next_game = 3
        self.next_game_name = name
        self.post_msg(
            f"The game mode will change to {name} after three questions.")

    def onMessage(self, author_id, message_object, thread_id, thread_type, metadata, msg, **kwargs):
        command = message_object.text.lower()
        # gamebot only selected thread
        if thread_id == self.thread_id:
            if author_id != self.uid:
                if "!game off" in command:
                    if author_id == self.admin_uid:
                        self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                        self.send(Message(text="Gamebot OFF!"),
                                  thread_id=thread_id, thread_type=thread_type)
                        self.changeNickname(
                            "assistant", client.uid, thread_id=thread_id, thread_type=ThreadType.GROUP)
                        start_bot()
                if "!rounds" in command:
                    rounds = command.split()
                    try:
                        r = int(rounds[1])
                        self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                        self.max_game_rounds = r
                        self.post_msg(f"Max round changed to {r}")
                    except ValueError:
                        self.reactToMessage(
                            message_object.uid, MessageReaction.NO)

                if "!about" in command:
                    self.post_msg("Gamebot for facebook")
                    self.post_msg("Created by: Jamuel Galicia")
                if "!bugtong" in command:
                    self.reactToMessage(
                        message_object.uid, MessageReaction.YES)
                    self.next_game_name_changer("bugtong")
                if "!opm" in command:
                    self.reactToMessage(
                        message_object.uid, MessageReaction.YES)
                    self.next_game_name_changer("opm")
                if "!math" in command:
                    self.reactToMessage(
                        message_object.uid, MessageReaction.YES)
                    self.next_game_name_changer("math")
                if "!texttwist" in command:
                    self.reactToMessage(
                        message_object.uid, MessageReaction.YES)
                    self.next_game_name_changer("tt")
                if "!lyrics" in command:
                    self.reactToMessage(
                        message_object.uid, MessageReaction.YES)
                    self.next_game_name_changer("lyrics")
                if "!all" in command:
                    self.reactToMessage(
                        message_object.uid, MessageReaction.YES)
                    self.next_game_name_changer("all")
                if "!clue" in command:
                    if self.game_tt_check == 1:
                        self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                        self.send(Message(text=define(self.answer)),
                                  thread_id=thread_id, thread_type=thread_type)
                if "!shuffle" in command:
                    if self.game_tt_check == 1:
                        try:
                            self.shuffle()
                            self.react('yes')
                        except NameError:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.NO)

                if "!pass" in command:
                    self.reactToMessage(message_object.uid,
                                        MessageReaction.YES)
                    self.send(Message(text=f"the correct answer is:\n{self.answer}"),
                              thread_id=thread_id, thread_type=thread_type)
                    sleep(3)
                    self.game_manager()
                if "!repeat" in command:
                    self.reactToMessage(message_object.uid,
                                        MessageReaction.YES)
                    self.repeat()
                if "!join" in command:
                    join = 0
                    u_join = self.fetchUserInfo(author_id)[author_id]
                    try:
                        name = u_join.first_name
                        for x in self.users:
                            if author_id in self.users[x][0]:
                                join = 1
                        if join == 0:
                            self.react('yes')
                            self.join_user(author_id, name)
                            self.send(Message(text=f"{name} joined."),
                                      thread_id=thread_id, thread_type=thread_type)
                        else:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.NO)
                            self.send(Message(text="You already joined."),
                                      thread_id=thread_id, thread_type=thread_type)
                    except IndexError:
                        self.reactToMessage(
                            message_object.uid, MessageReaction.NO)
                        print("Index error")
                if "!score" in command:
                    self.reactToMessage(message_object.uid,
                                        MessageReaction.YES)
                    scores = ""
                    for x in self.users:
                        scores += self.users[x][1]
                        scores += " = "
                        scores += str(self.users[x][2])
                        scores += "\n"
                    self.post_msg(scores)
                if "!help" in command:
                    self.reactToMessage(
                        message_object.uid, MessageReaction.YES)
                    self.send(Message(text="COMMAND LIST:\n\n"
                                      "!join - join game\n\n"
                                      "!clue - texttwist word definition\n\n"
                                      "!shuffle - texttwist shuffle word\n\n"
                                      "!score - show scores\n\n"
                                      "!repeat - repeat question\n\n"
                                      "!shuffle - shuffle word letters\n\n"
                                      "!pass - next question\n\n"
                                      "!rounds - set max rounds"),
                              thread_id=thread_id,
                              thread_type=thread_type)
                    self.send(Message(text=f"Pick a game\n!math\n!texttwist\n!opm\n!bugtong\n!lyrics\n!all"),
                              thread_id=self.thread_id, thread_type=ThreadType.GROUP)

                if self.answer in command:
                    self.joined = 0
                    command = command.split()
                    command = " ".join(command[0:])
                    for x in self.users:
                        if author_id in self.users[x]:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.LOVE)
                            self.users[x][2] += 1
                            self.send(Message(text=f"{self.users[x][1]} got the correct answer!\n{self.users[x][1]} = {self.users[x][2]}"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.joined = 1
                            self.rounds += 1
                            self.game_manager()
                    if self.joined == 0:
                        self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                        self.send(Message(text="Type !join to participate"),
                                  thread_id=thread_id, thread_type=thread_type)


class FacebookBot(Client):
    mirror = 0
    bot = 1  # activate bot
    thread_type = ThreadType.GROUP
    admin_uid = "100005766793253"
    bot_name = "!bot start"
    game = 0
    object_uid = ""
    thread_id = ""

    vision = 0
    removebg = 0
    # guessage = 0
    recognition = 0
    recognition_rename = 0
    guesswho = 0
    guesswho_upload = 0
    plant = 0

    # geoloc
    location = 0

    # groups
    bsit = "1503744573087777"
    rthb = "2288054797953239"
    testing = "2146979205353207"
    chuvaness = "1574454682870723"

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)
        self.sendMessage("Hello! you added me", from_id,
                         thread_type=ThreadType.USER)

    def searchExistUserLoc(self, id):
        db = mclient.bot
        col = db.location
        res = col.find_one({"id": id})
        return res

    def addloc(self, id, lat, lon):
        r = self.searchExistUserLoc(id)
        db = mclient.bot
        col = db.location
        try:
            if r['id'] == id:
                data = {"$set": {"lat": lat, "lon": lon}}
                col.update_one(r, data)
                cls()
                print('updated!')
                mclient.close()
        except:
            data = {"id": id, "lat": lat, "lon": lon}
            col.insert_one(data)
            cls()
            print('added!')
            mclient.close()

    def getloc(self, id):
        db = mclient.bot
        col = db.location
        res = col.find_one({"id": id})
        self.mapview(res['id'], res['lat'], res['lon'])
        self.streetview(res['id'], res['lat'], res['lon'])
        return self.getlocname(res['lat'], res['lon'])

    def mapview(self, id, lat, lon):
        endpoint = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=20&size=500x400&markers=size:mid|{lat}, {lon}&maptype=hybrid&key=REMOVED"
        r = requests.get(endpoint)
        with open(f'image/{id}_mapview.png', 'wb') as f:
            f.write(r.content)

    def streetview(self, id, lat, lon):
        endpoint = f"https://maps.googleapis.com/maps/api/streetview?location={lat}, {lon}&size=600x400&fov=120&source=outdoor&key=REMOVED"
        r = requests.get(endpoint)
        with open(f'image/{id}_streetview.png', 'wb') as f:
            f.write(r.content)

    def getlocname(self, lat, lon):
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat}, {lon}&key=REMOVED"
        r = requests.get(endpoint)
        r = r.json()
        return r['results'][0]['formatted_address']

    def onLiveLocation(self, mid, location, author_id, thread_id, thread_type, ts, msg):
        # cls()
        # self.sendMessage(f"{location}", thread_id, thread_type=ThreadType.GROUP)
        # print(location.latitude, location.longitude)
        if self.location == 1:
            self.location = 0
            if location.latitude != None:
                self.addloc(author_id, location.latitude, location.longitude)
                self.sendMessage("Your location has been added!",
                                 thread_id, thread_type=thread_type)
                self.sendMessage("!getlocation to verify",
                                 thread_id, thread_type=thread_type)

    def react(self, react):
        if react == "yes":
            self.reactToMessage(self.object_uid, MessageReaction.YES)
        if react == "no":
            self.reactToMessage(self.object_uid, MessageReaction.NO)
        if react == "love":
            self.reactToMessage(message_object.uid, MessageReaction.LOVE)

    def msg(self, msg):
        self.send(Message(text=f"{msg}"),
                  thread_id=self.thread_id, thread_type=self.thread_type)

    def onMessage(self, author_id, message_object, thread_id, thread_type, metadata, msg, **kwargs):
        if self.bot == 0:  # read if bot = 0
            if "!start" in message_object.text:  # if bot = 0 !start to make it 1
                self.markAsRead(thread_id)
                self.react('love')
                self.send(Message(text="Bot started!"),
                          thread_id=thread_id, thread_type=thread_type)
                self.bot = 1
                message_object.text = ""
        if self.bot == 1:  # read if bot = 1
            self.object_uid = message_object.uid
            self.thread_id = thread_id
            if thread_type == self.thread_type:  # if thread is group
                file_type = "%text"
                command = ""
                url = ""
                # getting filetype of the sended message
                try:
                    extension = msg["attachments"][0]["mimeType"]
                    if "image" in extension:
                        file_type = "%image"
                        url = msg["attachments"][0]["mercury"]["blob_attachment"]["large_preview"]["uri"]
                    if "application" in extension:
                        file_type = "%file"
                    if "audio" in extension:
                        file_type = "%audio"
                        url = msg["attachments"][0]["mercury"]["blob_attachment"]["playable_url"]
                except:
                    command = message_object.text.lower()
                if author_id != self.uid:
                    if file_type == "%text":  # if filetype is text
                        if self.recognition_rename == 1:
                            self.recognition_rename = 0
                            os.rename(f"faces/{thread_id}.jpg",
                                      f"faces/{command}.jpg")
                            self.msg(f"{command}'s image has been added.")
                            self.react('yes')

                        # provide random quotes
                        if "!meme help" == command:
                            self.msg(
                                f"type\n!meme id#text1#text2\n!meme id - list of all id")
                            self.react('yes')

                        if "!meme id" == command:
                            r = requests.get(
                                "https://api.imgflip.com/get_memes")
                            ids = []
                            res = r.json()
                            for x in res["data"]["memes"]:
                                ids.append(f"{x['id']} - {x['url']}")
                            ids = "\n".join(ids)
                            self.msg(ids)
                            self.react('yes')

                        if "!meme" in command:
                            if "#" in command:
                                try:
                                    t_id = command.split('#')[0].split()[1]
                                    msg1 = command.split('#')[1]
                                    msg2 = command.split('#')[2]
                                    img = Meme(t_id, msg1, msg2).make()
                                    self.sendRemoteImage(img, message=Message(text=''), thread_id=thread_id,
                                                         thread_type=thread_type)
                                    self.react('yes')
                                except:
                                    self.msg("Invalid id or parameters.")

                        if "!mirror on" in command:
                            if self.admin_uid == author_id:
                                self.mirror = 1
                                self.react('yes')
                                self.msg("Mirror bot on.")

                        if "!mirror off" in command:
                            if self.admin_uid == author_id:
                                self.mirror = 0
                                self.react('yes')
                                self.msg("Mirror bot off.")

                        # defining words
                        if "!define" in command:
                            result = Define(message_object.text).get()
                            self.msg(result)
                            self.react('yes')

                        # upload random images
                        if "!random image" in command:
                            url = "https://source.unsplash.com/random"
                            self.sendRemoteImage(url, message=Message(text=''), thread_id=thread_id,
                                                 thread_type=thread_type)
                            self.react('yes')

                        #  change group title
                        if "!title" in command:
                            title = message_object.text.split()
                            tit = " ".join(title[1:])
                            self.changeThreadTitle(
                                tit, thread_id=thread_id, thread_type=thread_type)
                            self.react('yes')

                        # change users nickname
                        if "!nickname" in command:
                            nickname = message_object.text.split()
                            nick = " ".join(nickname[1:])
                            self.changeNickname(
                                nick, author_id, thread_id=thread_id, thread_type=thread_type)
                            self.react('yes')

                        # search facebook
                        if "!search" in command:
                            try:
                                search = message_object.text.split()
                                searching = " ".join(search[1:])
                                user = self.searchForUsers(searching)[0]
                                self.msg(
                                    f"uid: {user.uid}\nname: {user.name}\nprofile: https://facebook.com/{user.uid}")
                                self.sendRemoteImage(
                                    user.photo, message=None, thread_id=thread_id, thread_type=thread_type)
                                self.react('yes')
                            except:
                                self.react('no')

                        if "!mod" in command:
                            try:
                                modulo = message_object.text.split()
                                mod = float(modulo[1]) % float(modulo[2])
                                self.msg(mod)
                                self.react('yes')
                            except:
                                self.react('no')

                        # search lyrics
                        if "!lyrics" in command:
                            try:
                                lyrics = message_object.text.split()
                                lyrics = " ".join(lyrics[1:])
                                genius = lyricsgenius.Genius(
                                    "8A2IemTA_-goTU98-UqjCGHaZCyEMkciN2NPn8DHfMKbmq0t9ilA-ekMlnnfWGR2")
                                try:
                                    lyrics = lyrics.split(',')
                                    song = genius.search_song(
                                        lyrics[0], lyrics[1])
                                except:
                                    song = genius.search_song(lyrics[0])
                                self.msg(song.lyrics)
                                self.react('yes')
                            except:
                                self.react('no')

                        # about bot
                        if "!about" in command:
                            self.msg("Virtual assistant for Facebook")
                            self.msg("Created by: Jamuel Galicia")
                            self.msg("Last Update: August 2020")
                            self.react('yes')

                        # pause bot
                        if "!pause" in command:
                            if author_id == self.admin_uid:
                                self.msg("Bot paused.")
                                self.bot = 0
                                self.react('yes')
                            else:
                                self.react('no')

                        # speak bot
                        if "!speak" in command:
                            self.react('yes')
                            data = message_object.text.split()
                            voice = " ".join(data[1:])
                            tts = gTTS(text=voice, lang='en')
                            path = f"audio/{voice}.mp3"
                            tts.save(path)
                            self.sendLocalFiles(
                                path, "", thread_id, thread_type)
                            os.remove(path)

                        # speak bot to a group
                        if "!msgto" in command:
                            try:
                                data = message_object.text.split()
                                t = data[1]
                                voice = " ".join(data[2:])
                                tts = gTTS(text=voice, lang='en')
                                path = f"audio/{voice}.mp3"
                                tts.save(path)
                                self.sendLocalFiles(
                                    path, "", t, thread_type)
                                os.remove(path)
                                self.react('yes')
                            except:
                                self.sendLocalFiles(
                                    path, "", t, ThreadType.USER)
                                os.remove(path)
                                self.react('yes')

                        # find network
                        if "!network" in command:
                            com = command.split()
                            try:
                                self.msg(mobile_prefixes(com[1]))
                                self.react('yes')
                            except FBchatFacebookError:
                                self.react('no')
                            except IndexError:
                                self.react('no')

                        # converting image to text
                        if "!write" in command:
                            text = message_object.text.split()
                            data = " ".join(text[1:])
                            img = Image.new('RGB', (150, 30),
                                            color=(255, 255, 255))
                            fnt = ImageFont.truetype(
                                'font/Roboto-Regular.ttf', 15)
                            d = ImageDraw.Draw(img)
                            d.text((10, 10), data, font=fnt, fill=(0, 0, 0))
                            path = "image/" + thread_id + '.png'
                            img.save(path)
                            self.sendLocalImage(path, message=Message(text=''), thread_id=thread_id,
                                                thread_type=thread_type)
                            os.remove(path)
                            self.react('yes')

                        # getting mac's provider
                        if "!mac" in command:
                            try:
                                com = command.split()
                                data = mac_address(com[1])
                                if data["vendorDetails"]["companyName"] != "":
                                    self.msg("VENDOR DETAILS\n\n"
                                             "Company Name: \n" + data["vendorDetails"]["companyName"] +
                                             "\n\nCompany Address: \n" +
                                             data["vendorDetails"]["companyAddress"] +
                                             "\n\nCountry Code: \n" +
                                             data["vendorDetails"]["countryCode"])
                                    self.react('yes')
                                else:
                                    self.react('no')
                            except IndexError:
                                self.react('no')

                        # conver url to qrcode
                        if "!qr" in command:
                            com = command.split()
                            base = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={com[1]}"
                            path = "image/" + thread_id + ".jpg"
                            urllib.request.urlretrieve(base, path)
                            self.sendLocalImage(path, message=Message(text=''), thread_id=thread_id,
                                                thread_type=thread_type)
                            os.remove(path)
                            self.react('yes')

                        # forwarding attachment
                        if "!forward" in command:
                            split = command.split()
                            url = "".join(split[1:])
                            try:
                                self.sendRemoteFiles(
                                    url, message=None, thread_id=thread_id, thread_type=thread_type)
                                self.react('yes')
                            except FBchatFacebookError:
                                self.react('no')

                        # sending sms
                        if "!sms" in command:
                            msg = command.split()
                            message = " ".join(msg[2:])
                            number = msg[1]
                            sms(number, message)
                            self.msg('Message sent.')
                            self.react('yes')

                        if "!game on" in command:
                            if author_id == self.admin_uid:
                                self.react('yes')
                                GameBot.users = {}
                                GameBot.thread_id = thread_id
                                game_bot.listen()

                        if "!bad on" in command:
                            if author_id == self.admin_uid:
                                self.react('yes')
                                BadBot.thread_id = thread_id
                                bad_bot.listen()

                        if "!bin" in command:
                            try:
                                b = command.split()
                                r = int(b[1])
                                r = bin(r)
                                r = r.replace("0b", "")
                                self.msg(r)
                                self.react('yes')
                            except:
                                self.react('no')

                        if "!hex" in command:
                            try:
                                b = command.split()
                                r = int(b[1])
                                r = hex(r)
                                r = r.replace("0x", "")
                                self.msg(r)
                                self.react('yes')
                            except:
                                self.react('no')

                        if "!oct" in command:
                            try:
                                b = command.split()
                                r = int(b[1])
                                r = oct(r)
                                r = r.replace("0o", "")
                                self.msg(r)
                                self.react('yes')
                            except:
                                self.react('no')

                        if "!sqrt" in command:
                            try:
                                b = command.split()
                                r = float(b[1])
                                r = sqrt(r)
                                self.msg(r)
                                self.react('yes')
                            except:
                                self.react('no')

                        if "!math" in command:
                            try:
                                b = command.split()
                                r = b[1]
                                r = eval(r)
                                self.msg(r)
                                self.react('yes')
                            except:
                                self.react('no')

                        if "!scanurl" in command:
                            command = command.split()
                            try:
                                vt = vtotal(command[1])
                                self.msg(vt)
                                self.react('yes')
                            except KeyError:
                                self.msg("Checking the url...")
                                self.msg("Scan again after few minutes.")
                                self.react('yes')

                        if "!vision" == command:
                            if self.vision == 0:
                                self.vision = 1
                                self.msg("Send your image.")
                                self.react('yes')

                        if "!plants" == command:
                            if self.plant == 0:
                                self.plant = 1
                                self.msg("Send your image.")
                                self.react('yes')

                        if "!translate" in command:
                            text = message_object.text.split()
                            word = " ".join(text[1:])
                            self.msg(translation(word))
                            self.react('yes')

                        if "!ping" in command:
                            command = command.split()
                            res = ping(command[1], verbose=True)
                            self.msg(f"average ping: {res.rtt_avg_ms}ms")
                            self.react('yes')

                        if "!image" in command:
                            q = command.split()
                            query = " ".join(q[1:])
                            try:
                                res = imgsearch(query)
                                self.sendRemoteImage(res, message=Message(text=''), thread_id=thread_id,
                                                     thread_type=thread_type)
                                self.react('yes')
                            except:
                                self.msg("Try again.")
                                self.react('no')

                        if "!spell" in command:
                            q = command.split()
                            query = " ".join(q[1:])
                            try:
                                res = suggestquery(query)
                                if res != query:
                                    self.msg(f"Did you mean {res}?")
                                    self.react('yes')
                                else:
                                    self.msg("The spelling was correct.")
                                    self.react('yes')
                            except:
                                self.react('no')

                        if "!removebg" == command:
                            if self.removebg == 0:
                                self.removebg = 1
                                self.msg("Send your image.")

                        # if "!guessage" == command:
                        #     if self.guessage == 0:
                        #         self.guessage = 1
                        #         self.send(Message(text=f"Please send your image."), thread_id=thread_id,
                        #                         thread_type=thread_type)
                        #     else:
                        #         self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if "!syn" in command:
                            try:
                                word = command.split()
                                self.msg(synonyms(word[1]))
                                self.react('yes')
                            except:
                                self.react('no')

                        # if "!train" == command:
                        #     try:
                        #         self.recognition = 1
                        #         self.send(Message(text=f"Please send your image to be trained"), thread_id=thread_id, thread_type=thread_type)
                        #     except:
                        #         self.reactToMessage(message_object.uid, MessageReaction.NO)

                        # if "!guesswho" == command:
                        #     try:
                        #         self.guesswho = 1
                        #         self.send(Message(text=f"Please send persons image"), thread_id=thread_id, thread_type=thread_type)
                        #     except:
                        #         self.reactToMessage(message_object.uid, MessageReaction.NO)

                        # if "!guesswho-img" == command:
                        #     if author_id == self.admin_uid:
                        #         try:
                        #             self.guesswho_upload = 1
                        #             self.send(Message(text=f"Please send persons image"), thread_id=thread_id, thread_type=thread_type)
                        #         except:
                        #             self.reactToMessage(message_object.uid, MessageReaction.NO)

                        if "!setlocation" == command:
                            self.location = 1
                            self.msg("Share your location.")
                            self.react('yes')

                        if "!getlocation" == command:
                            try:
                                self.msg(self.getloc(author_id))
                                self.sendLocalFiles(
                                    f"image/{author_id}_mapview.png", "", thread_id, thread_type)
                                self.sendLocalFiles(
                                    f"image/{author_id}_streetview.png", "", thread_id, thread_type)
                                self.react('yes')
                            except TypeError:
                                self.msg("No location info found.")
                                self.msg("!setlocation to add your location.")

                        if "!unplag" in command:
                            try:
                                word = command.split()
                                word = " ".join(word[1:])
                                url = "https://plagiarism-remover.p.rapidapi.com/api/rewrite"

                                payload = "{  \"sourceText\": \"" + \
                                    word + "\"}"
                                headers = {
                                    'x-rapidapi-host': "plagiarism-remover.p.rapidapi.com",
                                    'x-rapidapi-key': "fKF1gF6A8Hmshio5bYJ0MWDnKgRXp1HFSX7jsnmPs7rhcgCPmb",
                                    'content-type': "application/json",
                                    'accept': "application/json"
                                }

                                response = requests.request(
                                    "POST", url, data=payload, headers=headers)
                                res = response.json()
                                self.msg(res['NewText'])
                                self.react('yes')
                            except:
                                self.react('no')

                        if "!wiki" in command:
                            try:
                                word = command.split()
                                word = " ".join(word[1:])
                                res = wikipedia.summary(word)
                                self.msg(res)
                                self.react('yes')
                            except:
                                pass

                        # show commands
                        if "!commands" == command:
                            self.msg("COMMAND LIST:\n\n"
                                     "!random image - random image\n\n"
                                     "!define word - define a word\n\n"
                                     "!lyrics title, artist \n\n"
                                     "!title name - change chat title\n\n"
                                     "!nickname name - change your nickname\n\n"
                                     "!search name - search a user\n\n"
                                     "!speak words - speak bot\n\n"
                                     "!network 0930 - show network\n\n"
                                     "!write message\n\n"
                                     "!mac mac:address\n\n"
                                     "!qr link\n\n"
                                     "!forward file_link\n\n"
                                    #  "!sms {number} {message}\n\n"
                                     "!meme id#text1#text2\n\n"
                                     "!meme id - show all id\n\n"
                                     "!meme help\n\n"
                                     "!math formula\n\n"
                                     "!scanurl (url)\n\n"
                                     "!vision - image to text\n\n"
                                     "!translate word\n\n"
                                     "!image - search image\n\n"
                                     "!spell - suggest/autocomplete word\n\n"
                                     "!removebg - remove background from image\n\n"
                                     "!syn - get synonyms\n\n"
                                     # "!guesswho - guess person\n\n"
                                     "!setlocation - set your location\n\n"
                                     "!getlocation - get your location\n\n"
                                     "!unplag - unplagiarized text\n\n"
                                     "!wiki - wikipedia\n\n"
                                     "!plants - identify plant\n\n"
                                     "!about")
                            self.react('yes')
                        # else if words are not above
                        else:
                            # if mirror = 1
                            if self.mirror == 1:
                                self.send(
                                    message_object, thread_id=thread_id, thread_type=thread_type)
                                self.markAsDelivered(
                                    thread_id, message_object.uid)
                                self.markAsRead(thread_id)
                            else:
                                self.markAsDelivered(
                                    thread_id, message_object.uid)
                                self.markAsRead(thread_id)
                    if file_type == "%audio":
                        path = "audio/" + thread_id + "_temp.aac"
                        urllib.request.urlretrieve(url, path)
                        res = speechtotext(path)

                        #
                        if "hello" in res:
                            tts = gTTS(text="hi", lang='en')
                        if "hi" in res:
                            tts = gTTS(text="hello", lang='en')
                        if "your name" in res:
                            tts = gTTS(
                                text="I'm sorry i dont have name yet", lang='en')
                        if "how are you" in res:
                            tts = gTTS(text="I'm fine thank you.", lang='en')
                        if "thank" in res:
                            tts = gTTS(text="You're welcome.", lang='en')

                        if "+" in res or "plus" in res:
                            if "plus" in res:
                                res = res.replace("plus", "+")
                            self.send(Message(
                                text=f"{res}\n= {eval(res)}"), thread_id=thread_id, thread_type=thread_type)
                        if "-" in res or "minus" in res:
                            if "minus" in res:
                                res = res.replace("minus", "-")
                            self.send(Message(
                                text=f"{res}\n= {eval(res)}"), thread_id=thread_id, thread_type=thread_type)
                        if "/" in res or "divided" in res:
                            if "divided" in res:
                                res = res.replace("divided by", "/")
                            self.send(Message(
                                text=f"{res}\n= {eval(res)}"), thread_id=thread_id, thread_type=thread_type)
                        if "*" in res or "multiplied" in res:
                            if "multiplied" in res:
                                res = res.replace("multiplied by", "*")
                            self.send(Message(
                                text=f"{res}\n= {eval(res)}"), thread_id=thread_id, thread_type=thread_type)

                        path = f"audio/reply.mp3"
                        tts.save(path)
                        self.sendLocalFiles(path, "", thread_id, thread_type)

                    if file_type == "%image":
                        path = "image/" + thread_id + "_temp.jpg"
                        urllib.request.urlretrieve(url, path)
                        if self.vision == 1:
                            try:
                                self.vision = 0
                                self.msg(detect_text(
                                    f"image/{thread_id}_temp.jpg"))
                                self.react('yes')
                            except:
                                self.react('no')

                        if self.removebg == 1:
                            try:
                                self.removebg = 0
                                self.sendLocalFiles(
                                    removebg(f"image/{thread_id}_temp.jpg"), "", thread_id, thread_type)
                                self.react('yes')
                            except:
                                self.react('no')

                        if self.plant == 1:
                            try:
                                self.plant = 0
                                plant = identify_plant(
                                    [f"image/{thread_id}_temp.jpg"])['suggestions'][0]['plant_details']
                                common = ", ".join(plant['common_names'][0:])

                                self.send(Message(
                                    text=f"Scientific Name: \n{plant['scientific_name']}\nCommon Names: \n{common}"), thread_id=thread_id, thread_type=thread_type)

                                self.react('yes')
                            except Exception as e:
                                print(e)
                                self.react('no')

                        # if self.recognition == 1:
                        #     try:
                        #         self.recognition = 0
                        #         self.send(Message(text=f"Who is that person?"), thread_id=thread_id, thread_type=thread_type)
                        #         urllib.request.urlretrieve(url, f"faces/{thread_id}.jpg")
                        #         self.recognition_rename = 1
                        #     except:
                        #         self.reactToMessage(message_object.uid, MessageReaction.NO)
                        # if self.guesswho == 1:
                        #     try:
                        #         self.guesswho = 0
                        #         names = []
                        #         for x in classify_face(path):
                        #             names.append(x)
                        #         name = ", ".join(names)
                        #         if name == "Unknown":
                        #             self.send(Message(text=f"The person is not recognized\n\n!train to add"), thread_id=thread_id, thread_type=thread_type)
                        #         else:
                        #             self.send(Message(text=f"I think that person is {name}"), thread_id=thread_id, thread_type=thread_type)
                        #         #self.sendLocalFiles(f"output/{classify_face(path)[0]}.jpg", "", thread_id, thread_type)
                        #     except:
                        #         self.reactToMessage(message_object.uid, MessageReaction.NO)

                        # if self.guesswho_upload == 1:
                        #     try:
                        #         self.guesswho_upload = 0
                        #         names = []
                        #         for x in classify_face(path):
                        #             names.append(x)
                        #         name = ", ".join(names)
                        #         if name == "Unknown":
                        #             self.send(Message(text=f"The person is not recognized\n!train to add"), thread_id=thread_id, thread_type=thread_type)
                        #         else:
                        #             #self.send(Message(text=f"I think that person is {name}"), thread_id=thread_id, thread_type=thread_type)
                        #             self.sendLocalFiles(f"output/{classify_face(path)[0]}.jpg", "", thread_id, thread_type)
                        #     except:
                        #         self.reactToMessage(message_object.uid, MessageReaction.NO)

            else:
                if author_id != self.uid:
                    self.markAsDelivered(thread_id, message_object.uid)
                    self.markAsRead(thread_id)


def start_bot():
    global fb_bot
    global game_bot
    global bad_bot
    fb_bot = FacebookBot("", "", session_cookies=session_cookies)
    game_bot = GameBot("", "",  session_cookies=session_cookies)
    bad_bot = BadBot("", "", session_cookies=session_cookies)
    fb_bot.listen()


def main():
    cls()
    global client
    global session_cookies
    u_user = "jammy.jammy.9404362"  # input('Enter username: ')
    u_pw = "jamgbot4"  # getpass.getpass('Enter password: ')
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    client = Client(u_user, u_pw, user_agent=ua, max_tries=20)
    session_cookies = client.getSession()
    start_bot()


main()
