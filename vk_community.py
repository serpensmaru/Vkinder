from module.VkBoard import VkBoard, get_token
from module.VkOperator import VkOperator
from module.PostgressVK import engine_driv, get_favour_id, clear_sewipe, del_favour, Base_model, add_swipe, add_favour, bool_swipe_id, User, Swipe, if_not_add_user_id
# Создание базы данных
engine = engine_driv(user_db_name="postgres", password="123456", db_name="vkinder", log=False)
#  Создание таблиц, если их нет
Base_model.metadata.create_all(engine)
# API-ключ созданный ранее
TOKEN_commun = get_token("token_community.txt")
# Инициация класса бота и клавиатуры
session = VkBoard(TOKEN_commun)
# vk для обращений к методам API, longpoll для контроля событий
longpoll = session.evention()
# Инициация класса клавиатур
kb = session.kb
# Создаем кнопки 5 штук и 1 строку
list_butt = ("Помощь", "Поиск", "Избранное", 0, "Очистить", "Del из избран.", "Cлед. избран.", 0, "Сохранить", "Критерии", "Свайп")
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
iter_id_favour = None
id_favour = None
for event in longpoll.listen():
    if event.type == type_message:
        # Если оно имеет метку для меня (то есть бота)
        if event.to_me:
            # получаем user_id, того кто пишет боту   "Здравствуй, я бот знакомств, используй клавиатуру, для вызова справки, чтобы узнать как мной пользоваться"
            id_user = event.user_id
            # Проверяем клавиатуру user'a, если уже отправлена, то не отправляем
            session.vk_send_board(id_user)
            # Добавляет пользователя в БД, если его там нет
            if_not_add_user_id(id_user, engine, User)
            if event.text == "Помощь":
                text_find = "*\tПоиск - нажмите поиск и введите предложенные критерии поиска (пол, возраст, город, статус)\n"
                text_save = "*\tСохранить - после поиска вы можете сохранить понравившегося человека в избранное\n"
                text_criteria = "*\tКритерии - показть выбранные критерии поиска\n"
                text_favour = " *\tИзбранное - нажмите чтобы посмотреть избранное\n"
                text_favour_s = " *\tСлед. избран. - нажмите чтобы листать избранное, нажимается после 'Избранное'\n"
                text_swipe = "*\tСвайп - листать найденныъ людей после поиска\n"
                text_del = "*\tDel из избран. - когда листаете избранное, можете нажать чтобы удалить текущего человека из избранного\n"
                text_сlear = "*\tОчистить - люди которых вы свайпнули больше вам не попадутся в поиске, чтобы вернуть их в поиск нажмите очистить\n"
                help_text = f"{text_find}{text_сlear}{text_save}{text_favour}{text_favour_s}{text_del}{text_criteria}{text_swipe}"
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

            elif event.text == "Свайп":
                # Проверка Х, если был произведен поиск то Х=1, елси нет то 0
                # В идале было просто написать через искулючения, но я еще не умею этого
                if x == 1:
                    id_actual = next(iter_id_find)
                    bool_val = True
                    while bool_val:
                        id_actual = next(iter_id_find)
                        bool_val = bool_swipe_id(id_actual, id_user, engine, Swipe)
                        if bool_val:
                            break
                    msg, photos = srch.msg_for_send_photo(id_actual)
                    # Отправялем пользователю имя и фотки
                    session.send_msg_photo(msg, id_user, photos)
                    add_swipe(id_user=id_user, id_swipe=id_actual, engine=engine)
                else:
                    session.send_msg(f"Сначала нажмите поиск и следуйте инструкции", id_user)

            elif event.text == "Очистить":
                clear_sewipe(engine, id_user)

            elif event.text == "Критерии":
                sex = srch.if_attribute_none(sex, "Не выбрано")
                sex_text = srch.sext_text_from_int(sex)
                age_from = srch.if_attribute_none(age_from, "X")
                age_to = srch.if_attribute_none(age_to, "X")
                status = srch.if_attribute_none(status, "Не выбрано")
                session.send_msg(f"Пол: {sex_text}\nВозраст от {age_from} до {age_to}\nГород: {hometown}\nСтатус: {status}", id_user)

            elif event.text == "Сохранить":
                if x == 1:
                    add_favour(id_user, id_actual, engine)
                    session.send_msg("Сохраненно", id_user)
                else:
                    session.send_msg("Начните поиск и нажмите свайп", id_user)

            elif event.text == "Избранное":
                list_favout = get_favour_id(engine, id_user)
                iter_id_favour = srch.immotrtal_favour(list_favout)
                session.send_msg("Нажмите след. избран.", id_user)

            elif event.text == "Cлед. избран.":
                if iter_id_favour != None:
                    id_favour = next(iter_id_favour)
                    msg, photos = srch.msg_for_send_photo(id_favour)
                    session.send_msg_photo(msg, id_user, photos)
                else:
                    session.send_msg("Сначала нажмите избранное", id_user)

            elif event.text == "Del из избран.":
                if id_favour is not None:
                    del_favour(engine, id_user, id_favour)
