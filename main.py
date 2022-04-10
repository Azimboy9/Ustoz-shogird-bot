from collections import UserDict
import logging
from select import select
from coonfig import token
from aiogram import Bot,Dispatcher,executor,types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from buttons import telefon, user, admin, register
from state import Register 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import re
kanal_id = "-1001566172216"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
@dp.message_handler(commands=['start'])
async def do_start(message: types.Message):
    user = message.from_user.first_name 
    await message.answer(f"Assalomu aleykum {user}\nUstozShogird kanalining rasmiy (kopiya) botiga xush kelibsiz!", reply_markup=telefon)
@dp.message_handler(text="Sherik kerak")
async def do_star(message: types.Message):
    await message.answer(f"Sherik topish uchun ariza berish\n\nAriza to'ldirish tugmasini bosing\nkeyin sizga birnecha savollar beriladi. \nHar biriga javob bering. \nOxirida agar hammasi to`g`ri bo`lsa, \nTasdiqlash tugmasini bosing va arizangiz Adminga yuboriladi.", reply_markup=register)
@dp.message_handler(text="Ariza to'ldirish")
async def start_reg(message: types.Message):
    #await message.answer(cache_time=10)
    await message.delete()
    await message.answer("Ismingizni kiriting",reply_markup=ReplyKeyboardRemove())
    await Register.first_name.set()
@dp.message_handler(state=Register.first_name)
async def ism(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data(
        {'ism': ism}
    )
    await message.answer(f"Familiyangizni kiriting:")
    await Register.next()
@dp.message_handler(state=Register.last_name)
async def get_last(message: types.Message, state: FSMContext):
    familiya = message.text
    await state.update_data(
        {'familiya': familiya}
    )
    await message.answer(f"📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\n Java, C++, C#")
    await Register.next()
@dp.message_handler(state=Register.dasturlash_tili)
async def get_photo(message: types.Message, state: FSMContext):
    til = message.text
    await state.update_data(
        {'til': til}
    )
    await message.answer(f"📞 Aloqa:\n\n Bog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")
    await Register.next()
@dp.message_handler(state=Register.phone_number)
async def get_phonenumber(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(
        {'phone': number}
    )
    await message.answer(f"🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")   
    await Register.next()
@dp.message_handler(state=Register.Hudud)
async def get_reg(message: types.Message, state: FSMContext):
    hudud = message.text
    await state.update_data(
        {'region': hudud}
    )
    await message.answer(f"💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")
    await Register.next()
@dp.message_handler(state=Register.cash)
async def get_cash(message: types.Message, state: FSMContext):
    pul = message.text
    await state.update_data(
        {'som': pul}
    )
    await message.answer(f"🕑 Yosh:\n\n Yoshingizni kiriting?\nMasalan, 19")
    await Register.next()
@dp.message_handler(state=Register.yosh)
async def get_age(message: types.Message, state: FSMContext):
    yil = message.text
    await state.update_data(
        {'age': yil}
    )
    await message.answer(f"👨🏻‍💻 Kasbi:\n\n Ishlaysizmi yoki o`qiysizmi?\nMasalan, Talaba")
    await Register.next()
@dp.message_handler(state=Register.kasb)
async def get_kasb(message: types.Message, state: FSMContext):
    a = message.text
    await state.update_data(
        {'hunar': a}
    )
    await message.answer(f"🕰 Murojaat qilish vaqti:\n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")    
    await Register.next()
@dp.message_handler(state=Register.vaqt)
async def get_hour(message: types.Message, state: FSMContext):
    hour = message.text
    await state.update_data(
        {'hour': hour}
    )
    await message.answer(f"🔎 Maqsad:\n\n Maqsadingizni qisqacha yozib bering")    
    await Register.next()
@dp.message_handler(state=Register.maqsad)
async def get_sel(message: types.Message, state: FSMContext):
    c = message.text
    await state.update_data(
        {'sel': c, 'username': message.from_user.username}
    )
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    age = data.get('age')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = message.from_user.username
    msg = f"Sherik kerak:\n\n🏅Sherik:{ism} {familiya}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa:{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi:{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"
    await message.answer(msg, reply_markup=user)
    #await message.answer(f"Barcha malumotlar to'grimi?")
    await Register.next()
@dp.callback_query_handler(text="confirm", state=Register.admin)
async def send(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    age = data.get('age')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = data.get('username')
    msg = f"Foydalanuvchining arizasi:\n\n🏅Sherik:{ism} {familiya}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"
    await call.bot.send_message(1076893638, msg, reply_markup=admin)
    await call.message.answer("Adminga jo'natildi")
@dp.callback_query_handler(text='admin_confirm', user_id=1076893638)
async def ad(call: types.CallbackQuery):
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=kanal_id)
@dp.message_handler(text="Ish joyi kerak")
async def ish(message: types.Message):
    await message.answer(f"Ish joyi topish uchun ariza berish\n\nHozir sizga birnecha savollar beriladi. \nHar biriga javob bering. \nOxirida agar hammasi to`g`ri bo`lsa, \nHA tugmasini bosing va arizangiz Adminga yuboriladi.")
    await message.delete()
    await message.answer("Ismingizni kiriting",reply_markup=ReplyKeyboardRemove())
    await Register.first_name.set()
@dp.message_handler(state=Register.first_name)
async def ism(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data(
        {'ism': ism}
    )
    await message.answer(f"Familiyangizni kiriting:")
    await Register.next()
@dp.message_handler(state=Register.last_name)
async def get_last(message: types.Message, state: FSMContext):
    familiya = message.text
    await state.update_data(
        {'familiya': familiya}
    )
    await message.answer(f"📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\n Java, C++, C#")
    await Register.next()
@dp.message_handler(state=Register.dasturlash_tili)
async def get_photo(message: types.Message, state: FSMContext):
    til = message.text
    await state.update_data(
        {'til': til}
    )
    await message.answer(f"📞 Aloqa:\n\n Bog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")
    await Register.next()
@dp.message_handler(state=Register.phone_number)
async def get_phonenumber(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(
        {'phone': number}
    )
    await message.answer(f"🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")   
    await Register.next()
@dp.message_handler(state=Register.Hudud)
async def get_reg(message: types.Message, state: FSMContext):
    hudud = message.text
    await state.update_data(
        {'region': hudud}
    )
    await message.answer(f"💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")
    await Register.next()
@dp.message_handler(state=Register.cash)
async def get_cash(message: types.Message, state: FSMContext):
    pul = message.text
    await state.update_data(
        {'som': pul}
    )
    await message.answer(f"🕑 Yosh:\n\n Yoshingizni kiriting?\nMasalan, 19")
    await Register.next()
@dp.message_handler(state=Register.yosh)
async def get_age(message: types.Message, state: FSMContext):
    yil = message.text
    await state.update_data(
        {'age': yil}
    )
    await message.answer(f"👨🏻‍💻 Kasbi:\n\n Ishlaysizmi yoki o`qiysizmi?\nMasalan, Talaba")
    await Register.next()
@dp.message_handler(state=Register.kasb)
async def get_kasb(message: types.Message, state: FSMContext):
    a = message.text
    await state.update_data(
        {'hunar': a}
    )
    await message.answer(f"🕰 Murojaat qilish vaqti:\n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")    
    await Register.next()
@dp.message_handler(state=Register.vaqt)
async def get_hour(message: types.Message, state: FSMContext):
    hour = message.text
    await state.update_data(
        {'hour': hour}
    )
    await message.answer(f"🔎 Maqsad:\n\n Maqsadingizni qisqacha yozib bering")    
    await Register.next()
@dp.message_handler(state=Register.maqsad)
async def get_sel(message: types.Message, state: FSMContext):
    c = message.text
    await state.update_data(
        {'sel': c, 'username': message.from_user.username}
    )
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    age = data.get('age')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = message.from_user.username
    msg = f"Ish joyi kerak:\n\nXodim:{ism} {familiya}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa:{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi:{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"
    await message.answer(msg, reply_markup=user)
    await Register.next()
@dp.callback_query_handler(text="confirm", state=Register.admin)
async def send(call:types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    age = data.get('age')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = data.get('username')
    msg = f"Foydalanuvchining arizasi:\n\n🏅Xodim:{ism} {familiya}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"
    await call.bot.send_message(1076893638, msg, reply_keyboard=admin)
    await call.message.answer("Adminga jo'natildi")
@dp.callback_query_handler(text='admin_confirm', user_id=1076893638)
async def ad(call: types.CallbackQuery):
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=kanal_id)
@dp.message_handler(text="Hodim kerak")
async def hodim(message: types.Message):
    await message.answer(f"Hodim topish uchun ariza berish\n\nHozir sizga birnecha savollar beriladi. \nHar biriga javob bering. \nOxirida agar hammasi to`g`ri bo`lsa, \nHA tugmasini bosing va arizangiz Adminga yuboriladi.")
    await message.delete()
    await message.answer("🎓Idora nomi", reply_markup=ReplyKeyboardRemove())
    await Register.idora.set()
@dp.message_handler(state=Register.idora)
async def ism(message: types.Message, state: FSMContext):
    idora = message.text
    await state.update_data(
        {'idora': idora}
    )
    
    await message.answer(f"📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\n Java, C++, C#")
    await Register.next()
@dp.message_handler(state=Register.dasturlash_tili)
async def get_photo(message: types.Message, state: FSMContext):
    til = message.text
    await state.update_data(
        {'til': til}
    )
    await message.answer(f"📞 Aloqa:\n\n Bog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")
    await Register.next()
@dp.message_handler(state=Register.phone_number)
async def get_phonenumber(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(
        {'phone': number}
    )
    await message.answer(f"🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")   
    await Register.next()
@dp.message_handler(state=Register.Hudud)
async def get_reg(message: types.Message, state: FSMContext):
    hudud = message.text
    await state.update_data(
        {'region': hudud}
    )
    await message.answer(f"✍️Masul ism sharifi?")
    await Register.next()
@dp.message_handler(state=Register.masul)
async def get_cash(message: types.Message, state: FSMContext):
    masul = message.text
    await state.update_data(
        {'masul': masul}
    )
    
    await message.answer(f"🕰 Murojaat qilish vaqti:\n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")    
    await Register.next()
@dp.message_handler(state=Register.vaqt)
async def get_hour(message: types.Message, state: FSMContext):
    hour = message.text
    await state.update_data(
        {'hour': hour}
    )
    await message.answer(f"🕰Ish vaqtini kiriting")    
    await Register.next()
@dp.message_handler(state=Register.ish)
async def get_ish(message: types.Message, state: FSMContext):
    n = message.text
    await state.update_data(
        {'ish': n}
    )
    await message.answer(f"💰 Maoshni kiriting ?")
    await Register.next()
@dp.message_handler(state=Register.cash)
async def get_cash(message: types.Message, state: FSMContext):
    pul = message.text
    await state.update_data(
        {'som': pul}
    )
    await message.answer(f"‼️ Qo`shimcha ma`lumotlar?")
    await Register.next()
@dp.message_handler(state=Register.qosh)
async def get_cash(message: types.Message, state: FSMContext):
    qosh = message.text
    await state.update_data(
        {'qosh': qosh, 'username': message.from_user.username}
    )
    data = await state.get_data()
    idora = data.get('idora')
    #familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    masul = data.get('masul')
    hour = data.get('hour')
    ish = data.get('ish')
    som = data.get('som')
    qosh = data.get('qosh')
    username = message.from_user.username
    msg = f"Xodim kerak:\n\nIdora:{idora}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa:{phone}\n🌐Hudud:{region}\n✍️ Mas'ul:{masul}\n🕰 Murojaat vaqti:{ish}\n🕰Murojaat qilish vaqti:{hour}\n💰Narxi:{som}\n‼️Qo'shimcha:{qosh}"
    await message.answer(msg, reply_markup=user)
    await Register.next()
@dp.callback_query_handler(text="confirm", state=Register.admin)
async def send(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idora = data.get('idora')
    #familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    masul = data.get('masul')
    som = data.get('som')
    hour = data.get('hour')
    ish = data.get('ish')
    qosh = data.get('qosh')
    username = data.get('username')
    msg = f"Foydalanuvchining arizasi:\n\nIdora:{idora}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa:{phone}\n🌐Hudud:{region}\n✍️ Mas'ul:{masul}\n🕰 Murojaat vaqti:{ish}\n🕰Murojaat qilish vaqti:{hour}\n💰Narxi:{som}\n‼️Qo'shimcha;{qosh}"
    await call.bot.send_message(1076893638, msg, reply_markup=admin)
    await call.message.answer("Adminga jo'natildi")
@dp.callback_query_handler(text='admin_confirm')
async def ad(call: types.CallbackQuery):
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=kanal_id)
@dp.message_handler(text="Ustoz kerak", user_id=1076893638)
async def ustoz(message: types.message):
    await message.delete()
    await message.answer("Ismingizni kiriting",reply_markup=ReplyKeyboardRemove())
    await Register.first_name.set()
@dp.message_handler(state=Register.first_name)
async def ism(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data(
        {'ism': ism}
    )
    await message.answer(f"Familiyangizni kiriting:")
    await Register.next()
@dp.message_handler(state=Register.last_name)
async def get_last(message: types.Message, state: FSMContext):
    familiya = message.text
    await state.update_data(
        {'familiya': familiya}
    )
    await message.answer(f"📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\n Java, C++, C#")
    await Register.next()
@dp.message_handler(state=Register.dasturlash_tili)
async def get_photo(message: types.Message, state: FSMContext):
    til = message.text
    await state.update_data(
        {'til': til}
    )
    await message.answer(f"📞 Aloqa:\n\n Bog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")
    await Register.next()
@dp.message_handler(state=Register.phone_number)
async def get_phonenumber(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(
        {'phone': number}
    )
    await message.answer(f"🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")   
    await Register.next()
@dp.message_handler(state=Register.Hudud)
async def get_reg(message: types.Message, state: FSMContext):
    hudud = message.text
    await state.update_data(
        {'region': hudud}
    )
    await message.answer(f"💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")
    await Register.next()
@dp.message_handler(state=Register.cash)
async def get_cash(message: types.Message, state: FSMContext):
    pul = message.text
    await state.update_data(
        {'som': pul}
    )
    await message.answer(f"🕑 Yosh:\n\n Yoshingizni kiriting?\nMasalan, 19")
    await Register.next()
@dp.message_handler(state=Register.yosh)
async def get_age(message: types.Message, state: FSMContext):
    yil = message.text
    await state.update_data(
        {'age': yil}
    )
    await message.answer(f"👨🏻‍💻 Kasbi:\n\n Ishlaysizmi yoki o`qiysizmi?\nMasalan, Talaba")
    await Register.next()
@dp.message_handler(state=Register.kasb)
async def get_kasb(message: types.Message, state: FSMContext):
    a = message.text
    await state.update_data(
        {'hunar': a}
    )
    await message.answer(f"🕰 Murojaat qilish vaqti:\n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")    
    await Register.next()
@dp.message_handler(state=Register.vaqt)
async def get_hour(message: types.Message, state: FSMContext):
    hour = message.text
    await state.update_data(
        {'hour': hour}
    )
    await message.answer(f"🔎 Maqsad:\n\n Maqsadingizni qisqacha yozib bering")    
    await Register.next()
@dp.message_handler(state=Register.maqsad)
async def get_sel(message: types.Message, state: FSMContext):
    c = message.text
    await state.update_data(
        {'sel': c, 'username': message.from_user.username}
    )
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    age = data.get('age')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = message.from_user.username
    msg = f"Ustoz kerak:\n\n🎓Shogird:{ism} {familiya}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa:{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi:{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"
    await message.answer(msg, reply_markup=user)
    await Register.next()
@dp.callback_query_handler(text="confirm", state=Register.admin)
async def send(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    age = data.get('age')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = data.get('username')
    msg = f"Foydalanuvchining arizasi:\n\n🎓Shogird:{ism} {familiya}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"#, reply_markup=ariza
    await call.bot.send_message(1076893638, msg,  reply_markup=admin)
    await call.message.answer("Adminga jo'natildi")   
@dp.callback_query_handler(text='admin_confirm', user_id=1076893638)
async def ad(call: types.CallbackQuery):
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=kanal_id)
@dp.message_handler(text="Shogird kerak")
async def ustoz(message: types.message):
    await message.delete()
    await message.answer("Ismingizni kiriting",reply_markup=ReplyKeyboardRemove())
    await Register.first_name.set()
@dp.message_handler(state=Register.first_name)
async def ism(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data(
        {'ism': ism}
    )
    await message.answer(f"Familiyangizni kiriting:")
    await Register.next()
@dp.message_handler(state=Register.last_name)
async def get_last(message: types.Message, state: FSMContext):
    familiya = message.text
    await state.update_data(
        {'familiya': familiya}
    )
    await message.answer("🕑 Yosh:\n\nYoshingizni kiriting?\nMasalan, 19",reply_markup=ReplyKeyboardRemove())
    await Register.next()
@dp.message_handler(state=Register.yosh)
async def ism(message: types.Message, state: FSMContext):
    yosh = message.text
    await state.update_data(
        {'yosh': yosh}
    )
    await message.answer(f"📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\n Java, C++, C#")
    await Register.next()
@dp.message_handler(state=Register.dasturlash_tili)
async def get_last(message: types.Message, state: FSMContext):
    til = message.text
    await state.update_data(
        {'til': til}
    )
    await message.answer(f"📞 Aloqa:\n\n Bog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")
    await Register.next()
@dp.message_handler(state=Register.phone_number)
async def get_last(message: types.Message, state: FSMContext):
    num = message.text
    await state.update_data(
        {'num': num}
    )
    await message.answer(f"🌐 Hudud:\n\n Qaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")
    await Register.next()
@dp.message_handler(state=Register.Hudud)
async def get_last(message: types.Message, state: FSMContext):
    reg = message.text
    await state.update_data(
        {'reg': reg}
    )
    await message.answer(f"💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")
    await Register.next()
@dp.message_handler(state=Register.cash)
async def get_last(message: types.Message, state: FSMContext):
    som = message.text
    await state.update_data(
        {'som': som}
    )
    await message.answer(f"👨🏻‍💻 Kasbi:\n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba")
    await Register.next()
@dp.message_handler(state=Register.kasb)
async def get_last(message: types.Message, state: FSMContext):
    hunar = message.text
    await state.update_data(
        {'hunar': hunar}
    )
    await message.answer(f"🕰 Murojaat qilish vaqti:\n\n Qaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")
    await Register.next()
@dp.message_handler(state=Register.vaqt)
async def get_last(message: types.Message, state: FSMContext):
    hour = message.text
    await state.update_data(
        {'hour': hour}
    )
    await message.answer(f"🔎 Maqsad:\n\nMaqsadingizni qisqacha yozib bering.")
    await Register.next()
@dp.message_handler(state=Register.maqsad)
async def get_last(message: types.Message, state: FSMContext):
    sel = message.text
    await state.update_data(
        {'sel': sel, 'username':message.from_user.username}
    )
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    age = data.get('age')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = message.from_user.username
    msg = f"Shogird kerak:\n\n🎓Ustoz:{ism} {familiya}\n🌐 Yosh:{age}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa:{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi:{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"
    await message.answer(msg, reply_markup=user)
    await Register.next()
@dp.callback_query_handler(text="confirm", state=Register.admin)
async def send(call:types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ism = data.get('ism')
    familiya = data.get('familiya')
    age = data.get('age')
    til = data.get('til')
    phone = data.get('phone')
    region = data.get('region')
    som = data.get('som')
    hunar = data.get('hunar')
    hour = data.get('hour')
    sel = data.get('sel')
    username = data.get('username')
    msg = f"Foydalanuvchining arizasi:\n\n🎓Ustoz:{ism} {familiya}\n🌐 Yosh:{age}\n📚Texnologiya:{til}\n🇺🇿Telegram:@{username}\n📞Aloqa:{phone}\n🌐Hudud:{region}\n💰Narxi:{som}\n👤Yoshi:{age}\n👨🏻‍💻Kasbi:{hunar}\n🕰Murojaat qilish vaqti:{hour}\n🔎Maqsad:{sel}"
    await call.bot.send_message(1076893638, msg, reply_markup=admin)
    await call.message.answer("Adminga jo'natildi")
@dp.callback_query_handler(text='admin_confirm', user_id=1076893638)
async def ad(call: types.CallbackQuery):
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=kanal_id)
@dp.callback_query_handler(text = 'Bekor qilish')
async def bekor(call: types.CallbackQuery):
    await call.message.answer('Siz menyuga qaytdingiz', reply_markup=telefon)
if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)