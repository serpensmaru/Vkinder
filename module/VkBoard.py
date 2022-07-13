from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType


def get_token(name_file):
    """ Получения токена из файла"""
    """ Получаю TOKEN из txt файла """
    with open(name_file, "r", encoding="utf-8") as f:
        token = f.read()
        return token


class Keyboard:
    def __init__(self, one_time: bool = False, inline: bool = False):
        self.one_time = one_time
        self.inline = inline
        self.kb = self._kb_obj()

    def _kb_obj(self):
        """ Получаем объект клавиатуры с настройками"""
        return VkKeyboard(one_time=self.one_time, inline=self.inline)

    def pattern_kb(self, *args):
        """ Создание кнопок из списка/кортежа, если попадает на False/0, то создаем новую строку кнопок"""
        for one in args:
            if one == 0:
                self.kb.add_line()
            else:
                self.kb.add_button(label=one, color=VkKeyboardColor.NEGATIVE)
        return self.kb.get_keyboard()

class VkBot:
    def __init__(self, tokenCommunity):
        self.token = tokenCommunity
        self.session = self._session()
        self.method = self._method()

    def _session(self):
        """ Базовый класс"""
        ses = VkApi(token=self.token)
        return ses

    def _method(self):
        """ Для методов VK API"""
        return self.session.get_api()

    def evention(self):
        """ Объект слежения за событиями"""
        return VkLongPoll(self.session)

    def message_type(self):
        """ Тип сообытия сообщения"""
        return VkEventType.MESSAGE_NEW



class VkBoard(VkBot, Keyboard):
    """ Класс объедняющий VkBot, Keyboard c реализацией доп методов"""
    def __init__(self, tokenCommunity, one_time: bool = False, inline: bool = False):
        super().__init__(tokenCommunity)
        self.one_time = one_time
        self.inline = inline
        self.kb = self._kb_obj()
        self.session = self._session()
        self.method = self._method()

    def vk_send_board(self, user_id):
        """ Отправка клавиатуры пользователю"""
        self.method.messages.send(random_id=0, keyboard=self.kb.get_keyboard(), user_id=user_id, peer_id=user_id, message=".")

    def check_board(self, keyboard, user_id):
        """ Отправка клавиатуры пользователю с проверкой на нет ли у него этой клавы"""
        if self.kb.get_keyboard() != keyboard:
            self.vk_send_board(user_id)
        return keyboard

    def send_msg(self, messenge, user_id):
        """ Отправка сообщений пользователю"""
        self.method.messages.send(
                random_id=0,
                user_id=user_id,
                peer_id=user_id,
                message=messenge
            )
