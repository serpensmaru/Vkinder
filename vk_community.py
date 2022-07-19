from module.VkBoard import VkBoard, get_token
from module.VkOperator import VkOperator
# API-ключ созданный ранее
TOKEN_commun = get_token("token_community.txt")
# Инициация класса бота и клавиатуры
session = VkBoard(TOKEN_commun)
# vk для обращений к методам API, longpoll для контроля событий
longpoll = session.evention()
# Инициация класса клавиатур
kb = session.kb
# Создаем кнопки 5 штук и 1 строку
list_butt = ("Помощь", "Поиск", "Избранное", 0, "Сохранить", "Критерии", "Свайп")
keyboard = session.pattern_kb(*list_butt)
type_message = session.message_type()
# Создаем клаас дял поиска по критериям
TOKEN_pers = get_token("token_pers.txt")
srch = VkOperator(TOKEN_pers)
x = 0
# Цикл для получения событий(сообщений) адресованных боту (в сообщество)
sex = None
age_from = None
age_to = None
status = None
hometown = None
for event in longpoll.listen():
    if event.type == type_message:
        # Если оно имеет метку для меня (то есть бота)
        if event.to_me:
            # получаем user_id, того кто пишет боту   "Здравствуй, я бот знакомств, используй клавиатуру, для вызова справки, чтобы узнать как мной пользоваться"
            id_user = event.user_id
            # Проверяем клавиатуру user'a, если уже отправлена, то не отправляем
            session.vk_send_board(id_user)
            if event.text == "Помощь":
                text_find = "*\tПоиск - нажмите поиск и введите предложенные критерии поиска (пол, возраст, город, статус)\n"
                text_save = "*\tСохранить - после поиска вы можете сохранить понравившегося человека\n"
                text_criteria = "*\tКритерии - показть выбранные критерии поиска\n"
                text_favour = " *\tИзбранное - можете посмотреть кого вы сохранили\n"
                text_swipe = "*\tСвайп - листать найденныъ людей после поиска\n"
                help_text = f"{text_find}{text_save}{text_favour}{text_criteria}{text_swipe}"
                session.send_msg(help_text, id_user)
            elif event.text == "Поиск":
                session.send_msg("Выберите, введите пол: \n*любой\n*женский\n*мужской\nОбразец ввода:\nженский", id_user)
            elif event.text.lower() in ("женский", "мужской", "любой пол"):
                sex = srch.if_sex(event.text.lower())
                session.send_msg("Пол успешно выбран, теперь введите возрастной диапазон\nОбразец: \nвозраст от 18 до 24", id_user)
            elif "возраст от" in event.text.lower():
                age_from, age_to = srch.select_old(event.text.lower())
                session.send_msg("Введите название города\nОбразец:\nгород Тюмень", id_user)
            elif "город" in event.text.lower():
                hometown = srch.select_town(event.text.lower()).capitalize()
                print(hometown)
                session.send_msg("Город успешно выбран, введите статус:\n1-не женат(не замужем)\n2-встречаются\n3-помолвен(а)\n4-женат(замужем)\n5-все сложно\n6-в активном поиске\n7-влюблен(а)\n8-в граждансокм браке\nОбразец:\nстатус цифра статуса", id_user)
            elif "статус" in event.text.lower():
                status = srch.selext_status(event.text.lower())
                session.send_msg(f"Ожидайте завершения поиска", id_user)
                # Поиск по критериям, нужно сделать ввод критериев от пользователя, а также сделать итератор/генератор
                tuple_id_find = srch.sum_find_id(id_user, sex, hometown, status, age_from, age_to)
                iter_id_find = srch.iteration(tuple_id_find)
                type_iter = type(iter_id_find)
                session.send_msg("Поск завершен, нажмите свайп", id_user)
                x = 1
            elif event.text == "Критерии":
                sex = srch.if_attribute_none(sex, "Не выбрано")
                sex_text = srch.sext_text_from_int(sex)
                age_from = srch.if_attribute_none(age_from, "X")
                age_to = srch.if_attribute_none(age_to, "X")
                status = srch.if_attribute_none(status, "Не выбрано")
                session.send_msg(f"Пол: {sex_text}\nВозраст от {age_from} до {age_to}\nГород: {hometown}\nСтатус: {status}", id_user)
            elif event.text == "Избранное":
                session.send_msg("Поведение избранного еще не прописанно", id_user)
            elif event.text == "Сохранить":
                session.send_msg("Поведение сохранить еще не прописанно", id_user)
            elif event.text == "Свайп":
                # Проверка Х, если был произведен поиск то Х=1, елси нет то 0
                # В идале было просто написать через искулючения, но я еще не умею этого
                if x == 1:
                    id_actual = next(iter_id_find)
                    msg, photos = srch.msg_for_send_photo(id_actual)
                    # Отправялем пользователю имя и фотки
                    session.send_msg_photo(msg, id_user, photos)
                else:
                    session.send_msg(f"Поведение свайпа еще не прописанно", id_user)
