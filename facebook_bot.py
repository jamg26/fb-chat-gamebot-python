import fbchat
import requests
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
from urllib.parse import quote
import mysql.connector
import os
import getpass
from pythonping import ping
import time
from pprint import pprint
import base64

# mongodb
import pymongo
mclient = pymongo.MongoClient(
    "mongodb+srv://jamg:jamuel26@jamg-cluster-ccgrf.gcp.mongodb.net/test?retryWrites=true")



import argparse
import io
import re
import sys

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\jammm\\Documents\\jamgph-a2c23146675e.json"


my_db = mysql.connector.connect(
    host="35.187.240.251",
    user="jamg",
    passwd="jamuel26",
    database="bot"
)
my_cursor = my_db.cursor()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def synonyms(word):
    r = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
    r = r.json()
    # print(r[0]['word'])
    res = []
    for x in r:
      res.append(x['word'])
      # print(x['word'])
    res = "\n".join(res)
    return res


def guessage(url):
    # 1. Get your API token from https://aiception.com/dashboard
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aW1lIjoxNTYyNjQxOTc1LjI3MTQ1NSwiaWQiOjE0fQ.-keqe4Zt0I9FLTugfsYDeZheERsRBDY7pDG28OYF-ow'

    # 2. Let's find the approximate age of Taylor Swift from this image
    r = requests.post('https://aiception.com/api/v2.1/face_age',
                    auth=(token, 'password is ignored'),
                    json={'image_url': url})

    # 2b. The Response object r has a JSON response
    # print('Headers')
    # pprint(r.headers)

    #print('Server response to our POST request')
    # pprint(r.json())
    # {'Location': 'https://aiception.com/api/v2.1/face_age/12', 'message': 'age task created'}

    # The Location value is both in the headers and in the json body
    age_task_url = r.headers['Location']
    # age_task_url = r.json()['Location']  # is also fine


    # wait 2 seconds for aiception to complete the task
    time.sleep(2)

    # 3. Use the Location to get the age task
    r = requests.get(age_task_url, auth=(token, 'password is ignored'))
    x = r.json()
    # 3b. We now have an answer with the age of Taylor Swift
    #print('Server response to our GET request')
    # pprint(r.json())
    return x['answer']['age']


def removebg(path):
    p = 'image/no-bg.png'
    response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(path, 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'tipKyv76Xbda34JRGhicRqnm'},
    )
    if response.status_code == requests.codes.ok:
        with open(p, 'wb') as out:
            out.write(response.content)
            return p
    else:
        print("Error:", response.status_code, response.text)
        return 'error'


def suggestquery(query):
    headers = {'Content-Type': 'application/json'}
    r = requests.get(f"http://suggestqueries.google.com/complete/search?output=toolbar&client=firefox&hl=en&q={query}", headers=headers)
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
    return response.text_annotations[0].description

def vtotal(urls):
    params = {'apikey': '9d353804f5e793903b4b5b22ab85af3f81baede416146974ed5538b59c260481', 'url':urls}
    response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
    json_response = response.json()


    headers = {
    "Accept-Encoding": "gzip, deflate",
    "User-Agent" : "gzip,  My Python requests library example client or username"
    }
    params = {'apikey': '9d353804f5e793903b4b5b22ab85af3f81baede416146974ed5538b59c260481', 'resource':urls}
    response = requests.post('https://www.virustotal.com/vtapi/v2/url/report',
    params=params, headers=headers)
    json_response = response.json()
    return f"detected {json_response['positives']} out of {json_response['total']} viruses."



def meme(t_id, text0, text1):
    r = requests.post("https://api.imgflip.com/caption_image", data={'template_id': t_id,'username': 'jamg', 'password': 'jamuel26', 'text0': text0, 'text1': text1})
    r = r.json()
    return r["data"]["url"]


def sms(num, msg):
    url = 'https://www.itexmo.com/php_api/api.php'
    params = {'1': num, '2': f'{msg}\n\n\n\n\n\n\njamgph.com',
              '3': 'TR-JAMGP590720_ZDT9Y'}
    r = requests.post(url, data=params, verify=False)

def sms2(num, msg):
    url = 'https://www.itexmo.com/php_api/api.php'
    params = {'1': num, '2': f'{msg}\n\n\n\n\n\n\n',
              '3': 'TR-JACDC373780_PFEYY'}
    r = requests.post(url, data=params)

def sms3(num, msg):
    url = 'https://www.itexmo.com/php_api/api.php'
    params = {'1': num, '2': f'{msg}\n\n\n\n\n\n\n',
              '3': 'TR-KENTJ115195_69819'}
    r = requests.post(url, data=params)


def mysql_update(ind, msgs):
    sql = f"UPDATE crud SET message = '{msgs}' WHERE message = '{ind}'"
    my_cursor.execute(sql)
    my_db.commit()


def mysql_delete(msg):
    if msg == "all":
        sql = "DELETE FROM crud WHERE id != 0"
        my_cursor.execute(sql)
        my_db.commit()
    else:
        sql = f"DELETE FROM crud WHERE message = '{msg}'"
        my_cursor.execute(sql)
        my_db.commit()


def mysql_add(message):
    sql = f"INSERT INTO crud (message) VALUES ('{message}')"
    my_cursor.execute(sql)
    my_db.commit()


def mysql_get():
    my_cursor.execute("SELECT * FROM crud ORDER BY ID ASC")
    my_result = my_cursor.fetchall()
    res = []
    for x in my_result:
        res.append(x[1])
    res = "\n".join(res)
    return res


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

class BadBot(Client):

    thread_id = ""
    thread_type = ""
    admin_uid = "100005766793253" # admin uid
    

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)
        self.sendMessage("Hello! You added me.", from_id, thread_type=ThreadType.USER)


    def post_msg(self, msg):
        client.setTypingStatus(TypingStatus.TYPING, thread_id=self.thread_id, thread_type=self.thread_type)
        sleep(1)
        client.send(Message(text=f"{msg}"), thread_id=self.thread_id, thread_type=self.thread_type)
    
    def post_msg_b(self, msg):
        client.send(Message(text=f"{msg}"), thread_id=self.thread_id, thread_type=self.thread_type)
    
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
        client.changeNickname("BadBot", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)


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
                #cls()
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
                    self.reactToMessage(message_object.uid, MessageReaction.YES)
                    self.post_msg_b(f"salamat sa pagturo!")
                    self.badbot_add(q, a)

            if "!help" in com:
                self.reactToMessage(message_object.uid, MessageReaction.YES)
                self.post_msg_b("COMMAND:\n\n!add hi#hello {user} im bot")
            
            if "!about" in com:
                self.post_msg_b("PyBatibot: bad mode on")
                sleep(1)
                self.post_msg_b("Created by: Jamuel Galicia")

            if "!bad off" in com:
                #if author_id == self.admin_uid:
                self.reactToMessage(message_object.uid, MessageReaction.YES)
                self.post_msg_b("BadBot OFF")
                client.changeNickname("assistant", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)
                start_bot()
                # else:
                #     self.reactToMessage(message_object.uid, MessageReaction.NO)



class GameBot(Client):
    # main variables
    answer = "" # game answer
    thread_id = "" # game room id
    rounds = 1 # rounds
    users = {} # list of users
    users_count = 1 # count of users
    joined = 0 # if user is joined
    question = "" # game question
    admin_uid = "100005766793253" # admin uid

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
        self.answer = "" # game answer
        self.rounds = 1 # rounds
        self.question = "" # game question


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
            #self.game_changer("all")
            sleep(3)
            self.changeNickname("assistant", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)
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
                if m_pick ==2:
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
        client.send(Message(text=f"{self.game_title}{self.question}"), thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        cls()
        print(self.answer)

    def onQprimer(self, **kwargs):
        client.changeNickname("GameMaster", client.uid, thread_id=self.thread_id, thread_type=ThreadType.GROUP)
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
        self.post_msg(f"The game mode will change to {name} after three questions.")


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
                        self.changeNickname("assistant", client.uid, thread_id=thread_id, thread_type=ThreadType.GROUP)
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
                    self.post_msg("PyBatibot gamebot for facebook")
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
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
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
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
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
                    self.reactToMessage(message_object.uid, MessageReaction.YES)
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

    vision = 0
    removebg = 0
    guessage = 0

    # groups
    bsit = "1503744573087777"
    rthb = "2288054797953239"
    testing = "2146979205353207"
    chuvaness = "1574454682870723"

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)
        self.sendMessage("Hello! you added me", from_id, thread_type=ThreadType.USER)

    def onMessage(self, author_id, message_object, thread_id, thread_type, metadata, msg, **kwargs):
        if self.bot == 0:  # read if bot = 0
            if "!start" in message_object.text:  # if bot = 0 !start to make it 1
                self.markAsRead(thread_id)
                self.reactToMessage(message_object.uid, MessageReaction.LOVE)
                self.send(Message(text="Bot started!"),
                          thread_id=thread_id, thread_type=thread_type)
                self.bot = 1
                message_object.text = ""
        if self.bot == 1:  # read if bot = 1
            if thread_type == self.thread_type:  # if thread is group
                file_type = "%text"
                command = ""
                url = ""
                # getting filetype of the sended message
                try:
                    extension = msg["delta"]["attachments"][0]["mimeType"]
                    if "image" in extension:
                        file_type = "%image"
                        url = msg["delta"]["attachments"][0]["mercury"]["blob_attachment"]["large_preview"]["uri"]
                    if "application" in extension:
                        file_type = "%file"
                except IndexError:
                    command = message_object.text.lower()
                if author_id != self.uid:
                    if file_type == "%text":  # if filetype is text
                        # provide random quotes
                        if "!meme help" in command:
                            self.reactToMessage(message_object.uid, MessageReaction.YES)
                            self.send(Message(text=f"type\n!meme id#text1#text2\n!meme id - list of all id"),
                                    thread_id=thread_id, thread_type=thread_type)
                        if "!meme id" in command:
                            self.reactToMessage(message_object.uid, MessageReaction.YES)
                            r = requests.get("https://api.imgflip.com/get_memes")
                            tips = []
                            res = r.json()
                            for x in res["data"]["memes"]:
                                tips.append(f"{x['id']} - {x['url']}")
                            tips = "\n".join(tips)
                            self.send(Message(text=tips),
                                    thread_id=thread_id, thread_type=thread_type)
                        if "!meme" in command:
                            try:
                                data = command.split('#')
                                text0 = data[1]
                                text1 = data[2]
                                data = data[0].split()
                                t_id = data[1]
                                img = meme(t_id, text0, text1)
                                self.sendRemoteImage(img, message=Message(text=''), thread_id=thread_id,
                                                    thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except IndexError:
                                print("Index Error in !meme")
                        if "!mirror on" in command:
                            if self.admin_uid == author_id:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(Message(text="Mirror bot on!"),
                                        thread_id=thread_id, thread_type=thread_type)
                                self.mirror = 1
                        if "!mirror off" in command:
                            if self.admin_uid == author_id:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(Message(text="Mirror bot off!"),
                                        thread_id=thread_id, thread_type=thread_type)
                                self.mirror = 0
                        # defining words
                        if "!define" in command:
                            defined = message_object.text.split()
                            try:
                                if defined[2]:
                                    self.send(Message(text="You can only define 1 word"),
                                        thread_id=thread_id, thread_type=thread_type)
                            except IndexError:
                                try:
                                    d = define(defined[1])
                                    if d == "Invalid word":
                                        self.reactToMessage(
                                            message_object.uid, MessageReaction.NO)
                                    else:
                                        if d != "No data":
                                            self.reactToMessage(
                                                message_object.uid, MessageReaction.YES)
                                            self.send(
                                                Message(text=d), thread_id=thread_id, thread_type=thread_type)
                                        else:
                                            res = suggestquery(defined[1])
                                            self.send(
                                                Message(text=f"did you mean...\n{res}"), thread_id=thread_id, thread_type=thread_type)
                                except IndexError:
                                    self.reactToMessage(
                                        message_object.uid, MessageReaction.NO)
                        # upload random images
                        if "!random image" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            url = "https://source.unsplash.com/random"
                            self.sendRemoteImage(url, message=Message(text='Random image for you'), thread_id=thread_id,
                                                 thread_type=thread_type)
                        # when name called
                        if "batibot" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            reply = ["Unsa man ?", "oh?", "seg tawag", "hello"]
                            self.send(Message(text=random.choice(reply)),
                                      thread_id=thread_id, thread_type=thread_type)
                        # facebook messenger functions
                        #  change group title
                        if "!title" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            title = message_object.text.split()
                            tit = " ".join(title[1:])
                            self.changeThreadTitle(
                                tit, thread_id=thread_id, thread_type=thread_type)
                        # change users nickname
                        if "!nickname" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            nickname = message_object.text.split()
                            nick = " ".join(nickname[1:])
                            self.changeNickname(
                                nick, author_id, thread_id=thread_id, thread_type=thread_type)
                        # search facebook
                        if "!search" in command:
                            try:
                                search = message_object.text.split()
                                searching = " ".join(search[1:])
                                user = self.searchForUsers(searching)[0]
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(Message(text=f"uid: {user.uid}\nname: {user.name}\nprofile: https://facebook.com/{user.uid}"), thread_id=thread_id,
                                          thread_type=thread_type)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        if "!mod" in command:
                            try:
                                modulo = message_object.text.split()
                                mod = float(modulo[1]) % float(modulo[2])
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text=mod), thread_id=thread_id, thread_type=thread_type)
                            except FBchatFacebookError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except ValueError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # search lyrics
                        if "!lyrics" in command:
                            try:
                                lyrics = message_object.text.split()
                                lyrics = " ".join(lyrics[1:])
                                lyrics = lyrics.split(',')
                                fetch = lyricwikia.get_lyrics(
                                    lyrics[0], lyrics[1])
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text=fetch), thread_id=thread_id, thread_type=thread_type)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except LyricsNotFound:
                                self.send(Message(text="Lyrics not found"), thread_id=thread_id,
                                          thread_type=thread_type)
                        # about bot
                        if "!about" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(Message(text="Virtual assistant for Facebook"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.send(Message(text="Created by: Jamuel Galicia"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.send(Message(text="Last Update: May 14, 2019"),
                                      thread_id=thread_id, thread_type=thread_type)
                        # pause bot
                        if "!pause" in command:
                            if author_id == self.admin_uid:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text="Bot paused!"), thread_id=thread_id, thread_type=thread_type)
                                self.bot = 0
                            else:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # speak bot
                        if "!speak" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            data = message_object.text.split()
                            voice = " ".join(data[1:])
                            tts = gTTS(text=voice, lang='en')
                            path = f"audio/{voice}.mp3"
                            tts.save(path)
                            self.sendLocalFiles(
                                path, "", thread_id, thread_type)
                            os.remove(path)
                            
                        # speak bot to a group
                        if "!msgto" in message_object.text:
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
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                            except:
                                self.sendLocalFiles(
                                    path, "", t, ThreadType.USER)
                                os.remove(path)
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)

                        # find network
                        if "!network" in command:
                            com = command.split()
                            try:
                                self.send(Message(text=mobile_prefixes(com[1])), thread_id=thread_id,
                                          thread_type=thread_type)
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                            except FBchatFacebookError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # converting image to text
                        if "!write" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            text = message_object.text.split()
                            data = " ".join(text[1:])
                            img = Image.new('RGB', (150, 30),
                                            color=(255, 255, 255))
                            fnt = ImageFont.truetype(
                                '/font/Roboto-Regular.ttf', 15)
                            d = ImageDraw.Draw(img)
                            d.text((10, 10), data, font=fnt, fill=(0, 0, 0))
                            path = "image/" + thread_id + '.png'
                            img.save(path)
                            self.sendLocalImage(path, message=Message(text=''), thread_id=thread_id,
                                                thread_type=thread_type)
                            os.remove(path)
                        # getting mac's provider
                        if "!mac" in command:
                            try:
                                com = command.split()
                                data = mac_address(com[1])
                                if data["vendorDetails"]["companyName"] != "":
                                    self.reactToMessage(
                                        message_object.uid, MessageReaction.YES)
                                    self.send(Message(text="VENDOR DETAILS\n\n"
                                                           "Company Name: \n" + data["vendorDetails"]["companyName"] +
                                                           "\n\nCompany Address: \n" +
                                                           data["vendorDetails"]["companyAddress"] +
                                                           "\n\nCountry Code: \n" +
                                                           data["vendorDetails"]["countryCode"]),
                                              thread_id=thread_id, thread_type=thread_type)
                                else:
                                    self.reactToMessage(
                                        message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # conver url to qrcode
                        if "!qr" in command:
                            com = command.split()
                            base = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={com[1]}"
                            path = "image/" + thread_id + ".jpg"
                            urllib.request.urlretrieve(base, path)
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.sendLocalImage(path, message=Message(text=''), thread_id=thread_id,
                                                thread_type=thread_type)
                            os.remove(path)
                        # forwarding attachment
                        if "!forward" in command:
                            split = command.split()
                            url = "".join(split[1:])
                            try:
                                self.sendRemoteFiles(
                                    url, message=None, thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                            except FBchatFacebookError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        
                        # sending sms
                        if "!sms" in command:
                            msg = command.split()
                            message = " ".join(msg[2:])
                            number = msg[1]
                            sms(number, message)
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(Message(text="Message sent!"),
                                      thread_id=thread_id, thread_type=thread_type)
                        if "!game on" in command:
                            if author_id == self.admin_uid:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                GameBot.users = {}
                                GameBot.thread_id = thread_id
                                game_bot.listen()
                        if "!bad on" in command:
                            if author_id == self.admin_uid:
                                self.reactToMessage(
                                        message_object.uid, MessageReaction.YES)
                                BadBot.thread_id = thread_id
                                bad_bot.listen()
                        if "!bin" in command:
                            try:
                                b = command.split()
                                r = int(b[1])
                                r = bin(r)
                                r = r.replace("0b", "")
                                self.send(Message(text=f"{r}"), thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except ValueError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if "!hex" in command:
                            try:
                                b = command.split()
                                r = int(b[1])
                                r = hex(r)
                                r = r.replace("0x", "")
                                self.send(Message(text=f"{r}"), thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except ValueError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if "!oct" in command:
                            try:
                                b = command.split()
                                r = int(b[1])
                                r = oct(r)
                                r = r.replace("0o", "")
                                self.send(Message(text=f"{r}"), thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except ValueError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if "!sqrt" in command:
                            try:
                                b = command.split()
                                r = float(b[1])
                                r = sqrt(r)
                                self.send(Message(text=f"{r}"), thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except ValueError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if "!math" in command:
                            try:
                                b = command.split()
                                r = b[1]
                                r = eval(r)
                                self.send(Message(text=f"{r}"), thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except NameError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                                
                        if "!scanurl" in command:
                            command = command.split()
                            try:
                                vt = vtotal(command[1])
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(Message(text=vt), thread_id=thread_id,
                                    thread_type=thread_type)
                            except KeyError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(Message(text="Scanning url... Try again"), thread_id=thread_id,
                                      thread_type=thread_type)

                        if "!vision" == command:
                            if self.vision == 0:
                                self.vision = 1
                                self.send(Message(text="Please send your image!"), thread_id=thread_id,
                                        thread_type=thread_type)
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                        
                        if "!translate" in command:
                            text = message_object.text.split()
                            word = " ".join(text[1:])
                            self.send(Message(text=translation(word)), thread_id=thread_id,
                                        thread_type=thread_type)
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                        if "!ping" in command:
                            command = command.split()
                            res = ping(command[1], verbose=True)
                            self.send(Message(text=f"average ping: {res.rtt_avg_ms}ms"), thread_id=thread_id,
                                        thread_type=thread_type)
                            self.reactToMessage(message_object.uid, MessageReaction.YES)
                        if "!image" in command:
                            q = command.split()
                            query = " ".join(q[1:])
                            try:
                                res = imgsearch(query)
                                self.sendRemoteImage(res, message=Message(text=''), thread_id=thread_id,
                                                    thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except:
                                self.send(Message(text=f"Please try again.."), thread_id=thread_id,
                                        thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if "!spell" in command:
                            q = command.split()
                            query = " ".join(q[1:])
                            try:
                                res = suggestquery(query)
                                if res != query:
                                    self.send(Message(text=f"Did you mean...\n{res}"), thread_id=thread_id,
                                            thread_type=thread_type)
                                    self.reactToMessage(message_object.uid, MessageReaction.YES)
                                else:
                                    self.send(Message(text=f"You spelled it correctly."), thread_id=thread_id,
                                            thread_type=thread_type)
                                    self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if "!removebg" == command:
                            if self.removebg == 0:
                                self.removebg = 1
                                self.send(Message(text=f"Please send your image."), thread_id=thread_id,
                                                thread_type=thread_type)

                        if "!guessage" == command:
                            if self.guessage == 0:
                                self.guessage = 1
                                self.send(Message(text=f"Please send your image."), thread_id=thread_id,
                                                thread_type=thread_type)
                        if "!syn" in command:
                            try:
                                word = command.split()
                                self.send(Message(text=f"{synonyms(word[1])}"), thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                            except:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                                            
                        # show commands
                        if "!commands" == command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(Message(text="COMMAND LIST:\n\n"
                                                   "!random image - random image\n\n"
                                                   "!define word - define a word\n\n"
                                                   "!lyrics artist, song_title \n\n"
                                                   "!title name - change chat title\n\n"
                                                   "!nickname name - change your nickname\n\n"
                                                   "!search name - search a user\n\n"
                                                   "!speak words - speak bot\n\n"
                                                   "!network 0930 - show network\n\n"
                                                   "!write message\n\n"
                                                   "!mac mac:address\n\n"
                                                   "!qr link\n\n"
                                                   "!forward file_link\n\n"
                                                   "!sms {number} {message}\n\n"
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
                                                   "!guessage - guess your age\n\n"
                                                   "!syn - get synonyms\n\n"
                                                   "!about"),
                                      thread_id=thread_id,
                                      thread_type=thread_type)
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
                    if file_type == "%image":
                        path = "image/" + thread_id + "_temp.jpg"
                        urllib.request.urlretrieve(url, path)
                        if self.vision == 1:
                            try:
                                self.vision = 0
                                self.send(Message(text=detect_text(f"image/{thread_id}_temp.jpg")), thread_id=thread_id, thread_type=thread_type)
                                self.reactToMessage(
                                        message_object.uid, MessageReaction.YES)
                                self.send(Message(text=f"!vision to process another image."), thread_id=thread_id, thread_type=thread_type)
                            except:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if self.removebg == 1:
                            try:
                                self.removebg = 0
                                self.sendLocalFiles(removebg(f"image/{thread_id}_temp.jpg"), "", thread_id, thread_type)
                                self.reactToMessage(message_object.uid, MessageReaction.YES)
                                self.send(Message(text=f"!removebg to process another image."), thread_id=thread_id, thread_type=thread_type)
                            except:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
                        if self.guessage == 1:
                            try:
                                self.guessage = 0
                                self.send(Message(text=f"predicted age: {guessage(url)}"), thread_id=thread_id, thread_type=thread_type)
                                self.send(Message(text=f"!guessage to process another image."), thread_id=thread_id, thread_type=thread_type)
                            except:
                                self.reactToMessage(message_object.uid, MessageReaction.NO)
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
    u_user = input('Enter username: ')
    u_pw = getpass.getpass('Enter password: ')
    client = Client(u_user, u_pw)
    session_cookies = client.getSession()
    start_bot()
    


main()
