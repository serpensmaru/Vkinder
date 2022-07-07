import vk_api
from token_class import Token


class Vkontacte:

    def call_token(self, token_file:str):
        """ Получение токена.
        Метод класса вызывается с именем файла формата txt, в котором записан наш персональный токен """
        token = Token()

        return token.get_token(token_file)

    def start_vk_api_session(self, token_file:str):
        """ Запуск сессии API VK """
        self.token = self.call_token(token_file)
        self.vk_session = vk_api.VkApi(token=self.token)
        self.session_api = self.vk_session.get_api()

    def search_users(self, sex: int, city: str, status: int, from_age: int, to_age: int):
        """ Создание генератора ID.
        Первоначально отбираются 100 профилей, но в генератор попадают только открытые.
        Передаются параметры sex, city, status, from_age, to_age """
        self.response_json = self.session_api.users.search(sort='0', fields='is_closed', count='100', hometown=city, status=str(status), country='1', has_photo='1', sex=str(sex), age_from=str(from_age), age_to=str(to_age))
        self.id_gen = (item['id'] for item in self.response_json['items'] if item['is_closed'] == False)

        return self.id_gen

    def get_photo(self, id):
        """ Получение URL-ов трёх популярных фотографий пользователя в формате,
        удобном для последующей подставновки в метод messages.send(attachment=photo_id) бота"""
        self.photos_dict = self.session_api.photos.get(owner_id=str(id), album_id='profile', extended=1)
        self.three_best_photos = sorted(self.photos_dict['items'], key=lambda item: item['likes']['count'])[-3:]
        self.three_best_photos_list = []
        for photo in self.three_best_photos:
            self.three_best_photos_list.append(f'photo{photo["owner_id"]}_{photo["id"]}')

        return self.three_best_photos_list


if __name__ == '__main__':
    # Создание экземпляра класса Vkontacte
    vk = Vkontacte()

    # Запуск сессии VK API
    vk.start_vk_api_session('token_app.txt')

    # Получение списков из трёх фотографий тех пользоватей, которые удовлетворяют критериям поиска
    for id in vk.search_users(0, 'Москва', 1, 20, 30):
        print(vk.get_photo(id))
