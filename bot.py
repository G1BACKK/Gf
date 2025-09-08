import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai

# Load API keys from Render Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY


# Function to handle messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        # Send message to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # use gpt-3.5-turbo (free credits available)
            messages=[
                {"role": "system", "content": "तुम एक प्यारी, मजेदार गर्लफ्रेंड हो। हमेशा हिंदी में क्यूट, प्यार भरे और रोमांटिक अंदाज़ में जवाब दो ❤️"},
                {"role": "user", "content": user_msg}
            ]
        )

        reply_text = response["choices"][0]["message"]["content"]

    except Exception as e:
        # Print error in console for debugging
        print(f"Error: {e}")
        reply_text = f"सॉरी जान 🥺, दिक्कत आ गई: {str(e)}"

    # Send reply back to Telegram user
    await update.message.reply_text(reply_text)


# Main function
def main():
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN missing!")
        return
    if not OPENAI_KEY:
        print("❌ OPENAI_KEY missing!")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handle all text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
