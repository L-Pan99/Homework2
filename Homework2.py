import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB'
}

@bot.message_handler(commands=['start', 'help'])
def send_help(message: telebot.types.Message):
    text = ('Для работы введите команду в формате:\n'
            '<имя валюты> <в какую валюту перевести> <количество>\n'
            'Увидеть список валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n' + "\n".join(keys.keys())
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неправильное количество параметров. Введите в формате:\n<валюта> <в какую валюту> <количество>')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)

        text = f"{amount} {quote} = {total_base} {base}"
        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя: {e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка: {e}")

bot.polling()


