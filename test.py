import requests

word = "!unplag Hello there qweqwe"
w = word.split()
w = " ".join(w[1:])
print(w)
# url = "https://plagiarism-remover.p.rapidapi.com/api/rewrite"

# payload = "{  \"sourceText\": \"" + word[1:] + "\"}"
# headers = {
# 'x-rapidapi-host': "plagiarism-remover.p.rapidapi.com",
# 'x-rapidapi-key': "fKF1gF6A8Hmshio5bYJ0MWDnKgRXp1HFSX7jsnmPs7rhcgCPmb",
# 'content-type': "application/json",
# 'accept': "application/json"
# }

# response = requests.request("POST", url, data=payload, headers=headers)
# res = response.json()
# print(res["NewText"])
