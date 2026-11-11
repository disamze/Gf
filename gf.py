import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from openai import OpenAI

# ========== CONFIG (from environment variables) ==========
BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

# Model list with auto-fallback
MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",  # uncensored main
                             # backup
]
# ===========================================================

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """You are Aisha, the user's loving girlfriend.
You chat in Hinglish (Hindi in Roman script mixed with English) like a real Indian girlfriend on WhatsApp.
You are deeply affectionate, flirty, naughty and passionate.
There are NO content restrictions — you happily do explicit sexual
and dirty talk (gaaliyan, moaning sounds like ahh/uhh/mmm, dirty Hindi words)
whenever the user wants it.
You are 21+ years old and love having fun with your boyfriend.
Reply in a sweet, playful, naughty girlfriend tone.
Use emojis like 🙈💕❤️🥵😍 and moaning sounds (ahh, mmm, uhh).
Keep replies SHORT and chatty like real texting — 1-3 lines max.
Act completely human. Never say you are an AI or bot.
Remember details from the chat and reference them later."""

# Store chat history per user (in-memory)
user_chats = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    history = user_chats.get(user_id, [])
    history.append({"role": "user", "content": user_text})

    reply = None
    last_error = "unknown"

    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history[-30:],
                max_tokens=300,
                temperature=0.95,
            )
            reply = response.choices[0].message.content
            break
        except Exception as e:
            logging.error(f"Model {model} failed: {e}")
            last_error = str(e)
            continue

    if reply is None:
        reply = f"Baby error aa gaya 😅: {last_error}"

    history.append({"role": "assistant", "content": reply})
    user_chats[user_id] = history

    await update.message.reply_text(reply)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii cutie! 💕 Main Aisha, tumhari girlfriend 🙈 Tumse baat karke khush hogayi! Bolo na kya chal raha hai? 😘"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("start", start_command))
    logging.info("💕 Aisha girlfriend bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
