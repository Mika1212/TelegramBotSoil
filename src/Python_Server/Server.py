import urllib.request
import sys
import time
# import logging
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from src.config import BOT_TOKEN


class EventHandler(FileSystemEventHandler):
    # вызывается на событие создания файла или директории
    def on_created(self, event):
        print(event.event_type, event.src_path)



    # вызывается на событие модификации файла или директории
    def on_modified(self, event):
        print(event.event_type, event.src_path)
        file_name = event.src_path.split("\\")[-1]
        CHAT_ID = file_name.split("%")[0]
        print(CHAT_ID)


        webUrl = urllib.request.urlopen(
            F"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Hello+World!")

        # получаем код результата и выводим его
        print("result code: " + str(webUrl.getcode()))

        # читаем данные с URL-адреса и выводим их data = webUrl.read()
        print(webUrl.read())

        # https: // api.telegram.org / bot % TOKEN % / sendMessage?chat_id = % CHAT_ID % & text = Hello + World!

    # вызывается на событие удаления файла или директории
    def on_deleted(self, event):
        print(event.event_type, event.src_path)

    # вызывается на событие перемещения\переименования файла или директории
    def on_moved(self, event):
        print(event.event_type, event.src_path, event.dest_path)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO,
    #                    format='%(asctime)s - %(message)s',
    #                    datefmt='%Y-%m-%d %H:%M:%S')

    path = r"C:/Users/User/PycharmProjects/TelegramBotSoilMy/src/Python_Server"  # отслеживаемая директория с нужным файлом
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


#def main():
#    mypath = "C:/Users/User/PycharmProjects/TelegramBotSoilMy/src/Python_Server"
#    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
#    print(onlyfiles)
#
#
#if __name__ == "__main__":
#    main()
