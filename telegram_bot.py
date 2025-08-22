import logging
import json
import os
from dotenv import load_dotenv
from telegram import Update
from weather_oop import WeatherApp
from voice_recording import record, voice_to_text
from openai import OpenAI
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# Database should be implemented here

load_dotenv()
API_OPENAI_KEY = os.getenv("API_OPENAI_KEY")
BOT_TOKEN = os.getenv("API_TG_KEY")
client = OpenAI(api_key=API_OPENAI_KEY)

all_messages = []


def extract_location(user_voice_to_text):
    sys_message = "you are helpful assistant that extract geographical location from text"
    user_message = f"""extract the city and the country from the following sentence. If either is missing, return null.
    return a python dictionary with exactly two fields: 'city' and 'country'.
    text:{user_voice_to_text}"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": 'system', "content": sys_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0
    )
    return json.loads(response.choices[0].message.content)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ Hi! Send me a city or voice to check the weather.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    all_messages.append(msg)
    location = extract_location(msg)
    if not location["city"] or not location["country"]:
        await update.message.reply_text("❌ Couldn't extract location. Try again with a city and country.")
        return

    city = location["city"]
    country = location["country"]
    weather = WeatherApp(city, country)
    weather.run()

    text = f"""
🌍 Location: {city}, {country}
🌡️ Temp: {weather.temperatur}°C
💨 Wind: {weather.windspeed} km/h
👕 Outfit idea:
{weather.ai_clothing_advice}
"""
    await update.message.reply_text(text.strip())


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    voice_path = "weather_voice.ogg"
    await file.download_to_drive(voice_path)

    await update.message.reply_text("🔄 Transcribing voice...")
    transcript = voice_to_text(voice_path)

    location = extract_location(transcript)
    if not location["city"] or not location["country"]:
        await update.message.reply_text("❌ Couldn't extract location from voice. Try again.")
        return

    city = location["city"]
    country = location["country"]
    weather = WeatherApp(city, country)
    weather.run()

    text = f"""
🌍 Location: {city}, {country}
🌡️ Temp: {weather.temperatur}°C
💨 Wind: {weather.windspeed} km/h
👕 Outfit idea:
{weather.ai_clothing_advice}
"""
    await update.message.reply_text(text.strip())


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("🤖 Bot is running...")
    app.run_polling()
