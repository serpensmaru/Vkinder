from module.VkOperator import VkOperator
from module.VkBoard import get_token, VkBoard
from pprint import pprint


if __name__ == "__main__":
    TOKEN = get_token("token_pers.txt")
    session = VkOperator(TOKEN)
    # name = session.get_user_info(173442120)
    # url_photo = session.get_max_photos(173442120)
    # pprint(name)
    # pprint(url_photo)
    user_id = 173442120
    sex = "2"
    age_from = "18"
    age_to = "23"
    hometown = "тюмень"

    a = session.sum_find_id(
        user_id=user_id, gender=sex,
        hometown=hometown, status="1",
        old_min=age_from, old_max=age_to)
    print(len(a))
    print(a)
    # g = session.get_photo_id(173442120)
    # pprint(g)

    q = session.get_max_photos_id(173442120)
    print(q)
    pg = f"photo173442120_{q[0]}"
    print(pg)
    # token = get_token("token_pers.txt")
    # vk = VkBoard(token)
    vk.send_msg_photo("qwe", 173442120, photo173442120_456240882)