from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


order_flavor = ["микс дня", "сладкий", "кислый", "свежий"]
order_heaviness = ["лёгкий", "средний", "тяжелый", "убийственный"]
order_bowl = ["чаша", "грейп", "гранат", "ананас"]


class OrderStates(StatesGroup):
    waiting_for_order_flavor = State()
    waiting_for_order_heaviness = State()
    waiting_for_order_bowl = State()


async def order_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for flavor in order_flavor:
        keyboard.add(flavor)
    await message.answer("Какой вкус желаете?", reply_markup = keyboard)
    await OrderStates.waiting_for_order_flavor.set()

async def order_heavy(message: types.Message, state: FSMContext):
    if message.text.lower() not in order_flavor:
        await message.answer("Пожалуйста, выберите вкус используя появившиеся снизу кнопки.")
        return
    await state.update_data(hookah_flavor = message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for heaviness in order_heaviness:
        keyboard.add(heaviness)

    await OrderStates.next()
    await message.answer("Хорошо, теперь давайте решим с крепостью:", reply_markup = keyboard)


async def hookah_type(message: types.Message, state: FSMContext):
    if message.text.lower() not in order_heaviness:
        await message.answer("Пожалуйста, выберите крепость кальяна используя появившиеся снизу кнопки.")
        return
    await state.update_data(hookah_heaviness = message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    for bowl in order_bowl:
        keyboard.add(bowl)

    await OrderStates.next()
    await message.answer("Круто, на чём забьём?", reply_markup = keyboard)



async def order_finish(message:types.Message, state: FSMContext):
    if message.text.lower() not in order_bowl:
        await message.answer("Пожалуйста, выберите тип кальяна используя появившиеся снизу кнопки.")
        return
    guest_order = await state.get_data()
    await message.answer(f"Ваш заказ:\n Вкус - {guest_order['hookah_flavor']}\n" f"Крепость - {guest_order['hookah_heaviness']}\n" f"Тип чаши - {message.text.lower()}\n" "Сейчас кожаный мешок всё сделает, приятного покура=)", reply_markup = types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_order(dp: Dispatcher):
    dp.register_message_handler(order_start, commands = "order", state = "*")
    dp.register_message_handler(order_heavy, state = OrderStates.waiting_for_order_flavor)
    dp.register_message_handler(hookah_type, state = OrderStates.waiting_for_order_heaviness)
    dp.register_message_handler(order_finish, state = OrderStates.waiting_for_order_bowl)