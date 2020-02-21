import requests


class Meme(object):
    def __init__(self, mid, msg1, msg2):
        self.mid = mid
        self.msg1 = msg1
        self.msg2 = msg2

    def make(self):
        try:
            r = requests.post("https://api.imgflip.com/caption_image", data={
                'template_id': self.mid, 'username': 'jamg', 'password': 'jamuel26', 'text0': self.msg1, 'text1': self.msg2})
            r = r.json()
            return r["data"]["url"]

        except Exception as e:
            return "Invalid id."
