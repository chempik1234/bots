import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    login, password = 'dandijar@yandex.ru', 'VKdan!S.143'
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    ids = ['photo' + str(i['owner_id']) + '_' + str(i['id'])
           for i in vk.photos.get(group_id='212025650', album_id='283448220')['items']]
    vk_session = vk_api.VkApi(token='0d89314c6e248981a5ace7e252eca33d650f91fef28ed6025675840cb45f450faea53fe0742ea7f5cb0ea')
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, '212025650')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            users = vk.users.get(user_ids=event.obj.message['from_id'], fields='first_name')[0]
            text = 'Привет, ' + users['first_name'] + '!'
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             attachment=random.choice(ids),
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()