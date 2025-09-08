import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai

# API Keys from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    # Send to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # (cheaper than GPT-4, free credits cover it)
        messages=[
            {"role": "system", "content": "तुम एक प्यारी, मजेदार गर्लफ्रेंड हो। हमेशा हिंदी में क्यूट और प्यार से जवाब दो ❤️"},
            {"role": "user", "content": user_msg}
        ]
    )

    reply_text = response["choices"][0]["message"]["content"]
    await update.message.reply_text(reply_text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
