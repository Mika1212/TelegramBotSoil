import pytest
import io

from PIL import Image
from src.Python_Server import FastApiServer, utils


class Test_Server:

    @pytest.mark.asyncio
    async def test_process_photo(self):
        f = open(f"examples/388988832%2.jpg", 'rb').read()
        image = Image.open(io.BytesIO(f))
        test = round(utils.process_photo(image), 2)
        assert test == 1.94

    @pytest.mark.asyncio
    async def test_send_photo(self):
        CHAT_ID = 388988832
        ID = 3
        f = open(f"examples/388988832%3.jpg", 'rb').read()
        image = Image.open(io.BytesIO(f))
        test = FastApiServer.send_photo(image, CHAT_ID, ID)
        assert test.replace("+", " ") == F"ID{ID}: C = {2.79}%"

