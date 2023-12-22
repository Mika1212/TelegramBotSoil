import io
import urllib.request

from PIL import Image
from fastapi import FastAPI, File, UploadFile

from src.Python_Server import utils
from src.config import BOT_TOKEN

app = FastAPI()


@app.post("/download_photo")
async def create_file(file: UploadFile = File(...)):
    photo = await file.read()
    file_name = file.filename.split("/")[-1]
    ID = file_name.split("%")[1].split(".")[0]
    CHAT_ID = file_name.split("%")[0]
    print(ID)
    print(CHAT_ID)
    image = Image.open(io.BytesIO(photo))
    send_photo(image, CHAT_ID, ID)


def send_photo(photo, CHAT_ID, ID):
    ans = round(utils.process_photo(photo), 2)
    text = F"ID{ID}: C = {ans}%"
    text = text.replace(" ", "+")
    webUrl = urllib.request.urlopen(
        F"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

    # получаем код результата и выводим его
    print("result code: " + str(webUrl.getcode()))

    # читаем данные с URL-адреса и выводим их data = webUrl.read()
    print(webUrl.read())
    return text

