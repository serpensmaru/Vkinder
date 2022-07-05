import requests
from pprint import pprint

def get_token(name_file):
    """ Получаю TOKEN из txt файла """
    with open(name_file, "r", encoding="utf-8") as f:
        token = f.readline()
        return token

class Vkontacte:
    def __init__(self, token: str):
        self.token = token
        self.V = "5.131"
        self.URL = "https://api.vk.com/method/"

    def find(self):
        params = {
            "count": '1000',
            "sort": "0",
            "user_id": "173442120",  # это мой ID, сюда надо будет вставлять ID user'а который ищет
            "offset": "0",
            "fields": "bdate,city,relation,can_write_private_message,can_see_all_posts",
            "access_token": self.token,
            "v": self.V,
            "has_photo": "1",
            "hometown": "тюмень",   # строковое значение, регистр не важен
            "sex": "2",             # 1-жен, 0-муж
            "status": "1",          # 1-8 см. справку
            "age_from": "18",       # от
            "age_to": "23",         # до old
            }
        url = f"{self.URL}users.search"
        res = requests.get(url, params=params)
        return res.json()


if __name__ == "__main__":
    TOKEN = get_token("token_app.txt")

    vk = Vkontacte(TOKEN)
    w = vk.find()
    r = w["response"]["items"]
    pprint(r)