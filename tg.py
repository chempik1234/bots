from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Updater, MessageHandler, Filters
import requests


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


def geocoder(update, context):
    try:
        geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_uri, params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "format": "json",
            "geocode": update.message.text
        })
        ll, spn = find_coords(update.message.text), get_size(update.message.text)
        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={ll},pm2vvm"
        context.bot.send_photo(
            update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
            # Ссылка на static API, по сути, ссылка на картинку.
            # Телеграму можно передать прямо её, не скачивая предварительно карту.
            static_api_request,
            caption="Нашёл:"
        )
    except Exception as err:
        d = {'list index out of range': 'Ничего не найдено'}
        text = err.__str__()
        if text in d.keys():
            text = d[text]
        update.message.reply_text('Ошибка ' + err.__class__.__name__.__str__() + ': ' + text)


def main():
    updater = Updater('5147513805:AAEiG0-XjDlug2pmoPcRPuufLSZBYs8jbIc', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, geocoder))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()