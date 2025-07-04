import requests
import json
def video(id,link):
    #"cookie": "lang=ru; _ga_233R9NY1HK=GS1.1.1730446237.1.0.1730446237.0.0.0; _ga=GA1.1.623005752.1730446237; cookieAccept=true",
    headers = {
        'accept': "application/json",
        "accept-language": "ru",
        "content-type": "application/json",

        "priority": "u=1, i",
        "referer": "https://downloader.bot/ru",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36"
    }
    json = {'url':link}
    response = requests.post("https://downloader.bot/api/tiktok/info",headers=headers,json=json)
    response.encoding = 'utf-8'
    print(response.json()['data']['mp4'])

    if response.status_code != 200:
        return "<b>Ошибка! Введите существующую ссылку или обратитесь к админу</b>"
    need_video = requests.get(response.json()['data']['mp4'])
    print(need_video)

    if isinstance(need_video.text,str):
        return "<b>Ошибка на стороне сервера! Исправление займет несколько часов!</b>:"
    elif response.status_code == 200:
        name = f"media/{id}_tiktok.mp4"
        with open(name, 'wb') as file:
            file.write(need_video.content)
        return "Видео успешно скачано!"
    else:
        return f"Не удалось скачать видео. Статус код: {response.status_code}"

