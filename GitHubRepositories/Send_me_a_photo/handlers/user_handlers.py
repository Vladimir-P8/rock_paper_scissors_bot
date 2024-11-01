import requests

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from config_data.config import Config,load_config
from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_LINK_RU, LEXICON_ERR_MESSAGE_RU
#from services.services import get_bot_choice, get_winner
API_URL = 'https://api.telegram.org/bot'

router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)

# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.message(F.text == LEXICON_RU['yes_button'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)

# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(F.text == LEXICON_RU['no_button'])
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])

#Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(F.text.in_([LEXICON_RU['cat'],
                            LEXICON_RU['dog'],
                            LEXICON_RU['fox'],
                            ]))
async def process_game_button(message: Message):
    #bot_choice = get_bot_choice()
    await message.answer(text='Твой выбор - '+message.text)
    animal_response = requests.get(LEXICON_LINK_RU[message.text])
    # Загружаем конфиг в переменную config
    config: Config = load_config()
    bot_token = config.tg_bot.token
    if animal_response.status_code == 200:
        if message.text=='Кошечка 😼':
            animal_link = animal_response.json()[0]["url"]
        elif message.text=='Собачка 🐶':
            animal_link = animal_response.json()["url"]
        elif message.text == 'Лисичка 🦊':
            animal_link = animal_response.json()["image"]

        requests.get(f'{API_URL}{bot_token}/sendPhoto?chat_id={message.chat.id}&photo={animal_link}')
    else:
        requests.get(f'{API_URL}{bot_token}/sendMessage?chat_id={message.chat.id}&text={LEXICON_ERR_MESSAGE_RU[message.text]}')

    #winner = get_winner(message.text, bot_choice)
    await message.answer(text="<b>Ещё слать?</b>", reply_markup=yes_no_kb)
