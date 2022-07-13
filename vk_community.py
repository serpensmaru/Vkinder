from module.VkBoard import VkBoard, get_token
from module.VkOperator import VkOperator
from Vk_api import Vkontacte
# API-ключ созданный ранее
TOKEN_commun = get_token("token_community.txt")
# Инициация класса бота и клавиатуры
session = VkBoard(TOKEN_commun)
# vk для обращений к методам API, longpoll для контроля событий
longpoll = session.evention()
# Инициация класса клавиатур
kb = session.kb
# Создаем кнопки 5 штук и 1 строку
list_butt = ("Помощь", "Поиск", "Избранное", 0, "Сохранить", "Свайп")
keyboard = session.pattern_kb(*list_butt)
type_message = session.message_type()
# Cоздание класса Operator для поиска
TOKEN_personal = get_token("token_pers.txt")
vk_pj = Vkontacte(TOKEN_personal)


# Цикл для получения событий(сообщений) адресованных боту (в сообщество)
for event in longpoll.listen():
    if event.type == type_message:
        # Если оно имеет метку для меня (то есть бота)
        if event.to_me:
            # получаем user_id, того кто пишет боту
            id_user = event.user_id
            # Проверяем клавиатуру user'a, если уже отправлена, то не отправляем
            old_kb = session.check_board(keyboard, user_id=id_user)
            print(event.text)
            if event.text == "Помощь":
                text_find = "*\tПоиск - нажмите поиск и введите предложенные критерии поиска (пол, возраст, город)\n"
                text_save = "*\tСохранить - после поиска вы можете сохранить понравившегося человека\n"
                text_favour = " *\tИзбранное - можете посмотреть кого вы сохранили\n"
                text_swipe = "*\tСвайп - листать найденныъ людей после поиска\n"
                help_text = f"{text_find}{text_save}{text_favour}{text_swipe}"
                session.send_msg(help_text, id_user)
            elif event.text == "Поиск":
                # sex = "2"
                # age_from = "18"
                # age_to = "23"
                hometown = "тюмень"
                # Поиск по критериям, нужно сделать ввод критериев от пользователя, а также сделать итератор/генератор
                q = vk_pj.sum_find_id(user_id=id_user, metropolis=hometown)
                print(q)
                session.send_msg("Поведение поиска еще не прописанно", id_user)
            elif event.text == "Избранное":
                session.send_msg("Поведение избранного еще не прописанно", id_user)
            elif event.text == "Сохранить":
                session.send_msg("Поведение сохранить еще не прописанно", id_user)
            elif event.text == "Свайп":
                session.send_msg("Поведение свайпа еще не прописанно", id_user)
