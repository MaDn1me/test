import telebot
import sqlite3

conn = sqlite3.connect(r'WHERE_IS_IT')
cur = conn.cursor()

bot = telebot.TeleBot('YOUR_TOKEN')

lst = list()
name = ''
surname = ''
age = 0
lst = list()
dictinory = {}
x = tuple()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   id TEXT PRIMARY KEY,
   name TEXT,
   surname TEXT,
   age TEXT);
""")
conn.commit()


@bot.message_handler(commands=['start'])
def one(message):
    bot.send_message(message.from_user.id,
                     'Привет! Я телеграмм бот который получает и обробатывет информацию об пользователе!')
    bot.send_message(message.from_user.id, 'Для начала спрошу: "Использовал ли ты меня до этого?"')
    bot.register_next_step_handler(message, yes)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global check
    global user_id
    check = False
    user_id = message.from_user.username
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         "Привет! Я телеграмм бот который получает и обробатывет информацию об пользователе!")
        bot.send_message(message.from_user.id, 'Для начала спрошу: "Использовал ли ты меня до этого?"')
        bot.register_next_step_handler(message, yes)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def yes(message):
    if message.text == 'Да':
        text = ''
        conn = sqlite3.connect(r'WHERE_IS_IT')
        cur = conn.cursor()
        user_id = message.from_user.username
        results = cur.execute("SELECT * FROM users WHERE id = '%s'" % user_id).fetchall()
        conn.commit()
        print(results)
        idk = results[0]
        for i in range(len(idk)):
            if i > 0:
                text += idk[i] + ' '
        bot.send_message(message.from_user.id, 'Привет, ' + idk[1] + '!')
    elif message.text == 'Нет':
        bot.send_message(message.from_user.id, 'Тогда начнем.')
        bot.send_message(message.from_user.id, 'Как тебя зовут?')
        bot.register_next_step_handler(message, second_step)


def search(message):
    new = open(r'WHERE_IS_IT', 'r', encoding='utf-8')
    for i in new:
        lst.append(i.strip())
    for i in range(len(lst)):
        print(lst)
        print(lst[i])
        if message.text == lst[i]:
            bot.send_message(message.from_user.id, lst[i + 1])


def start(message):
    bot.send_message(message.from_user.id, 'Как тебя зовут?')
    bot.register_next_step_handler(message, second_step)


def second_step(message):
    global name
    name = message.text
    lst.append(name)
    bot.send_message(message.from_user.id, 'Хорошо, ' + name + '. Какая у тебя фамилия??')
    bot.register_next_step_handler(message, third_step)


def third_step(message):
    global surname
    surname = message.text
    lst.append(surname)
    bot.send_message(message.from_user.id, 'Значит твоя фамилия - ' + surname + ', понятно.')
    bot.send_message(message.from_user.id, 'А сколько тебе лет??')
    bot.register_next_step_handler(message, last_step)


def last_step(message):
    global age
    age = message.text
    lst.append(str(age))
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global x
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню :)')
        x = (str(user_id), str(name), str(surname), str(age))
        dictinory[str(user_id)] = surname, name, str(age)
        print(user_id)
        print(x)
        print(type(user_id))
        conn = sqlite3.connect(r'WHERE_IS_IT')
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?);", x)
        conn.commit()
        lst.clear()
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Значит все по новой -_-')
        bot.send_message(call.message.chat.id, 'Опять пиши привет...')


print('Hello world')
bot.polling(none_stop=True, interval=0)
