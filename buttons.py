from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
register = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ariza to'ldirish")]
    ],
    resize_keyboard=True,
)
telefon = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Sherik kerak"), KeyboardButton(text="Ish joyi kerak")],
        [KeyboardButton(text="Hodim kerak"), KeyboardButton(text="Ustoz kerak")],
        [KeyboardButton(text="Shogird kerak")]
    ], 
    resize_keyboard=True,
)
user = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Tasdiqlash", callback_data="confirm"), InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")]
    ],
    resize_keyboard=True
)
admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Tasdiqlash", callback_data="admin_confirm"), InlineKeyboardButton(text="Bekor qilish", callback_data="admin_cancel")]
    ],
    resize_keyboard=True
)
#ariza = ReplyKeyboardMarkup(
    #keyboard=[
        #[KeyboardButton(text="HA✅" ), KeyboardButton(text="YO'Q❌")]
    #],
    #resize_keyboard=True,
#)