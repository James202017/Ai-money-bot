import requests
import openai
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен вашего Telegram-бота
BOT_TOKEN = '8110411018:AAEspx8gn2jcgDTh-hghFI_7tiuDIvCg-74'
# Ваш OpenAI API ключ для ChatGPT
OPENAI_API_KEY = 'sk-c0bWPuVcXDfaZZv69tQKT3BlbkFJd01BtL7PSoZZcI2U5wqqEY'

# Установка API ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Функция для генерации текста через ChatGPT
def generate_chatgpt_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",  # Или другой доступный движок
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Функция для генерации изображения через ComfyUI
def generate_image_comfyui(prompt: str) -> str:
    url = "http://localhost:5000/generate"  # Замените на свой endpoint ComfyUI
    payload = {
        "prompt": prompt,
        "width": 512,  # Настройте размер изображения
        "height": 512
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        # Сохранение изображения на сервер
        image_url = response.json().get("image_url")
        return image_url
    else:
        return None

# Функция, которая обрабатывает команды бота
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне текст, и я создам изображение с помощью AI или помогу с чем-то другим.')

# Функция для обработки текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    
    if text.startswith("/image"):
        # Генерация изображения с помощью ComfyUI
        prompt = text[len("/image "):]  # Извлекаем запрос после "/image"
        update.message.reply_text(f"Генерирую изображение по запросу: {prompt}...")
        image_url = generate_image_comfyui(prompt)
        
        if image_url:
            update.message.reply_text(f"Вот изображение по вашему запросу: {image_url}")
        else:
            update.message.reply_text("Произошла ошибка при генерации изображения.")
    else:
        # Генерация ответа через ChatGPT
        update.message.reply_text("Обрабатываю запрос через ChatGPT...")
        response_text = generate_chatgpt_response(text)
        update.message.reply_text(response_text)

# Основная функция для запуска бота
def main():
    # Создание Updater и передача токена бота
    updater = Updater(BOT_TOKEN)
    
    # Получаем диспатчер для обработки сообщений
    dispatcher = updater.dispatcher
    
    # Обработчик команды /start
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Запуск бота
    updater.start_polling()

    # Ожидание завершения работы бота
    updater.idle()

if __name__ == '__main__':
    main()
