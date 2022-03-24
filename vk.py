import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random, wikipedia


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    cyrillic = 'йцукенгшщзхъфывапролджэячсмитьбюё'
    vk_session = vk_api.VkApi(token='0d89314c6e248981a5ace7e252eca33d650f91fef28ed'
                                    '6025675840cb45f450faea53fe0742ea7f5cb0ea')
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, '212025650')

    for event in longpoll.listen():
        if event.type == VkBotEventType.GROUP_JOIN:
            print(event)
            user = vk.users.get(user_ids=event.obj.message['from_id'], fields='first_name')[0]
            text = 'Привет, ' + user['first_name'] + '! Задавайте вопросы.'
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             random_id=random.randint(0, 2 ** 64))
        elif event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            message = event.obj.message['text']
            if any(i in cyrillic for i in message.lower()):
                wikipedia.set_lang('ru')
            else:
                wikipedia.set_lang('en')
            response = wikipedia.search(message)
            text = "k"
            if response:
                page = wikipedia.page(response[0])
                text = page.content
            else:
                text = "Википедия не ответила"
            cur = ""
            for i in range(len(text)):
                if i == 4095:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=cur,
                                     random_id=random.randint(0, 2 ** 64))
                    cur = ""
                else:
                    cur += text[i]


if __name__ == '__main__':
    main()