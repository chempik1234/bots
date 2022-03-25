from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Updater, MessageHandler, Filters


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop, или пропустить вопрос, послав команду /skip.\n"
        "В каком городе вы живёте?")
    return 1


# Добавили словарь user_data в параметры.
def first_response(update, context):
    if update.message.text == '/skip':
        context.user_data['locality'] = ""
        update.message.reply_text("Какая погода у вас за окном?")
        return 2
    context.user_data['locality'] = update.message.text
    update.message.reply_text(
        "Какая погода в городе {0}?".format(
            context.user_data['locality']))
    return 2


# Добавили словарь user_data в параметры.
def second_response(update, context):
    weather = update.message.text
    if context.user_data['locality']:
        update.message.reply_text(
            "Спасибо за участие в опросе! Привет, {0}!".format(
                context.user_data['locality']))
    else:
        update.message.reply_text("Спасибо за участие в опросе!")
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater('5147513805:AAEiG0-XjDlug2pmoPcRPuufLSZBYs8jbIc', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('start', start)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text, first_response, pass_user_data=True)],
            # ...и для его использования.
            2: [MessageHandler(Filters.text, second_response, pass_user_data=True)]
        },

        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()