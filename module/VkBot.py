import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def write_msg(vk: vk_api.vk_api.VkApi, user_id: int, message: str):
    """ Отправка сообщения, потом переделаю"""
    """ Для отправки сообщения"""
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


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
        """ Настройка отображения клавиатуры"""
        return VkKeyboard(one_time=self.one_time, inline=self.inline)

    def pattern_kb(self, *args):
        """ Создание кнопок из списка, если попадает на False, то создаем новую строку кнопок"""
        for one in args:
            if one == 0:
                self.kb.add_line()
            else:
                self.kb.add_button(label=one, color=VkKeyboardColor.NEGATIVE)
        return self.kb.get_keyboard()


class VkBot:
    def __init__(self, token):
        self.token = token
        self.session = self._session()
        self.method = self._method()

    def _session(self):
        """ Базовый класс"""
        ses = vk_api.VkApi(token=self.token)
        return ses

    def _method(self):
        """ Для методов VK API"""
        return self.session.get_api()

    def evention(self):
        """ Объект слежения за событиями"""
        return VkLongPoll(self.session)


class VkBoard(VkBot, Keyboard):
    def __init__(self, token, one_time: bool = False, inline: bool = False):
        super().__init__(token)
        self.one_time = one_time
        self.inline = inline
        self.kb = self._kb_obj()
        self.session = self._session()
        self.method = self._method()

    def vk_send_board(self, user_id):
        self.method.messages.send(random_id=0, keyboard=self.kb.get_keyboard(), user_id=user_id, peer_id=user_id, message=".")

    def check_board(self, old_kb, user_id):
        new_kb = self.kb.get_keyboard()
        if self.kb.get_keyboard() != old_kb:
            self.vk_send_board(user_id)
            old_kb = new_kb
        return old_kb

    def send_msg(self, messenge, user_id):
        self.method.messages.send(
                random_id=0,
                user_id=user_id,
                peer_id=user_id,
                message=messenge
            )
