import telebot
from config import *
from telebot import types
import sqlite3

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT OR REPLACE INTO belarusneftdatabase (user_id, user_name, user_surname, username) VALUES (?,?,?,?)', (user_id, user_name, user_surname, username))
    conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    sign_up = types.KeyboardButton('📝 Регистрация')

    markup.add(sign_up)

    bot.send_message(message.chat.id, '💚 Здравствуйте, <b>{0.first_name}!</b>\n'
                                      ' Вас приветствует чат-бот сети АЗС «Белоруснефть»!\n'
                                      ' Предлагаем Вам стать участником нашей программы лояльности.\n'
                                      'Для продолжения нажмите кнопку 📝 Регистрация.'.format(message.from_user),
                                      parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == '📝 Регистрация':
        bot.send_message(message.chat.id, 'Если вы согласны на обработку ваших данных напишите "Да".', parse_mode='html')

    elif message.text == "Да":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        main_menu = types.KeyboardButton('📖 Главное меню')
        markup.add(main_menu)
        bot.send_message(message.chat.id, "💚 Поздравляю! Вы стали участником нашей программы лояльности!\n"
                                          "Посмотреть номер Вашей виртуальной карты можно перейдя в 📖 Главное меню",
                         reply_markup=markup, parse_mode='html')

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

    elif message.text == '📖 Главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        adv_game = types.KeyboardButton('🎲 Рекламные игры')
        bonus_program = types.KeyboardButton('💯 Бонусная программа')
        social_network = types.KeyboardButton('📸 Инстраграм')
        virtual_card = types.KeyboardButton('💳 Посмотреть номер виртуальной карты')
        markup.add(adv_game, bonus_program, social_network, virtual_card)
        bot.send_message(message.chat.id, '💚 <b>{0.first_name}</b>, добро пожаловать в Главное меню!\n'
                                          'Здесь вы сможете:\n'
                                          '- узнать, как принять участие в наших рекламных играх;\n'
                                          '- ознакомиться с условиями программы поощрения "Заправка";\n'
                                          '- подписаться на нас в Инстаграм;\n'
                                          '- просматривать номер вашей виртуальной карты, когда это необходимо!\n'
                                          'Оставайтесь с нами, чтобы важная информация всегда была под рукой!'.format(message.from_user)
                         , parse_mode='html', reply_markup=markup)

    elif message.text == '🎲 Рекламные игры':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Перейти на сайт 💚', url='https://bonus.belorusneft.by/registration')

        markup.add(btn)
        bot.send_message(message.chat.id, '💚 Заполните анкету в личном кабинете для участия '
                                          'в рекламных играх с розыгрышами крупных денежных '
                                          'сумм, подарочных сертификатов и суперпризов от партнера!',
                                          reply_markup=markup)

    elif message.text == '💯 Бонусная программа':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Перейти на сайт 💚', url='https://bit.ly/3xmsebQ')

        markup.add(btn)
        bot.send_message(message.chat.id, '💚 ИЗМЕНЕНИЯ В 2022 году.\n'
                                          '- получайте бонусы: за топливо (1 литр = 1 бонус), '
                                          'за товары (до 10 % от их стоимости);\n'
                                          '- обменивайте бонусы: на нетопливные '
                                          'товары до 50% от их стоимости (1 бонус = 1 копейка);\n'
                                          '- получайте повышенные (х2) бонусы в День Рождения (±3 дня);\n'
                                          '- срок действия бонусов с момента получения – 1 год.', reply_markup=markup)

    elif message.text == '📸 Инстраграм':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Перейти на сайт 💚', url='https://www.instagram.com/belarusn.by/')

        markup.add(btn)
        bot.send_message(message.chat.id, '💚 Изучать Беларусь и строить маршруты проще с туристическим проектом '
                                          '#BelarusN. Мы знаем куда поехать и что посмотреть!\n'
                                          '💚 <b>{0.first_name}</b>, нас уже более 10.000. Присоединяйтесь и Вы, чтобы '
                                          'участвовать в викторинах и конкурсах, узнавать трогательные истории '
                                          'победителей наших розыгрышей, а также следить за самыми свежими новостями и '
                                          'делиться ими с друзьями!'.format(message.from_user), parse_mode='html',
                                          reply_markup=markup)

    elif message.text == '💳 Посмотреть номер виртуальной карты':
        bot.send_message(message.chat.id, f"Номер Вашей виртуальной карты: {message.from_user.id}", parse_mode='html')


bot.polling(none_stop=True)
