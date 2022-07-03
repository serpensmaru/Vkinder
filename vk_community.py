import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def write_msg(user_id, mes):
    """ Для отправки сообщения"""
    vk.method('messages.send', {'user_id': user_id, 'message': mes, 'random_id': 0})


def get_token(name_file):
    """ Получаю TOKEN из txt файла """
    with open(name_file, "r", encoding="utf-8") as f:
        token = f.read()
        return token


if __name__ == "__main__":

    # API-ключ созданный ранее
    TOKEN = get_token("token_community.txt")

    # Авторизуемся как сообщество VK
    vk = vk_api.VkApi(token=TOKEN)

    # Работа с сообщениями
    longpoll = VkLongPoll(vk)

    # Цикл для получения событий(сообщений) адресованных боту (в сообщество)
    for event in longpoll.listen():
        # Если пришло новое сообщение. определяем тип события == сообщение
        if event.type == VkEventType.MESSAGE_NEW:
            # Если оно имеет метку для меня (то есть бота)
            if event.to_me:
                message = event.text.lower()  # получаем текст сообещния и приводим к нижнему регистру
                id_user = event.user_id  # получаем user_id, того кто пишет боту
                print(id_user)
                print(message)
                write_msg(id_user, "Привет я бот для знакомств")
                write_msg(id_user, "Скоро тут будет инструкция как мной пользоваться")
