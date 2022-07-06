from vk_api.longpoll import VkEventType
from module.VkBot import VkBoard, get_token

# API-ключ созданный ранее
TOKEN = get_token("token_community.txt")
# Инициация класса бота и клавиатуры
session = VkBoard(TOKEN)
# vk для обращений к методам API, longpoll для контроля событий
vk = session.method
longpoll = session.evention()
# Инициация класса клавиатур
kb = session.kb
# Создаем кнопки 5 штук и 1 строку
list_butt = ["Помощь", "Поиск", "Избранное", False, "Сохранить", "Свайп"]
keyboard = session.pattern_kb(*list_butt)
# Цикл для получения событий(сообщений) адресованных боту (в сообщество)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня (то есть бота)
        if event.to_me:
            # получаем user_id, того кто пишет боту
            id_user = event.user_id
            # Проверяем клавиатуру user'a, если уже отправлена, то не отправляем
            old_kb = session.check_board(keyboard, user_id=id_user)
            print(event.text)
            if event.text == "Помощь":
                session.send_msg("Поведение помощи еще не прописанно", id_user)
            elif event.text == "Поиск":
                session.send_msg("Поведение поиска еще не прописанно", id_user)
            elif event.text == "Избранное":
                session.send_msg("Поведение избранного еще не прописанно", id_user)
            elif event.text == "Сохранить":
                session.send_msg("Поведение сохранить еще не прописанно", id_user)
            elif event.text == "Свайп":
                session.send_msg("Поведение свайпа еще не прописанно", id_user)
