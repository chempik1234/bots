from flask import Flask, render_template
import vk_api
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
levels = {}


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


@app.route('/vk_stat/<int:group_id>')
def index(group_id):
    login, password = 'dandijar@yandex.ru', 'VKdan!S.143'
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    info = vk.stats.get(group_id=group_id, fields='reach')
    periods = [i for i in info[0: min(len(info), 10)] if i['visitors']['visitors'] > 0]
    user_ages, user_activities, user_cities = {'12-18': 0, '18-21': 0, '21-24': 0, '24-27': 0,
                                               '27-30': 0, '30-35': 0, '35-45': 0, '45-100': 0},\
                                              {'likes': 0, 'comments': 0, 'subscribed': 0}, []
    for n in range(len(periods)):
        i = periods[n]
        visitors = i['visitors']
        ages = visitors['age']
        if n == 0:
            for j in ages:
                if j['value'] in user_ages.keys():
                    user_ages[j['value']] += j['count']
                else:
                    user_ages[j['value']] = j['count']
            cities = visitors['cities']
            for j in cities:
                if not j['name'] in user_cities:
                    user_cities.append(j['name'])
        if i.get('activity'):
            activity = i['activity']
            if activity.get('likes'):
                user_activities['likes'] += activity['likes']
            if activity.get('comments'):
                user_activities['comments'] += activity['comments']
            if activity.get('subscribed'):
                user_activities['subscribed'] += activity['subscribed']
    return render_template('vk_stat.html', dicts={'Activities': user_activities, 'Ages': user_ages},
                           cities=user_cities, td={'Activities': ('#8E44AD', '#BB8FCE'),
                                                   'Ages': ('#45B39D', '#73C6B6'),
                                                   'Cities': '#F5B7B1'})


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')