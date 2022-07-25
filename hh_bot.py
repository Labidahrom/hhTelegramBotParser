import telebot
from telebot import types
from hh_parser import HHParser

some = HHParser.hhparser('юрист', 'Пермь')
HHParser.get_first_vacancy(some)



