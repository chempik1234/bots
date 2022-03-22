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
            vk = vk_session.get_api()
            days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
            text = 'Если ввести сообщение, в котором есть слова «время», «число», «дата», «день», можно получить' \
                   'сегодняшнюю дату, московское время и день недели'
            if any([i in event.obj.message['text'].lower() for i in ['время', 'число', 'дата', 'день']]):
                ts = int(event.obj.message['date'])
                date = datetime.utcfromtimestamp(ts)
                text = 'Дата: ' + date.strftime('%Y-%m-%d') + ' время: ' + date.strftime('%H:%M:%S') + \
                       ' день недели: ' + days[date.weekday()]
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()