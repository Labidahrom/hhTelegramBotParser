import telebot
from telebot import types
from hh_parser import HHParser

API_TOKEN = 'token'

bot = telebot.TeleBot(API_TOKEN)


class HhRequest:
    def __init__(self):
        self.vacancy_name = None
        self.vacancy_city = None
        self.vacancy_amount = None
        self.vacancy_salary = None
        self.vacancy_link = None


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
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Количество вакансий', 'Средняя зарплата', 'Пример вакансии')
    HhRequest.vacancy_city = message.text
    parser_info = HHParser.hhparser(HhRequest.vacancy_name, HhRequest.vacancy_city)
    if len(parser_info) == 3:
        bot.send_message(message.from_user.id, 'Выберите что вас интересует:', reply_markup=markup,
                         allow_sending_without_reply=True)
        HhRequest.vacancy_amount = parser_info[0]
        HhRequest.vacancy_salary = parser_info[1]
        HhRequest.vacancy_link = parser_info[2]
    else:
        bot.send_message(message.from_user.id, parser_info)
    bot.register_next_step_handler(message, choose_option)


def choose_option(message):
    if message.text == "Количество вакансий":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Вернуться назад')
        bot.send_message(message.from_user.id, HhRequest.vacancy_amount, reply_markup=markup,
                         allow_sending_without_reply=True)
    elif message.text == "Средняя зарплата":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Вернуться назад')
        bot.send_message(message.from_user.id, HhRequest.vacancy_salary, reply_markup=markup,
                         allow_sending_without_reply=True)
    elif message.text == "Пример вакансии":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Вернуться назад')
        HhRequest.vacancy_description = HHParser.get_first_vacancy(HhRequest.vacancy_link)
        bot.send_message(message.from_user.id, HhRequest.vacancy_description, reply_markup=markup,
                         allow_sending_without_reply=True)
    else:
        bot.send_message(message.from_user.id, 'Ниче не выбрал')
    bot.register_next_step_handler(message, second_step)


def second_step(message):
    if message.text == "Вернуться назад":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Количество вакансий', 'Средняя зарплата', 'Пример вакансии')
        bot.send_message(message.from_user.id, HhRequest.vacancy_amount, reply_markup=markup,
                         allow_sending_without_reply=True)
        bot.register_next_step_handler(message, choose_option)
    elif message.text == "Средняя зарплата":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Количество вакансий', 'Пример вакансии')
        bot.send_message(message.from_user.id, HhRequest.vacancy_salary, reply_markup=markup,
                         allow_sending_without_reply=True)
        bot.register_next_step_handler(message, choose_option)
    elif message.text == "Пример вакансии":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Количество вакансий', 'Средняя зарплата')
        bot.send_message(message.from_user.id, vacancy_description, reply_markup=markup,
                         allow_sending_without_reply=True)
    else:
        bot.send_message(message.from_user.id, 'Ниче не выбрал')
        bot.register_next_step_handler(message, send_welcome)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()



