from vk_api import VkApi
from itertools import cycle
from re import search


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

    def get_photo_id(self, identif):
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

    def get_max_photos_id(self, user):
        """ Получаем ID фото с макс лайками, максимум """
        list_photo = self.get_photo_id(user)
        maximum = self._photo_max_like3(list_photo)
        photo_max_id = []
        for ph in list_photo:
            if ph["likes"]["count"] in maximum:
                photo = ph["id"]
                photo_max_id.append(photo)
        return photo_max_id

    def get_user_info(self, user_id):
        """ Получаем ФИО по ID"""
        info = self.method.users.get(user_id=user_id)
        dict_info = info[0]
        first_name = dict_info["first_name"]
        last_name = dict_info["last_name"]
        return f"{first_name} {last_name}"

    def parametrs_for_find(self, user_id, gender, hometown, status, old_min, old_max, sorting=1, has_ph=1):
        """ Поиск по параметрам, стандарт соритровка п поулярности"""
        search = self.method.users.search(
            user_id=user_id,
            sex=gender,
            hometown=hometown,
            status=status,
            age_from=old_min,
            age_to=old_max,
            has_photo=has_ph,
            sort=sorting,
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
        id_set = set([x["id"] for x in summ if x["is_closed"] == False])
        return id_set

    @staticmethod
    def iteration(iter_obj):
        """ Итерируем коллекцию идентификаторов"""
        i, len_iter = cycle(iter_obj), len(iter_obj)
        for one_iter in range(0, len_iter):
            yield next(i)

    @staticmethod
    def immotrtal_favour(iter_obj):
        return cycle(iter_obj)

    @staticmethod
    def atachment_photo(id_owner, list_id):
        """ Формируем строку для attachment в massages.send в виде <type><owner_id>_<media_id>"""
        list_ph = []
        for ph in list_id:
            one = f"photo{id_owner}_{ph},"
            list_ph.append(one)
        return "".join(list_ph)

    def msg_for_send_photo(self, user_id):
        """ Объединеие функций, получаем имя, URL и поле attachment"""
        name = self.get_user_info(user_id)
        list_id_photo = self.get_max_photos_id(user_id)
        photos = self.atachment_photo(user_id, list_id_photo)
        url = "{}{}".format("https://vk.com/id", user_id)
        masg_send = f"{name}\n{url}"
        return masg_send, photos

    @staticmethod
    def if_attribute_none(attr, val: str):
        if attr is None:
            return val
        else:
            return attr

    @staticmethod
    def if_sex(event):
        if event == "мужской":
            return "2"
        elif event == "женский":
            return "1"
        elif event == "любой пол":
            return "0"

    @staticmethod
    def sext_text_from_int(int_sex):
        if int_sex == "2":
            return "мужской"
        elif int_sex == "1":
            return "женский"
        elif int_sex == "0":
            return "любой пол"
        elif int_sex == "Не выбрано":
            return int_sex

    @staticmethod
    def select_old(old_text):
        reg = r"(\d+)(\D*)(\d+)"
        res = search(reg, old_text)
        old_from = int(res.group(1))
        old_to = int(res.group(3))
        age_from = min(old_from, old_to)
        age_to = max(old_to, old_from)
        return age_from, age_to

    @staticmethod
    def select_town(old_text):
        reg = r"(\s+|-)(\w*)"
        res = search(reg, old_text)
        town = res.group(2)
        return town

    @staticmethod
    def selext_status(status):
        reg = r"(\s+)(\d*)"
        res = search(reg, status)
        int_status = int(res.group(2))
        return int_status

    def is_closed(self, user_id):
        info = self.method.users.get(user_id=user_id)
        dict_info = info[0]
        return dict_info["is_closed"]
