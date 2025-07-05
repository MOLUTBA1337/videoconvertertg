import re
import aiohttp
import aiofiles
import re
import os
import asyncio


"""def download_video(id,link):
    headers = {
        'accept': "*/*",
        "accept-language": "ru",
        "content-type": "application/json",
        #"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36"
    }

    json = {
        "url": link,

    }

    get_token_link = "https://ssstik.com.co/ru/"
    get_token = requests.get(get_token_link)

    match = re.search(
        r'<input\b[^>]*\b(?:id\s*=\s*["\']_token["\']|name\s*=\s*["\']token["\'])[^>]*value\s*=\s*["\']([^"\']*)["\']',
        get_token.text
    )

    if match:
        json["token"] = match.group(1)
    else:
        return "<b>Произошла ошибка на сервере!</b>"


    first_link = "https://ssstik.com.co/wp-json/ahc/down/"

    req = requests.post(url=first_link,headers=headers,json=json).json()
    print(json["token"],req)
    try:
        match1 = re.search(
            r'<a\b[^>]*\bid\s*=\s*["\']videodl["\'][^>]*href\s*=\s*["\']([^"\']*)["\']',
            req["html"]
        )
    except IndexError:
        return "<b>Ошибка скачивания, это займет несколько часов!</b>"

    if match1:
        link_for_download =  match1.group(1)
    else:
        return "<b>Произошла ошибка на сервере!</b>"
    last_request = requests.get(link_for_download)
    with open(f"media/{id}_output_video.mp4","wb") as c:
        c.write(last_request.content)
"""


async def download_video(id, link):
    headers = {
        'accept': "*/*",
        "accept-language": "ru",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36"
    }

    get_token_link = "https://ssstik.com.co/ru/"
    first_link = "https://ssstik.com.co/wp-json/ahc/down/"

    async with aiohttp.ClientSession() as session:
        # Step 1: Fetch token page
        try:
            async with session.get(get_token_link, headers=headers) as token_response:
                if token_response.status != 200:
                    return "<b>Ошибка получения токена с сервера!</b>"
                token_html = await token_response.text()
        except aiohttp.ClientError as e:
            return f"<b>Ошибка подключения: {str(e)}</b>"

        # Step 2: Extract token value
        token_match = re.search(
            r'<input\b[^>]*\b(?:id\s*=\s*["\']_token["\']|name\s*=\s*["\']token["\'])[^>]*value\s*=\s*["\']([^"\']*)["\']',
            token_html
        )
        if not token_match:
            return "<b>Не удалось извлечь токен!</b>"

        token_value = token_match.group(1)

        # Step 3: Post URL and token to get video HTML
        json_data = {
            "url": link,
            "token": token_value
        }

        try:
            async with session.post(first_link, headers=headers, json=json_data) as post_response:
                if post_response.status != 200:
                    print(await post_response.text())
                    return "<b>Ошибка получения HTML для загрузки видео.</b>"
                post_json = await post_response.json()
        except (aiohttp.ClientError, ValueError) as e:
            return f"<b>Ошибка при отправке данных: {str(e)}</b>"

        # Step 4: Extract download link from HTML
        html_content = post_json.get("html", "")
        download_match = re.search(
            r'<a\b[^>]*\bid\s*=\s*["\']videodl["\'][^>]*href\s*=\s*["\']([^"\']*)["\']',
            html_content
        )
        if not download_match:
            return "<b>Не удалось извлечь ссылку для загрузки видео!</b>"

        download_url = download_match.group(1)

        try:
            async with session.get(download_url, headers=headers) as video_response:
                if video_response.status != 200:
                    return "<b>Ошибка загрузки видео по полученной ссылке.</b>"
                video_content = await video_response.read()
        except aiohttp.ClientError as e:
            return f"<b>Ошибка при загрузке видео: {str(e)}</b>"

        # Step 6: Write file asynchronously
        os.makedirs("media", exist_ok=True)
        file_path = f"media/{id}_output_video.mp4"

        try:
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(video_content)
        except Exception as e:
            return f"<b>Ошибка при записи файла: {str(e)}</b>"

    return None




