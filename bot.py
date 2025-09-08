import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq  # Groq client

# Load API keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


# Function to handle messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        # Send message to Groq (LLaMA 3 model)
        response = client.chat.completions.create(
            model="llama3-70b-8192",   # big + free model
            messages=[
                {"role": "system", "content": "तुम एक प्यारी, मजेदार गर्लफ्रेंड हो। हमेशा हिंदी में क्यूट, प्यार भरे और रोमांटिक अंदाज़ में जवाब दो ❤️"},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=512,
        )

        reply_text = response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error: {e}")
        reply_text = f"सॉरी जान 🥺, दिक्कत आ गई: {str(e)}"

    await update.message.reply_text(reply_text)


# Main function
def main():
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN missing!")
        return
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY missing!")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Hindi Girlfriend Bot (Groq) is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
