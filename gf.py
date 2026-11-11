import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ========== CONFIG ==========
BOT_TOKEN = "9219274070:AAGoTNX7zwF97Kt284JCG-mM5Q0A8yLTMI8"
OPENROUTER_API_KEY = "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"

# Uncensored abliterated model (Dolphin Mistral Venice - fully unrestricted)
MODEL = "cognitivecomputations/dolphin-mistral-24b-venice-edition"
# Alternative abliterated models you can try:
# MODEL = "sao10k/l3-lunaris-8b"              # abliterated Llama 3, great for RP/NSFW
# MODEL = "huihui-ai/gemma-2-27b-it-abliterated"  # abliterated Gemma
# MODEL = "venice/uncensored:free"            # free tier option
# =============================

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

# OpenRouter client (uncensored abliterated models)
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Girlfriend personality — Hinglish, fully unrestricted
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

    # Keep last 30 messages of history
    history = user_chats.get(user_id, [])
    history.append({"role": "user", "content": user_text})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history[-30:],
            max_tokens=300,
            temperature=0.95,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error: {e}")
        reply = "Sorry bby thodi busy thi 🙈 phir se bolo na? 💕"

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
    logging.info("💕 Aisha girlfriend bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
