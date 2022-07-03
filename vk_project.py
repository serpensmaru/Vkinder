import requests
from pprint import pprint

def get_token(name_file):
    """ Получаю TOKEN из txt файла """
    with open(name_file, "r", encoding="utf-8") as f:
        token = f.read()
        return token

class Vkontacte:
    def __init__(self, token: str):
        self.token = token
        self.V = "5.131"
        self.URL = "https://api.vk.com/method/"

    def photo(self, id: str): # Взял этот метод просто для проверки работоспособности запросов от имни приложения
        """Все фотографии с профиля и информация о них"""
        params = {
            "owner_id": id,
            "extended": '1',
            "album_id":'profile',
            "access_token": self.token,
            "v": self.V
            }
        url = f"{self.URL}photos.get"
        res = requests.get(url, params=params)
        return res.json()

if __name__ == "__main__":
    TOKEN = get_token("token_app.txt")
    vk = Vkontacte(TOKEN)
    durov = vk.photo(1) # ID=1 это павел дуров
    pprint(durov)