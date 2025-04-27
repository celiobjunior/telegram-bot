# Telegram Bot with Google Gemini

This Telegram bot uses the Google Gemini API to intelligently respond to user questions.

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     TELEGRAM_API_KEY="your_telegram_token_here"
     BOT_USERNAME="your_bot_username_here"
     GEMINI_API_KEY="your_gemini_api_key_here"
     GEMINI_MODEL="your_gemini_model_name_key_here"
     ```

### How to obtain API keys:

#### Telegram Bot Token
1. Talk to [@BotFather](https://t.me/BotFather) on Telegram
2. Use the `/newbot` command and follow the instructions
3. Copy the provided token to the `.env` file

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Log in or create a Google account
3. Create a new API key
4. Copy the key to the `.env` file

## Running the bot

```
python telegram-bot.py
```

## Features

- Responds to user messages using Google Gemini intelligence
- Available commands:
  - `/start` - Starts the conversation
  - `/help` - Displays help
  - `/custom` - Example custom command 