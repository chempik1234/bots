import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
import random, requests
import os
stages = {}


def find_coords(geocode):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    if not response or not json_response["response"]["GeoObjectCollection"]["featureMember"]:
        return False
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coordinates = toponym["Point"]["pos"]
    return toponym_coordinates.replace(' ', ',')


def get_size(address):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {"apikey": api_key, "lang": "ru_RU", "text": address}
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    organization = json_response["features"][0]["properties"]
    toponym_lc, toponym_uc = organization["boundedBy"]
    toponym_size = max(abs(toponym_lc[0] - toponym_uc[0]),
                       abs(toponym_lc[1] - toponym_uc[1]))
    return str(toponym_size) + ',' + str(toponym_size)


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    vk_session = vk_api.VkApi(
        token='0d89314c6e248981a5ace7e252eca33d650f91fef28ed6025675840cb45f450faea53fe0742ea7f5cb0ea')

    longpoll = VkBotLongPoll(vk_session, '212025650')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            from_id = event.obj.message['from_id']
            if from_id not in stages.keys():
                stages[from_id] = [0, None]
            stage = stages[from_id][0]
            message = event.obj.message['text']
            vk = vk_session.get_api()
            if stage == 0:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Напишите какое-нибудь место',
                                 random_id=random.randint(0, 2 ** 64))
                stages[from_id][0] += 1
            elif stage == 1:
                if not stages[from_id][1]:
                    stages[from_id][1] = message
                    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
                    keyboard.add_button("Спутник", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
                    keyboard.add_button("Схема", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
                    keyboard.add_button("Гибрид", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Выберите тип карты',
                                     keyboard=keyboard.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    stages[from_id][0] += 1
            elif stages[from_id][0] == 2:
                if message == 'Спутник' or message == 'Схема' or message == 'Гибрид':
                    stages[from_id][0] += 1
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Надо написать Спутник, Схема или Гибрид. Вы написали ' + message,
                                     random_id=random.randint(0, 2 ** 64))
            if stages[from_id][0] == 3:
                stages[from_id][0] = 2.5
                address = stages[from_id][1]
                if not find_coords(address):
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Не найдены результаты. Всё заново',
                                     random_id=random.randint(0, 2 ** 64))
                    stages[from_id][0] = 1
                types = {'Спутник': 'sat', 'Схема': 'map', 'Гибрид': 'sat,skl'}
                map_params = {
                    "ll": find_coords(address),
                    "spn": get_size(address),
                    "l": types[message]
                }
                map_api_server = "http://static-maps.yandex.ru/1.x/"
                response = requests.get(map_api_server, params=map_params)
                print(response.url)
                path = os.path.join('static\\img\\maps', f'map{from_id}.jpg')
                if os.path.isfile(path):
                    os.remove(path)
                with open(path, "wb") as file:
                    file.write(response.content)
                login, password = 'dandijar@yandex.ru', 'VKdan!S.143'
                vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
                try:
                    vk_session.auth(token_only=True)
                except vk_api.AuthError as error_msg:
                    print(error_msg)
                    return
                upload = vk_api.VkUpload(vk_session)
                photo = upload.photo([path], '283448220', group_id='212025650')
                vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
                vk_session = vk_api.VkApi(
                    token='0d89314c6e248981a5ace7e252eca33d650f91fef28ed6025675840cb45f450faea53fe0742ea7f5cb0ea')
                vk = vk_session.get_api()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'Это {address}. Что ещё хотите увидеть?',
                                 attachment=vk_photo_id,
                                 random_id=random.randint(0, 2 ** 64))
                stages[from_id][1] = None
                stages[from_id][0] = 1


if __name__ == '__main__':
    main()