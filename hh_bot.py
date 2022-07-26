import telebot
from telebot import types
from hh_parser import HHParser

API_TOKEN = '!!!!!!!!!!!!!!!!токена нет!!!!!!!!!!!!!!!!!!!!!!!!'

bot = telebot.TeleBot(API_TOKEN)


class HhRequest:
    def __init__(self, vacancy_name):
        self.vacancy_name = vacancy_name
        self.vacancy_city = None


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    message = bot.send_message(message.from_user.id,  """\
Привет. Я могу узнать информацию с hh.ru по поводу интересующей тебя вакасии. Для того что бы я мог предоставить
информацию, напиши какая вакансия тебя интересует
""", allow_sending_without_reply=True)
    bot.register_next_step_handler(message, vacancy_name_step)


def vacancy_name_step(message):
    HhRequest.vacancy_name = message.text
    bot.send_message(message.from_user.id, 'Отлично! Теперь напиши город который тебе нужен')
    bot.register_next_step_handler(message, start_hh_parser)


def start_hh_parser(message):
    HhRequest.vacancy_city = message.text
    parser_info = HHParser.hhparser(HhRequest.vacancy_name, HhRequest.vacancy_city)
    if len(parser_info) == 3:
        bot.send_message(message.from_user.id,
                         str(parser_info[0]) + ' ' + str(parser_info[1]) + ' ' + str(parser_info[2]))
    else:
        bot.send_message(message.from_user.id, parser_info)
    bot.register_next_step_handler(message, send_welcome)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()



