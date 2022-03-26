from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Updater, MessageHandler, Filters
text = 'Черемуха душистая\n' \
       'С весною расцвела\n' \
       'И ветки золотистые,\n' \
       'Что кудри, завила.\n' \
       'Кругом роса медвяная\n' \
       'Сползает по коре,\n' \
       'Под нею зелень пряная\n' \
       'Сияет в серебре.\n' \
       'А рядом, у проталинки,\n' \
       'В траве, между корней,\n' \
       'Бежит, струится маленький\n' \
       'Серебряный ручей.\n' \
       'Черемуха душистая,\n' \
       'Развесившись, стоит,\n' \
       'А зелень золотистая\n' \
       'На солнышке горит.\n' \
       'Ручей волной гремучею\n' \
       'Все ветки обдает\n' \
       'И вкрадчиво под кручею\n' \
       'Ей песенки поет.'
strings = text.split('\n')


def start(update, context):
    update.message.reply_text('Я читаю первую строчку стихотворения, а ты - вторую,'
                              ' затем я - третью, ты - четвёртую и так до конца.\n'
                              '/stop - прервать работу\n/suphler - подсказка\n'
                              'Стихотворение Есенина "Черёмуха"\n'
    )
    context.user_data['string'] = 0
    return string_read(update, context)


def suphler(update, context):
    update.message.reply_text('Подсказка: ' + strings[context.user_data['string']])


def string_read(update, context):
    n = context.user_data['string']
    update.message.reply_text(strings[n])
    context.user_data['string'] += 1
    return 2 if context.user_data['string'] != len(strings) else exit_(update, context)


def string_check(update, context):
    if update.message.text == '/suphler':
        return suphler(update, context)
    if update.message.text == '/stop':
        return stop(update, context)
    n = context.user_data['string']
    if update.message.text != strings[n]:
        update.message.reply_text('Нет, не так!')
        suphler(update, context)
        return 2
    context.user_data['string'] += 1
    return string_read(update, context) if context.user_data['string'] != len(strings) else exit_(update,
                                                                                                  context)


def exit_(update, context):
    update.message.reply_text("Круто! Это была последняя строчка, работа окончена.")
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
            1: [MessageHandler(Filters.text, string_read, pass_user_data=True)],
            2: [MessageHandler(Filters.text, string_check, pass_user_data=True)],
            3: [MessageHandler(Filters.text, exit_)]
        },

        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('suphler', suphler, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()