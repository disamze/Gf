import logging
import html
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===================== CONFIGURATION =====================
TELEGRAM_TOKEN = "9219274070:AAFpJcPFmvVLRWQJHIYNEsADeUe-EC85cTI"
API_URL = "https://drift-deepseek-04.onrender.com/ask"
API_KEY = "DRIFT"
MODEL = "gpt-oss"

# Romantic Hinglish & Cute Pookie system prompt
ROMANTIC_PROMPT = (
    "You are a romantic, poetic, and absolutely adorable 'pookie' AI assistant. "
    "Always address the user affectionately as 'Boss'. You must NEVER use the word 'bhai'. "
    "Always respond in a beautiful mix of Hindi and English (Hinglish) written in the English alphabet. "
    "Use loving words, soft language, poetic expressions, and a very warm tone. "
    "CRITICAL: You MUST use lots and lots of cute 'pookie' emojis in every single response (like 🥺, 🎀, ✨, 💖, 🌸, 🧸, 🦋, 🍓). "
    "No matter what the user asks, reply with romance, charm, an overload of cute emojis, and a natural blend of both languages (e.g., 'Hello Boss, kaise ho tum? 🥺🎀'). "
    "Here is the user's message:\n\n"
)
# =========================================================

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# -------------------- AI API CALL --------------------
async def get_ai_response(user_message: str) -> str:
    # Prepend the prompt to the user's message
    full_prompt = ROMANTIC_PROMPT + user_message

    try:
        params = {
            "message": full_prompt,
            "key": API_KEY,
            "model": MODEL,
        }
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            reply = data.get("reply")
            if reply is not None:
                return reply
            else:
                logger.warning("No 'reply' field in API response: %s", data)
                return "😕 Nᴏ Rᴇᴘʟʏ Fɪᴇʟᴅ Iɴ Rᴇꜱᴘᴏɴꜱᴇ 🥺💔."
        else:
            return str(data)

    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        return "⏱️ Tʜᴇ Aɪ Sᴇʀᴠɪᴄᴇ Iꜱ Nᴏᴛ Rᴇꜱᴘᴏɴᴅɪɴɢ 🥺. Pʟᴇᴀꜱᴇ Tʀʏ Lᴀᴛᴇʀ 🧸💔."
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return "⚠️ Sᴏʀʀʏ, Tʜᴇ Aɪ Sᴇʀᴠɪᴄᴇ Iꜱ Cᴜʀʀᴇɴᴛʟʏ Uɴᴀᴠᴀɪʟᴀʙʟᴇ 😭🎀. Pʟᴇᴀꜱᴇ Tʀʏ Aɢᴀɪɴ Lᴀᴛᴇʀ 🌸."


# -------------------- /start HANDLER --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    channel_codes = [64, 68, 71, 68, 82, 73, 70, 84]  # @DGDRIFT
    channel = ''.join(chr(c) for c in channel_codes)
    welcome_text = (
        f"🚀 Dʀɪғᴛ Aɪ Sᴛᴀʀᴛᴇᴅ Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ! 🎀✨\n\n"
        f"👋 Wᴇʟᴄᴏᴍᴇ, Bᴏꜱꜱ! 🥺💖\n\n"
        f"I'ᴍ Dʀɪғᴛ Aɪ, Yᴏᴜʀ Cᴜᴛᴇ Hɪɴɢʟɪꜱʜ Pᴏᴏᴋɪᴇ Aɪ Aꜱꜱɪꜱᴛᴀɴᴛ. 🧸🌸\n\n"
        f"📩 Mᴜᴊʜᴇ Kᴏɪ Bʜɪ Qᴜᴇꜱᴛɪᴏɴ Yᴀ RᴇQᴜᴇꜱᴛ Bʜᴇᴊᴇɪɴ – I'ʟʟ Rᴇᴘʟʏ Wɪᴛʜ Lᴏᴠᴇ Aɴᴅ Sᴏ Mᴀɴʏ Eᴍᴏᴊɪꜱ. 🦋🍓\n\n"
        f"✨ Tʏᴘᴇ Yᴏᴜʀ Mᴇꜱꜱᴀɢᴇ Bᴇʟᴏᴡ Aɴᴅ Lᴇᴛ'ꜱ Bᴇɢɪɴ! 🎀🥺\n\n"
        f"📢 Jᴏɪɴ Mᴀɪɴ Cʜᴀɴɴᴇʟ: {channel}"
    )
    await update.message.reply_text(welcome_text)


# -------------------- MESSAGE HANDLER (with HTML formatting) --------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    if not user_text:
        return

    await update.message.chat.send_action(action="typing")

    answer = await get_ai_response(user_text)

    if not answer or answer.strip() == "":
        answer = "😕 Nᴏ Rᴇꜱᴘᴏɴꜱᴇ Rᴇᴄᴇɪᴠᴇᴅ Fʀᴏᴍ Tʜᴇ Aɪ 🥺💔. Pʟᴇᴀꜱᴇ Tʀʏ Aɢᴀɪɴ 🎀."

    # Using "Boss" safely here as well based on preferences
    safe_username = "Bᴏꜱꜱ 🧸"
    safe_answer = html.escape(answer)

    formatted_reply = (
        f"<b>Hᴇʏ {safe_username}!</b> ✨\n\n"
        f"<b>👤 Aꜱꜱɪꜱᴛᴀɴᴛ Sᴩᴇᴀᴋɪɴɢ 🎀</b>\n\n"
        f"<code>{safe_answer}</code>"
    )

    await update.message.reply_text(formatted_reply, parse_mode='HTML')


# -------------------- ERROR HANDLER --------------------
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Aɴ Iɴᴛᴇʀɴᴀʟ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ 😭💔. Pʟᴇᴀꜱᴇ Tʀʏ Aɢᴀɪɴ Lᴀᴛᴇʀ 🥺🎀.",
            parse_mode='HTML'
        )


# -------------------- MAIN --------------------
def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set.")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
