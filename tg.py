from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import Updater, MessageHandler, Filters
import json
from random import shuffle
with open('questions.json', 'r', encoding="UTF-8") as f:
    file = json.load(f)['test']


def start(update, context):
    update.message.reply_text('Сейчас я задам вам вопросы, а вы на них должны ответить."\n'
    )
    context.user_data['questions'] = file
    shuffle(context.user_data['questions'])
    context.user_data['current'] = 0
    context.user_data['right'] = 0
    return question(update, context)


def question(update, context):
    n = context.user_data['current']
    questions = context.user_data['questions']
    if n > 0 and questions[n - 1]['response'] == update.message.text:
        context.user_data['right'] += 1
    if n < len(questions):
        update.message.reply_text('Вопрос: ' + questions[n]['question'])
    context.user_data['current'] += 1
    if context.user_data['current'] <= len(questions):
        return 1
    else:
        return exit_(update, context)


def exit_(update, context):
    update.message.reply_text("Правильных: " + str(context.user_data['right']) + '/' +
                              str(len(context.user_data['questions'])) + '.\nЗаново: /start')
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
            1: [MessageHandler(Filters.text, question, pass_user_data=True)],
            2: [MessageHandler(Filters.text, exit_, pass_user_data=True)]
        },

        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()