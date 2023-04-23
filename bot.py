from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, quote_html
from aiogram.types import ParseMode, InputFile
import time

from utils import texts, filename, extension
from drawing import create_field, delete_file
from service_game import find_best_move, check_win


class TicTacToeBot:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot)
        self.position = []
        self.free_fields = []
        self.user_role = "."
        self.comp_role = "."

    def start(self):
        print("TicTacToeBot launched successfully!")
        self.set_handlers()
        executor.start_polling(self.dp)

    def set_handlers(self):
        @self.dp.message_handler(commands=['start'])
        async def process_start_command(message: types.Message):
            msg = text(texts["start"]["greeting"].format(quote_html(message.from_user.first_name)))

            await message.answer(msg)

        @self.dp.message_handler(commands=['new_game'])
        async def process_start_command(message: types.Message):
            msg = text(texts["new_game"]["choice"])

            keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="X", callback_data="START|X"),
                         types.InlineKeyboardButton(text="O", callback_data="START|O"))

            await message.answer(msg, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

        @self.dp.callback_query_handler(text_startswith="START|")
        async def send_random_value(call: types.CallbackQuery):
            await self.bot.answer_callback_query(call.id)
            await call.message.edit_reply_markup(
                reply_markup=None
            )

            self.user_role = call.data.split('|')[1].lower()
            if self.user_role == "o":
                self.comp_role = "x"
            else:
                self.comp_role = "o"

            self.position = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
            self.free_fields = [i for i in range(1, 10)]

            # await call.message.answer(texts["new_game"]["role_accepted"].format(self.user_role),
            #                           parse_mode=ParseMode.MARKDOWN)

            if self.user_role == "o":
                self.position, field_number = find_best_move(self.position, self.comp_role)
                self.free_fields.remove(field_number)

            await call.message.answer(texts["new_game"]["role_accepted"].format(self.user_role.upper()),
                                      parse_mode=ParseMode.MARKDOWN)

            curr_filename = filename.format(int(time.time()))
            create_field(curr_filename, extension, self.position)

            keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=f"{free_field}", callback_data=f"NEXT|{free_field}")
                           for free_field in self.free_fields])

            await call.message.answer_photo(photo=InputFile(curr_filename), reply_markup=keyboard)
            delete_file(curr_filename)

        @self.dp.callback_query_handler(text_startswith="NEXT|")
        async def send_random_value(call: types.CallbackQuery):
            await self.bot.answer_callback_query(call.id)
            await call.message.delete()

            occupied_field = int(call.data.split('|')[1])
            self.free_fields.remove(occupied_field)
            self.position[(occupied_field - 1) // 3][(occupied_field - 1) % 3] = self.user_role

            # НИЧЬЯ
            if len(self.free_fields) == 0:
                curr_filename = filename.format(int(time.time()))
                create_field(curr_filename, extension, self.position)

                await call.message.answer_photo(photo=InputFile(curr_filename))
                await call.message.answer(texts["end_game"]["tie"])

                delete_file(curr_filename)
            else:
                checked = check_win(self.position, self.user_role)
                if checked:
                    curr_filename = filename.format(int(time.time()))
                    create_field(curr_filename, extension, self.position)

                    await call.message.answer_photo(photo=InputFile(curr_filename))
                    await call.message.answer(texts["end_game"]["win"])

                    delete_file(curr_filename)
                else:
                    if self.user_role == "o":
                        self.position, field_number = find_best_move(self.position, "x")
                        self.free_fields.remove(field_number)
                    else:
                        self.position, field_number = find_best_move(self.position, "o")
                        self.free_fields.remove(field_number)

                    curr_filename = filename.format(int(time.time()))
                    create_field(curr_filename, extension, self.position)

                    checked = check_win(self.position, self.comp_role)
                    if checked:
                        await call.message.answer_photo(photo=InputFile(curr_filename))
                        await call.message.answer(texts["end_game"]["lose"])
                    elif len(self.free_fields) == 0:
                        await call.message.answer_photo(photo=InputFile(curr_filename))
                        await call.message.answer(texts["end_game"]["tie"])
                    else:
                        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
                        keyboard.add(
                            *[types.InlineKeyboardButton(text=f"{free_field}", callback_data=f"NEXT|{free_field}")
                              for free_field in self.free_fields])

                        await call.message.answer_photo(photo=InputFile(curr_filename), reply_markup=keyboard)

                    delete_file(curr_filename)
