import requests


class Define(object):
    def __init__(self, word):
        self.word = word

    def define(self, word):
        app_id = '0d6c4d8a'
        app_key = '642dd9bb994eb786bea9ac1453dedb07'
        language = 'en'
        url = f'https://od-api.oxforddictionaries.com:443/api/v2/entries/{language}/{word.lower()}'
        r = requests.get(
            url, headers={'app_id': app_id, 'app_key': app_key})

        if r.status_code == 404:
            return "No data"
        else:
            da = r.json()
            try:
                res = da['results'][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['definitions']
                return "".join(res)
            except KeyError:
                return "No data"

    def suggestquery(self, query):
        headers = {'Content-Type': 'application/json'}
        r = requests.get(
            f"http://suggestqueries.google.com/complete/search?output=toolbar&client=firefox&hl=en&q={query}", headers=headers)
        r = r.json()
        return r[1][0]

    def get(self):
        defined = self.word.split()
        try:
            if defined[2]:
                return "Multiple word is invalid."
        except IndexError:
            try:
                d = self.define(defined[1])
                if d == "Invalid word":
                    return "Word not found."
                else:
                    if d != "No data":
                        return d
                    else:
                        res = self.suggestquery(defined[1])
                        if defined[1] != res:
                            return f"did you mean...\n{res}"
                        else:
                            pass
            except Exception as e:
                return e
