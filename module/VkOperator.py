from vk_api import VkApi
from module.VkBoard import get_token
from pprint import pprint


class VkOperator:
    def __init__(self, token_personal):
        self.token = token_personal
        self.session = self._session()
        self.method = self._method()

    def _session(self):
        """ Базовый класс"""
        ses = VkApi(token=self.token)
        return ses

    def _method(self):
        """ Для методов VK API"""
        return self.session.get_api()

    def _get_photo_id(self, identif):
        """ Получаем фото профиля по ID"""
        all_photo = self.method.photos.get(
            user_id=identif,
            album_id="profile",
            extended=1
        )
        x = all_photo["items"]
        return x

    @staticmethod
    def _photo_max_like3(list_dict_photo, count_max=3):
        """ Получаем кортеж с максимальными (3 шт) лайками фото порфиля"""
        list_like = [x["likes"]["count"] for x in list_dict_photo]
        list_like.sort(reverse=True)
        return list_like[:count_max]

    def get_max_photos(self, user):
        """ Получаем URL фото с макс лайками, максимум """
        list_photo = self._get_photo_id(user)
        maximum = self._photo_max_like3(list_photo)
        photo_max = []
        for ph in list_photo:
            if ph["likes"]["count"] in maximum:
                photo = ph["sizes"][-1]["url"]
                photo_max.append(photo)
        return photo_max

    def get_user_info(self, user_id):
        """ Получаем ФИО по ID"""
        info = self.method.users.get(user_id=user_id)
        dict_info = info[0]
        first_name = dict_info["first_name"]
        last_name = dict_info["last_name"]
        return f"{first_name} {last_name}"

    def parametrs_for_find(self, user_id, gender, hometown, status, old_min, old_max, sorting=1):
        """ Поиск по параметрам, стандарт соритровка п поулярности"""
        search = self.method.users.search(
            user_id=user_id,
            sex=gender,
            hometown=hometown,
            status=status,
            age_from=old_min,
            age_to=old_max,
            has_photo=sorting,
            sort="0",
            count="1000",
            offset="0",
            fields="bdate,city,relation,can_write_private_message,can_see_all_posts"
        )
        return search["items"]

    def sum_find_id(self, user_id, gender, hometown, status, old_min, old_max):
        """ Возвращает объединение множеств поиска с разными сортировками чтобы было больше людей"""
        no_sort = self.parametrs_for_find(user_id, gender, hometown, status, old_min, old_max, sorting=1)
        sorting = self.parametrs_for_find(user_id, gender, hometown, status, old_min, old_max, sorting=0)
        summ = [*no_sort, *sorting]
        id_set = set([x["id"] for x in summ])
        return id_set


