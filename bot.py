import requests
import datetime
from config import API_KEY, BOT_TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю тебе прогноз погоды")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "ясно",
        "Rain": "дождь",
        "Snow": "снег",
        "Clouds": "облачно",
        "Thunderstorm": "гроза"
    }

    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_KEY}&units=metric&lang=ru'
        )
        data = response.json()

        city = data["name"]
        current_temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        wind = data["wind"]["speed"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = ""

        await message.answer(
            f"<b>📅 Сегодня:</b> {datetime.datetime.now().strftime('%d-%m-%Y')}\n"
            f"<b>🌆 Город:</b> {city}\n"
            f"<b>🌡 Температра:</b> {current_temp}°C, <i>{wd}</i>\n"
            f"<b>🫡 Ощущается как:</b> {feels_like}°C.\n"
            f"<b>💧 Влажность воздуха:</b> {humidity}%\n"
            f"<b>🎈 Давление:</b> {pressure} мм.рт.ст\n"
            f"<b>🌅 Восход:</b> {sunrise}\n"
            f"<b>🌄 Закат:</b> {sunset}\n"
            f"<b>💨 Скорость ветра:</b> {wind}м/с"
        )
    except:
        await message.reply("Я не знаю такого города.../")


if __name__ == '__main__':
    executor.start_polling(dp)
