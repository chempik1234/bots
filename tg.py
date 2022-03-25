from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Updater, MessageHandler, Filters
sculptures = ['Венера Милосская', 'Дискобол', 'Капитолийская волчица', 'Дорифор']
paints = ['Рождение Венеры', 'Даная', 'Весна', 'Сатурн, пожирающий своего сына', 'Похищение Европы', 'Три грации',
          'Венера Урбинская', 'Падение Икара']
books = ['Иллиада', 'Одиссея', 'Риторика', 'Аппология Сократа']


def start(update, context):
    update.message.reply_text(
        "Здравствуйте! В нашем музее представлены известные античные скульптуры, картины, научные труды и книги.\n"
        "Не забудьте снять верхнюю одежду и надеть чистую обувь, залы должны быть чистыми!\n"
        "Вы можете пройти только в комнату 1"
    )
    return 1


def room1(update, context):
    update.message.reply_text("Вы в зале 1. Здесь находятся скульптуры, например:\n* " + '\n* '.join(sculptures) +
                              '. Можно выйти /exit или пройти в комнату с картинами /room2')
    return 2


def room2(update, context):
    if update.message.text == "/exit":
        return exit_(update, context)
    elif update.message.text == "/room1":
        update.message.reply_text("Вы в зале 2. Здесь находятся картины, например:\n* " + '\n* '.join(paints) +
                                  '. Можно пройти только в 3 зал, там античные книги.')
        return 3
    else:
        update.message.reply_text("Раз вы не ушли, находитесь в зале 2. Здесь находятся картины, например:\n* " +
                                  '\n* '.join(paints) + '. Можно пройти только в 3 зал, там античные книги.')
        return 3


def room3(update, context):
    update.message.reply_text("Вы в зале 3. Здесь представлены книги, есть оригинальные и переведённые. "
                              "Некоторые книги из общего списка:\n* " + "\n* ".join(books) +
                              '.\nПройти можно в /room1 (скульптуры) и /room4 (научные труды)')
    return 4


def room4(update, context):
    if update.message.text == "/room1":
        return room1(update, context)
    elif update.message.text == "/room4":
        update.message.reply_text("Вы в зале 4. Здесь находятся научные труды Аристотеля, Платона, Гиппократа, "
                                  "Архимеда и других учёных. Можно пройти только в 1 зал, там скульптуры.")
        return 1
    else:
        update.message.reply_text("Раз вы не ушли, находитесь в зале 2. Здесь находятся научные труды Аристотеля,"
                                  "Платона, Гиппократа, Архимеда и других учёных. Можно пройти только в 1 зал, "
                                  "там скульптуры.")
        return 1


def exit_(update, context):
    update.message.reply_text("Вы на выходе. Не забудьте забрать свои вещи из гардероба. Всего доброго!")
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
            1: [MessageHandler(Filters.text, room1)],
            2: [MessageHandler(Filters.text, room2)],
            3: [MessageHandler(Filters.text, room3)],
            4: [MessageHandler(Filters.text, room4)],
            5: [MessageHandler(Filters.text, exit_)]
        },

        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()