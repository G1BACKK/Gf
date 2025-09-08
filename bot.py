import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai

# Load keys from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

# Handle incoming messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # free trial credits work with this
            messages=[
                {"role": "system", "content": "तुम एक प्यारी, मजेदार गर्लफ्रेंड हो। हमेशा हिंदी में क्यूट, प्यार भरे और रोमांटिक अंदाज़ में जवाब दो ❤️"},
                {"role": "user", "content": user_msg}
            ]
        )

        reply_text = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply_text = "सॉरी जान 🥺, अभी थोड़ी दिक्कत आ रही है।"

    await update.message.reply_text(reply_text)

# Start the bot
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
