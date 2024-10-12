
import telebot
import requests

# Токен Telegram-бота
BOT_TOKEN = '8024337898:AAHlKPtGX4iDzSyEQT2QfVu8CSNEWLMhht4'
# API-ключ от Cohere
COHERE_API_KEY = 'SoNBRbfGZSFsk9ECNOQzlLhM0cJW8Gc0CSgUUdlE'

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для получения ответа от Cohere
def get_ai_response(message_text):
    api_url = "https://api.cohere.ai/generate"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
        "Cohere-Version": "2022-12-06"  # Устанавливаем версию API
    }
    data = {
        "model": "command-xlarge-nightly",  # Бесплатная модель
        "prompt": message_text,
        "max_tokens": 100,
        "temperature": 0.75
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            return response.json()["generations"][0]["text"]
        except KeyError:
            return f"Ошибка в ответе от API: {response.json()}"
    else:
        return f"Ошибка API: {response.status_code}, {response.text}"

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    ai_response = get_ai_response(message.text)
    bot.reply_to(message, ai_response)

# Запуск бота
bot.polling()
