# SkyDresser

**SkyDresser** is a voice-enabled, LLM-powered weather assistant.
It combines weather APIs, OpenAI’s language models, and some careful prompt engineering to deliver natural, human-like weather updates.

You can run it in **two modes**:
- **Standalone** (run locally via `main.py`) — test and interact with the assistant directly on your machine.
- **Telegram Bot** (via `telegram_bot.py`) — deploy the assistant to Telegram, with text and **voice message support**.

---

## ✨ Features

- **Real-time weather queries** with external APIs.
- **LLM integration (OpenAI)** for understanding queries and generating friendly responses.
- **Prompt engineering** to make the assistant respond clearly and naturally instead of dumping raw API data.
- **Telegram bot deployment** for easy access anywhere.
- **Voice messaging**: send a short audio clip in Telegram → it’s transcribed, interpreted, and answered.
- **Database support** (`data.py`) for logging/storing queries and results.
- **Configurable via `.env`**, so no secrets are exposed in code.

---

## 🛠 How It’s Organized

```
telegram_bot_weather/
│
├── telegram_bot.py      # Deploys the assistant as a Telegram bot
├── main.py              # Standalone mode (local testing)
├── weather_oop.py       # Weather logic in OOP style
├── voice_recording.py   # Handles voice messages and audio processing
├── data.py              # Database helpers (store queries, etc.)
├── requirements.txt     # Dependencies
├── .env.example         # Example config file
└── .gitignore           # Keeps secrets/artifacts out of git
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/pejman93/SkyDresser.git
cd SkyDresser
```

### 2. Set up environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure `.env`
Copy the example config:
```bash
cp .env.example .env
```

Fill in your keys:
```
API_OPENAI_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
WEATHER_API_KEY=your_weather_api_key_here
API_SOUND_KEY=your_assemblyai_key_here
```

### 5. Run
- **Local (no Telegram):**
  ```bash
  python main.py
  ```
- **Telegram bot:**
  ```bash
  python telegram_bot.py
  ```

---

## 🔒 Security
- `.env` is git-ignored. API keys **stay local**.
- If you ever accidentally commit a key, revoke it and remove it from git history before pushing.

---

## 🌤 Why “SkyDresser”?
This assistant doesn’t just fetch the weather.
It uses an LLM to *interpret weather conditions into something human-friendly* — like a small helper that tells you whether to grab an umbrella, wear a jacket, or just enjoy the sun.

---

## 🗣 Telegram Voice Highlight
One of the best parts of SkyDresser is **voice interaction**:

1. Record a short voice note in Telegram.
2. The bot transcribes it → feeds it through an LLM with weather context.
3. You get back a natural, clear response in chat.

This transforms the bot from a rigid query tool into a **conversational assistant**.

---

## ⚡️ Why It’s Different
Unlike many weather bots that only dump raw data, SkyDresser:
- Uses **OpenAI’s LLM** to interpret intent.
- Applies **prompt engineering** so answers are natural, not robotic.
- Supports **voice-based interaction**, which feels far more personal.
- Can run **locally** or via **Telegram deployment**.

---

## ✅ Status
SkyDresser is a functional prototype:
- Fully working locally and on Telegram.
- Clean, modular code ready for extension.

---

## 🌱 Future Directions
- Richer multi-day forecasts.
- More personalized advice (“take a sweater”, “don’t forget sunscreen”).
- Support for more languages in both text and voice.
- Deployable beyond Telegram (e.g. WhatsApp, Slack).

