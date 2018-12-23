import fbchat
import requests
import random
from random import shuffle
from fbchat import Client
from fbchat.models import *
import lyricwikia
from lyricwikia import LyricsNotFound
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import mysql.connector
import os
import _thread
my_db = mysql.connector.connect(
    host="35.187.240.251",
    user="jamg",
    passwd="jamuel26",
    database="bot"
)
my_cursor = my_db.cursor()


def sms(num, msg):
    url = 'https://www.itexmo.com/php_api/api.php'
    params = {'1': num, '2': f'{msg}\n\n\n\n\n\njamgph.com',
              '3': 'TR-JAMGP699769_CESFW'}
    r = requests.post(url, data=params)


def mysql_update(ind, msgs):
    sql = f"UPDATE crud SET message = '{msgs}'WHERE ID={ind}"
    my_cursor.execute(sql)
    my_db.commit()


def mysql_delete(ind):
    if ind == "all":
        sql = "DELETE FROM crud WHERE id != 0"
        my_cursor.execute(sql)
        my_db.commit()
    else:
        sql = f"DELETE FROM crud WHERE id = {ind}"
        my_cursor.execute(sql)
        my_db.commit()


def mysql_add(message):
    sql = f"INSERT INTO crud (message) VALUES ('{message}')"
    my_cursor.execute(sql)
    my_db.commit()


def mysql_get():
    my_cursor.execute("SELECT * FROM crud ORDER BY ID ASC")
    my_result = my_cursor.fetchall()
    res = "\n".join(map(str, my_result[0:]))
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
    url = f'https://od-api.oxforddictionaries.com:443/api/v1/entries/{language}/{word.lower()}'
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    if r.status_code == 404:
        return "Not found"
    else:
        da = r.json()
        try:
            res = da['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['definitions']
            return "".join(res)
        except KeyError:
            res = da['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['crossReferenceMarkers']
            return "".join(res)


def rand_a():
    a = random.randint(0, 9999)
    return a


def rand_b():
    b = random.randint(0, 9999)
    return b


class GameBot(Client):
    answer = ""
    thread_id = ""
    round = 1
    users = {}
    users_count = 1
    joined = 0
    question = ""
    admin_uid = "100005766793253"

    def join_user(self, id, name):
        self.users[self.users_count] = [id, name, 0]
        self.users_count += 1

    def text_twist(self):
        global leng
        global word
        # opening file putting word in words
        with open('words.txt', 'r') as f:
            words = []
            for x in f:
                words.append(x)
        # generating random line in words.txt
        ran = random.randint(0, 28700)
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
        client.send(Message(text=f"ROUND {self.round}\nTEXT TWIST"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        client.send(Message(text=self.question),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)

    def shuffle(self):
        x = [i for i in range(leng)]
        shuffle(x)
        shuff = []
        for y in x:
            shuff.append(word[y])
        shuff = "".join(shuff)
        self.question = f"{shuff}"
        self.repeat()

    def math_game(self):
        game = random.randint(1, 3)
        if game == 1:
            return self.math_add()
        if game == 2:
            return self.math_difference()
        if game == 3:
            return self.text_twist()

    def math_add(self):
        a = rand_a()
        b = rand_b()
        self.answer = f"{a+b}"
        self.question = f"{a} + {b} = ?"
        client.send(Message(text=f"ROUND {self.round}\nMATH"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        client.send(Message(text=self.question),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)

    def math_difference(self):
        a = rand_a()
        b = rand_b()
        self.answer = f"{a-b}"
        self.question = f"{a} - {b} = ?"
        client.send(Message(text=f"ROUND {self.round}\nMATH"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        client.send(Message(text=self.question),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)

    def repeat(self):
        client.send(Message(text=self.question),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)

    def onQprimer(self, **kwargs):
        client.send(Message(text="Gamebot ON!"),
                    thread_id=self.thread_id, thread_type=ThreadType.GROUP)
        self.math_game()

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
                        start_bot()
                if "!clue" in command:
                    if isinstance(self.answer, str):
                        self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                        self.send(Message(text=define(self.answer)),
                                  thread_id=thread_id, thread_type=thread_type)
                if "!shuffle" in command:
                    if isinstance(self.answer, str):
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
                    self.math_game()
                if "!repeat" in command:
                    self.reactToMessage(message_object.uid,
                                        MessageReaction.YES)
                    self.repeat()
                if "!join" in command:
                    join = 0
                    try:
                        name = command.split()
                        for x in self.users:
                            if author_id in self.users[x][0]:
                                join = 1
                        if join == 0:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.join_user(author_id, name[1])
                            self.send(Message(text=f"{name[1]} joined."),
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
                    for x in self.users:
                        self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                        self.send(Message(text=f"{self.users[x][1]} = {self.users[x][2]}"),
                                  thread_id=thread_id, thread_type=thread_type)
                if "!help" in command:
                    self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                    self.send(Message(text="COMMAND LIST:\n\n"
                                                   "!join (name) - join game\n\n"
                                                   "!clue - word definition\n\n"
                                                   "!shuffle - shuffle word\n\n"
                                                   "!score - show scores\n\n"
                                                   "!repeat - repeat question\n\n"
                                                   "!shuffle - shuffle word letters\n\n"),
                                      thread_id=thread_id,
                                      thread_type=thread_type)
                    
                if self.answer in command:
                    self.joined = 0
                    for x in self.users:
                        if author_id in self.users[x]:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.LOVE)
                            self.users[x][2] += 1
                            self.send(Message(text="You got it!"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.joined = 1
                            self.round += 1
                            self.math_game()
                    if self.joined == 0:
                        self.reactToMessage(
                            message_object.uid, MessageReaction.YES)
                        self.send(Message(text="You need to type !join yourname"),
                                  thread_id=thread_id, thread_type=thread_type)


class FacebookBot(Client):
    mirror = 0
    bot = 1  # activate bot
    thread_type = ThreadType.GROUP
    admin_uid = "100005766793253"
    bot_name = "!bot start"
    game = 0

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)
        self.sendMessage("Hello! you added me, dont reply im a robot ",
                         from_id, thread_type=ThreadType.USER)

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
                        if "!quote" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            # response = requests.get(
                            #     "https://talaikis.com/api/quotes/random/")
                            # data = response.json()
                            self.send(
                                Message(text="not available"), thread_id=thread_id, thread_type=thread_type)
                        # bot mirroring
                        if "!mirror on" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(Message(text="Mirror bot on!"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.mirror = 1
                        if "!mirror off" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(Message(text="Mirror bot off!"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.mirror = 0
                        # defining words
                        if "!define" in command:
                            defined = message_object.text.split()
                            try:
                                d = define(defined[1])
                                if d == "Invalid word":
                                    self.reactToMessage(
                                        message_object.uid, MessageReaction.NO)
                                else:
                                    self.reactToMessage(
                                        message_object.uid, MessageReaction.YES)
                                    self.send(
                                        Message(text=d), thread_id=thread_id, thread_type=thread_type)
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
                                self.send(Message(text=f"uid: {user.uid}"), thread_id=thread_id,
                                          thread_type=thread_type)
                                self.send(Message(text=f"name: {user.name}"), thread_id=thread_id,
                                          thread_type=thread_type)
                                self.send(Message(text=f"profile: https://facebook.com/{user.uid}"),
                                          thread_id=thread_id,
                                          thread_type=thread_type)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # calculation functions
                        # addition
                        if "!add" in command:
                            try:
                                addition = message_object.text.split()
                                adding = addition[1:]
                                results = list(map(float, adding))
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text=sum(results)), thread_id=thread_id, thread_type=thread_type)
                            except FBchatFacebookError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except ValueError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # subtraction
                        if "!diff" in command:
                            try:
                                difference = message_object.text.split()
                                diff = float(
                                    difference[1]) - float(difference[2])
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text=diff), thread_id=thread_id, thread_type=thread_type)
                            except FBchatFacebookError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except ValueError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # multiplication
                        if "!multi" in command:
                            try:
                                multiply = message_object.text.split()
                                multi = float(multiply[1]) * float(multiply[2])
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text=multi), thread_id=thread_id, thread_type=thread_type)
                            except FBchatFacebookError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except ValueError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        # division
                        if "!div" in command:
                            try:
                                division = message_object.text.split()
                                div = float(division[1]) / float(division[2])
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text=div), thread_id=thread_id, thread_type=thread_type)
                            except FBchatFacebookError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except ValueError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
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
                            self.send(Message(text="Python bot"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.send(Message(text="Created by: Jam"),
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
                                self.send(Message(text="di po ikaw boss ko"), thread_id=thread_id,
                                          thread_type=thread_type)
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
                        if "!text-to-image" in command:
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
                        # mysql prototype
                        if "!mysql show" in command:
                            tip = "Executing\nSELECT * from table_name;"
                            self.send(
                                Message(text=tip), thread_id=thread_id, thread_type=thread_type)
                            self.send(Message(text="ID, MESSAGE"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            try:
                                self.send(
                                    Message(text=mysql_get()), thread_id=thread_id, thread_type=thread_type)
                            except fbchat.models.FBchatFacebookError:
                                self.send(
                                    Message(text='no data'), thread_id=thread_id, thread_type=thread_type)
                        if "!mysql add" in command:
                            message = command.split()
                            msg = " ".join(message[2:])
                            tip = f"Executing\nINSERT INTO table_name (column1)\nVALUES('{msg}');"
                            self.send(
                                Message(text=tip), thread_id=thread_id, thread_type=thread_type)
                            mysql_add(msg)
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(
                                Message(text=f"'{msg}' added"), thread_id=thread_id, thread_type=thread_type)
                        if "!mysql delete" in command:
                            message = command.split()
                            self.send(Message(text=f"Executing\nDELETE FROM table_name WHERE ID = {message[2]}"),
                                      thread_id=thread_id, thread_type=thread_type)
                            try:
                                mysql_delete(message[2])
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text="deleted"), thread_id=thread_id, thread_type=thread_type)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except mysql.connector.errors.ProgrammingError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                        if "!mysql update" in command:
                            message = command.split()
                            msg = " ".join(message[3:])
                            self.send(Message(
                                text=f"Executing\nUPDATE table_name SET message = '{msg}' WHERE ID={message[2]}"), thread_id=thread_id, thread_type=thread_type)
                            try:
                                mysql_update(message[2], msg)
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.YES)
                                self.send(
                                    Message(text="updated"), thread_id=thread_id, thread_type=thread_type)
                            except IndexError:
                                self.reactToMessage(
                                    message_object.uid, MessageReaction.NO)
                            except mysql.connector.errors.ProgrammingError:
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
                                GameBot.thread_id = thread_id
                                game_bot.listen()

                        # SQL Cheat sheet
                        if "!mysql cheat-sheet" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(Message(text="SELECT * FROM table_name;"), thread_id=thread_id,
                                      thread_type=thread_type)
                            self.send(Message(text="SELECT column_name FROM table_name;"), thread_id=thread_id,
                                      thread_type=thread_type)
                            self.send(Message(text="INSERT INTO table_name (column1, column2, column3, ...)\n"
                                                   "VALUES (value1, value2, value3, ...);"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.send(Message(text="UPDATE table_name\nSET column1 = value1, column2 = value2, ..."
                                                   "\nWHERE condition;"), thread_id=thread_id, thread_type=thread_type)
                            self.send(Message(text="DELETE FROM table_name WHERE condition;"),
                                      thread_id=thread_id, thread_type=thread_type)
                            self.send(Message(text="CREATE DATABASE databasename;"), thread_id=thread_id,
                                      thread_type=thread_type)
                            self.send(Message(text="CREATE TABLE table_name (\ncolumn1 datatype,"
                                                   "column2 datatype,\n"
                                                   "column3 datatype,\n"
                                                   "....\n"
                                                   ");"), thread_id=thread_id, thread_type=thread_type)
                        # show commands
                        if "!commands" in command:
                            self.reactToMessage(
                                message_object.uid, MessageReaction.YES)
                            self.send(Message(text="COMMAND LIST:\n\n"
                                                   "!quotes - random quotes\n\n"
                                                   "!random image - random image\n\n"
                                                   "!mirror on/off - mirror bot\n\n"
                                                   "!define {word} - define a word\n\n"
                                                   "!lyrics artist, song - getting song lyrics\n\n"
                                                   "!title {name} - change chat title\n\n"
                                                   "!nickname {name} - change your nickname\n\n"
                                                   "!search {name} - search a user\n\n"
                                                   "!add n1 n2 n3 nn - adding multiple numbers\n\n"
                                                   "!diff n1 n2 - subtracting numbers\n\n"
                                                   "!multi n1 n2 - multiplying numbers\n\n"
                                                   "!div n1 n2 - dividing numbers\n\n"
                                                   "!mod n1 n2 - modulus division\n\n"
                                                   "!speak {words} - speak bot\n\n"
                                                   "!pause - pause bot\n\n"
                                                   "!start - start bot\n\n"
                                                   "!network 0930 - show network\n\n"
                                                   "!text-to-image\n\n"
                                                   "!mac {mac:address}\n\n"
                                                   "!qr {link}\n\n"
                                                   "!forward {file link}\n\n"
                                                   "!mysql cheat-sheet\n\n"
                                                   "!mysql show - show datas\n\n"
                                                   "!mysql add {message}\n\n"
                                                   "!mysql delete {id}\n\n"
                                                   "!mysql update {id} {message}\n\n"
                                                   "!sms {number} {message}\n\n"
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
            else:
                if author_id != self.uid:
                    self.markAsDelivered(thread_id, message_object.uid)
                    self.markAsRead(thread_id)


def start_bot():
    global fb_bot
    global game_bot
    fb_bot = FacebookBot("pybotjamgph", "jamuel26",
                         session_cookies=session_cookies)
    game_bot = GameBot("pybotjamgph", "jamuel26",
                       session_cookies=session_cookies)
    fb_bot.listen()


def main():
    global client
    global session_cookies
    client = Client("pybotjamgph", "jamuel26")
    session_cookies = client.getSession()
    start_bot()


main()
