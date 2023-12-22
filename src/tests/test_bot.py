import pytest

from unittest.mock import AsyncMock

from src.config import bot
from src.main import dp
from src.states import States
from src import text, kb
from src.handlers import start_handler, menu, how_it_works, message_us, message_us_question, message_us_mail, \
    instruction, send_photo, handle_photo


class Test_Bot:
    @pytest.mark.asyncio
    async def test_start(self):
        text_mock = "/start"
        message_mock = AsyncMock(text=text_mock)
        await start_handler(msg=message_mock)
        message_mock.answer.assert_called_with(text.greet_text.format(name=message_mock.from_user.full_name),
                                               reply_markup=kb.menu)

    @pytest.mark.asyncio
    async def test_menu(self):
        text_mock = "Меню"
        message_mock = AsyncMock(text=text_mock)
        await menu(msg=message_mock)
        message_mock.answer.assert_called_with(text.menu_text, reply_markup=kb.menu)

    @pytest.mark.asyncio
    async def test_how_it_works(self):
        text_mock1 = "Меню"
        message_mock1 = AsyncMock(text=text_mock1)
        await menu(msg=message_mock1)

        text_mock2 = "how_it_works"
        message_mock2 = AsyncMock(text=text_mock2)
        await how_it_works(clbck=message_mock2, state=States.main_menu)

        assert message_mock2.mock_calls[0].args[0] == text.how_it_works_text
        assert message_mock2.mock_calls[1].args[0] == text.exit_text

    @pytest.mark.asyncio
    async def test_message_us(self):
        text_mock1 = "Меню"
        message_mock1 = AsyncMock(text=text_mock1)
        await menu(msg=message_mock1)

        text_mock2 = "message_us"
        message_mock2 = AsyncMock(text=text_mock2)
        await message_us(clbck=message_mock2, state=dp.fsm.storage)
        assert message_mock2.mock_calls[0].args[0] == text.message_us_text
        assert message_mock2.mock_calls[1].args[0] == text.exit_text

        text_mock3 = "Как дела?"
        message_mock3 = AsyncMock(text=text_mock3)
        await message_us_question(msg=message_mock3, state=dp.fsm.resolve_context(bot, 1, 1))
        assert message_mock3.mock_calls[0].args[0] == text.mail_text

        text_mock4 = "ilravgaz05@mail.ru"
        message_mock4 = AsyncMock(text=text_mock4)
        await message_us_mail(msg=message_mock4, state=dp.fsm.resolve_context(bot, 1, 1))
        message_mock4.answer.assert_called_with(text.question_all_text.format(question=text_mock3, mail=text_mock4),
                                                parse_mode='HTML', reply_markup=kb.yes_no_kb)

    @pytest.mark.asyncio
    async def test_instructions(self):
        text_mock1 = "Меню"
        message_mock1 = AsyncMock(text=text_mock1)
        await menu(msg=message_mock1)

        text_mock2 = "instruction"
        message_mock2 = AsyncMock(text=text_mock2)
        await instruction(clbck=message_mock2, state=States.main_menu)

        assert message_mock2.mock_calls[0].args[0] == text.instruction_text
        assert message_mock2.mock_calls[1].args[0] == text.exit_text

    @pytest.mark.asyncio
    async def test_send_photo(self):
        text_mock1 = "Меню"
        message_mock1 = AsyncMock(text=text_mock1)
        await menu(msg=message_mock1)

        text_mock2 = "send_photo"
        message_mock2 = AsyncMock(text=text_mock2)
        await send_photo(clbck=message_mock2, state=dp.fsm.resolve_context(bot, 1, 1))

        assert message_mock2.mock_calls[0].args[0] == text.send_photo_text
        assert message_mock2.mock_calls[1].args[0] == text.exit_text

