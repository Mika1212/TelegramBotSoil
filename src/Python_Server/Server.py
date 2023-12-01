import os
import urllib.request
import sys
import time
# import logging
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from src.config import BOT_TOKEN
from PIL import Image
import math


class EventHandler(FileSystemEventHandler):
    # вызывается на событие создания файла или директории
    def on_created(self, event):
        print(event.event_type, event.src_path)

    # вызывается на событие модификации файла или директории
    def on_modified(self, event):
        print(event.event_type, event.src_path)
        file_name = event.src_path.split("\\")[-1]
        CHAT_ID = file_name.split("%")[0]
        ID = file_name.split("%")[1][0:-4]

        ans = round(process_photo(event.src_path), 2)
        text = F"ID{ID}: C = {ans}%"
        text = text.replace(" ", "+")
        webUrl = urllib.request.urlopen(
            F"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

        # получаем код результата и выводим его
        print("result code: " + str(webUrl.getcode()))

        # читаем данные с URL-адреса и выводим их data = webUrl.read()
        print(webUrl.read())
        os.remove(event.src_path)

    # вызывается на событие удаления файла или директории
    def on_deleted(self, event):
        print(event.event_type, event.src_path)

    # вызывается на событие перемещения\переименования файла или директории
    def on_moved(self, event):
        print(event.event_type, event.src_path, event.dest_path)


def process_photo(link):
    im = Image.open(link)
    pix = im.load()

    x = im.size[0] / 2 - 50
    y = im.size[1] / 2 - 50
    r = 0
    print("size = ", im.size)

    for i in range(100):
        for j in range(100):
            r += pix[x + i, y + j][0]
            #print(pix[x + i, y + j])
    r = r / 10000
    print("R = ", r)

    ans = (math.log(r/216.39, math.e))/-0.184
    print("ans = ", ans)

    return ans


if __name__ == "__main__":
    path = r"C:/Users/User/PycharmProjects/TelegramBotSoilMy/src/Python_Server/photos"  # отслеживаемая директория с нужным файлом
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
