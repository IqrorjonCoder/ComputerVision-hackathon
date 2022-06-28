import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = 'XXXX XXXX XXXX XXXX'

bot = Bot(token=API_TOKEN)

button1 = KeyboardButton("bazaga qo'shilish")
button2 = KeyboardButton('Anonym Coders jamoasi')
button3 = KeyboardButton("hisobni ko'rish")

keybord1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2).add(button3)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Salom bu Anonym Coder tomonidan ishlab chiqilgan EasyPay loyihasi uchun ro'yxatga olish "
                         "boti !!!", reply_markup=keybord1)

    class Form(StatesGroup):
        ism = State()
        familiya = State()
        karta_raqam = State()
        karta_muddat = State()
        karta_parol = State()

    @dp.message_handler(text="bazaga qo'shilish")
    async def cmd_start(message: types.Message):
        await Form.ism.set()
        await message.answer("Iltimos ismingizni kiriting ?")

    @dp.message_handler(state=Form.ism)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['ism'] = message.text
        await Form.next()
        await message.answer("Familiyangizni kiriting ?")

    @dp.message_handler(state=Form.familiya)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['familiya'] = message.text
        await Form.next()
        await message.answer("Karta raqamingizni kiriting ?")

    @dp.message_handler(state=Form.karta_raqam)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['karta_raqam'] = message.text
        await Form.next()
        await message.answer("Kartangiz amal qilish muddatini kiriting ?")

    @dp.message_handler(state=Form.karta_muddat)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['karta_muddat'] = message.text
        await Form.next()
        await message.answer("Kartangiz parolini kiriting ?")

    @dp.message_handler(state=Form.karta_parol)
    async def process_gender(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['karta_parol'] = message.text
            data['karta_hisob'] = "10000"

            rasm_url = f"./photos/{data['ism']}__{data['familiya']}__{data['karta_raqam']}__{data['karta_muddat']}__{data['karta_hisob']}__{data['karta_parol']}"
            json_url = f"./jsons/{data['ism']}__{data['familiya']}__{data['karta_raqam']}__{data['karta_muddat']}__{data['karta_hisob']}__{data['karta_parol']}"

            dic = {
                "ism": data['ism'],
                "familiya": data['familiya'],
                "karta_raqam": data['karta_raqam'],
                "karta_muddat": data['karta_muddat'],
                "karta_hisob": data['karta_hisob'],
                "karta_parol": data['karta_parol'],
                "rasm_url": rasm_url
            }

            with open(f"{json_url}.json", "w") as outfile:
                json.dump(dic, outfile)

            with open(f"database_json.json", "w") as outfile:
                json.dump(dic, outfile)

        await message.answer("Rasmingizni kiritng: ")

        @dp.message_handler(content_types=['photo'])
        async def handle_docs_photo(message: types.Message):
            try:

                f = open(f'database_json.json', 'r')
                data = json.load(f)
                #
                await message.photo[-1].download(destination_file=f"{data['rasm_url']}.jpg")

                await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz !!!")

                # await message.answer(f"ism           : {data['ism']}\n"
                #                      f"familiya      : {data['familiya']}\n"
                #                      f"karta raqami  : {data['karta_raqam']}\n"
                #                      f"karta muddati : {data['karta_muddat']}\n"
                #                      f"karta paroli  : {data['karta_parol']}\n"
                #                      f"karta hisobi  : {data['karta_hisob']}\n"
                #                      f"rasm url      : {data['rasm_url']}")
                await message.answer("Bazaga yana odam qo'shish uchun BAZAGA QO'SHILISH tugmasini bosing !!!")


            except:
                pass

        await state.finish()


@dp.message_handler(text="hisobni ko'rish")
async def cmd_start(message: types.Message):
    await message.answer("Anonym Coders jamoasi hali berib bu funksiyani qo'shgani yo'q !!!")


@dp.message_handler(text="Anonym Coders jamoasi")
async def cmd_start(message: types.Message):
    await message.answer("Anonym Coders jamoasi Hambridge Hackathonda qatnashayotgan va EasyPay dasturi ustida ish "
                         "olib borayotgan jamoa !!!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
