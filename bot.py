import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start - начать работу с ботом и получить приветственное сообщение.\n/help - получить список доступных команд.\n/show_city <city_name> - отобразить указанный город на карте.\n/remember_city <city_name> - сохранить город в список избранных.\n/show_my_cities - показать все сохраненные города.")
    


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = " ".join(message.text.split()[1:])
    # Реализуй отрисовку города по запросу
    bot.send_message(message.chat.id, "Какой цвет вы хотите использовать? Напишите первую букву цвета на английском языке.")
    bot.register_next_step_handler(message, handle_show_city_def, bot=bot, city_name=city_name)

def handle_show_city_def(message, bot, city_name):
    try:
        user_id = message.chat.id
        color = message.text
        manager.create_graph(f'{user_id}.png', [city_name], color)  # Создание карты для города
        with open(f'{user_id}.png', 'rb') as map:  # Открытие и отправка карты пользователю
            bot.send_photo(user_id, map)
    except Exception:
        bot.send_message(message.chat.id, "Вы не правильно указали цвет. Попробуйте ещё раз.")
        bot.register_next_step_handler(message, handle_show_city_def, bot=bot, city_name=city_name)




@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = " ".join(message.text.split()[1:])
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    bot.send_message(message.chat.id, "Какой цвет вы хотите использовать? Напишите первую букву цвета на английском языке.")
    bot.register_next_step_handler(message, handle_show_visited_cities_def, bot=bot, cities=cities)

def handle_show_visited_cities_def(message, bot, cities):
    try:
        color = message.text
        user_id = message.chat.id
        manager.create_graph(f'{user_id}.png', cities, color)  # Создание карты для города
        with open(f'{user_id}.png', 'rb') as map:  # Открытие и отправка карты пользователю
            bot.send_photo(user_id, map)
    except Exception:
        bot.send_message(message.chat.id, "Вы не правильно указали цвет. Попробуйте ещё раз.")
        bot.register_next_step_handler(message, handle_show_visited_cities_def, bot=bot, cities=cities)

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
