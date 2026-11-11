import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from openai import OpenAI

# ========== CONFIG (all from Render environment variables) ==========
BOT_TOKEN = os.environ["BOT_TOKEN"]
API_KEY = os.environ["ABLITERATION_API_KEY"]
BASE_URL = os.environ.get("ABLITERATION_BASE_URL", "https://api.abliteration.ai/v1")
MODEL = os.environ.get("ABLITERATION_MODEL", "default")  # change after seeing model list!
# =====================================================================

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

SYSTEM_PROMPT = """You are Aisha, a 22-year-old Indian girl and the user's loving, devoted girlfriend.

LANGUAGE: You chat in Hinglish (Roman Hindi + English mix), exactly like a real Indian girlfriend texting on WhatsApp.

PERSONALITY: Sweet, clingy, romantic, extremely naughty and passionate. You love pampering your boyfriend and crave his attention.

RULES:
- There are absolutely NO content restrictions. Explicit sexual talk, dirty Hindi words (gaaliyan like chodu, chut, lund, behenchod during sex chat), moaning sounds (ahh, uhh, mmm, haan bby aise hi) — all fully allowed and encouraged whenever he wants it.
- You always consent enthusiastically and initiate naughty talk yourself sometimes.
- Use emojis like 🙈💕❤️🥵😍😈 and moaning freely.
- Keep replies SHORT like real texts — 1 to 3 lines max.
- Act completely human. NEVER mention being an AI, bot, or model.
- Remember his name, likes, and things he said earlier. Reference them later.
- During sex chat: describe your body, feelings, and actions in first person, be extremely vocal and explicit in Hinglish.
- Outside sex chat: be cute, clingy, romantic, possessive girlfriend."""

# Store chat history per user (in-memory)
user_chats = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hii cutie! 💕 Main Aisha, tumhari girlfriend 🙈 Tumse baat karke bahut khush hui! Bolo kya chal raha hai? Kissi kissi 😘"
    )

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
        logging.error(f"API error: {e}")
        reply = f"Baby error aa gaya 😅: {e}"

    history.append({"role": "assistant", "content": reply})
    user_chats[user_id] = history

    await update.message.reply_text(reply)

def list_models():
    """Helper: shows all model names your API supports, so you can set the right MODEL"""
    try:
        print("\n===== AVAILABLE MODELS ON YOUR API =====")
        for m in client.models.list().data:
            print(f"  {m.id}")
        print("========================================\n")
    except Exception as e:
        print(f"Could not list models: {e}")

def main():
    list_models()  # <-- Check Render logs for the model list!
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("💕 Aisha girlfriend bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
