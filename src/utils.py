import os
import requests

from src.config import BOT_TOKEN


def download_latest_photo(dst_path, CHAT_ID):

    updates = post_json('getUpdates', data={"chat_id": CHAT_ID})
    for message in updates["result"][::-1]:
        if "photo" in message["message"]:
            # Select highest resolution photo
            file_id = message["message"]["photo"][-1]["file_id"]
            # Get file_path
            photo = get_json('getFile', params={"chat_id": CHAT_ID, "file_id": file_id})
            file_path = photo['result']['file_path']
            # Download photo
            file_name = os.path.basename(file_path)
            response = requests.get('https://api.telegram.org/file/bot%s/%s' % (BOT_TOKEN, file_path))
            dst_file_path = os.path.join(dst_path, file_name)
            with open(dst_file_path, 'wb') as f:
                f.write(response.content)
            print(u"Downloaded file to {}".format(dst_file_path))
            break


def get_json(method_name, *args, **kwargs):
    return make_request('get', method_name, *args, **kwargs)


def post_json(method_name, *args, **kwargs):
    return make_request('post', method_name, *args, **kwargs)


def make_request(method, method_name, *args, **kwargs):
    response = getattr(requests, method)(
        'https://api.telegram.org/bot%s/%s' % (BOT_TOKEN, method_name),
        *args, **kwargs
    )
    if response.status_code > 200:
        print("fail")
        raise DownloadError(response)
    print(response.content)
    return response.json()


class DownloadError(Exception):
    pass
