import random
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import Updater, MessageHandler, Filters
times = {'30 минут': 30 * 60,
         '1 минута': 1 * 60,
         '5 минут': 5 * 60}
cubes = {'кинуть один шестигранный  кубик': lambda x: str(random.randint(1, 6)),
         'кинуть 2 шестигранных кубика одноверменно': lambda x: str(random.randint(1, 6)) + ' ' +
                                                                str(random.randint(1, 6)),
         'кинуть 20-гранный кубик': lambda x: str(random.randint(1, 20))}
chat_ids_string = {}


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text=chat_ids_string[job.context] + ' истекло')


def set_timer(update, context, string):
    chat_id = update.message.chat_id
    try:
        if string not in times.keys():
            return
        due = times[string]
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return
        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        chat_ids_string[chat_id] = string
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'засек {string}'
        if job_removed:
            text += ' Старая задача удалена.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text)

    except (IndexError, ValueError) as err:
        update.message.reply_text(err.__str__)
    except Exception as err:
        print(err)


def start(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "/dice - кинуть кубики, /timer - засечь время",
        reply_markup=markup
    )


def timer_keys(update, context):
    reply_keyboard = [['30 минут', '5 минут', '1 минута']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        text="Сколько времени засечь?",
        reply_markup=markup
    )


def dice(update, context):
    reply_keyboard = [['кинуть один шестигранный  кубик', 'кинуть 2 шестигранных кубика одноверменно'],
                      ['кинуть 20-гранный кубик', 'вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Сколько кубиков бросить?",
        reply_markup=markup
    )


def check_rus_args(update, context):
    if update.message.text in times.keys():
        set_timer(update, context, update.message.text)
    elif update.message.text in cubes.keys():
        update.message.reply_text(cubes[update.message.text](1))


def main():
    updater = Updater('5147513805:AAEiG0-XjDlug2pmoPcRPuufLSZBYs8jbIc', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("timer", timer_keys, pass_args=True))
    text_handler = MessageHandler(Filters.text, check_rus_args)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()