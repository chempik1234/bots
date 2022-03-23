import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime


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
            message = event.obj.message['text']
            vk = vk_session.get_api()
            days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
            text = 'Введите дату в формате YYYY-MM-DD, и я скажу какой тогда был день'
            if len(message) == 10 and message[0: 4].isdigit() and message[5: 7].isdigit() and message[8:].isdigit() \
                    and message[4] == message[7] == '-':
                try:
                    date = datetime.strptime(message, '%Y-%m-%d').date()
                    text = days[date.weekday()]
                except Exception:
                    text = 'Неправильная дата'
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()