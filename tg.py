from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests


def translator(update, context):
    reply_keyboard = [['en|ru', 'ru|en']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    try:
        if not context.user_data.get('langpair'):
            context.user_data['langpair'] = "ru|en"
        if update.message.text == 'en|ru':
            context.user_data['langpair'] = "en|ru"
            return
        elif update.message.text == 'ru|en':
            context.user_data['langpair'] = "ru|en"
            return
        lang = context.user_data['langpair']
        word = update.message.text
        url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
        querystring = {"langpair": lang, "q": word}
        headers = {
            'x-rapidapi-key': "24fd2ead8amshc203cd479b8fa8bp18d9b1jsnb8779c61c6a3",
            'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        output = response.json()
        new = output['responseData']['translatedText']
        update.message.reply_text(new, reply_markup=markup)
    except Exception as err:
        update.message.reply_text('Ошибка ' + err.__class__.__name__.__str__() + ': ' + err.__str__(),
                                  reply_markup=markup)


def main():
    updater = Updater('5147513805:AAEiG0-XjDlug2pmoPcRPuufLSZBYs8jbIc', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, translator, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()