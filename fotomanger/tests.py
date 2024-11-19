import asyncio
import mimetypes
import os
import aiofiles
from aiohttp import ClientSession, FormData, MultipartWriter, BasicAuth

import requests
from django.test import TestCase
from urllib3 import request

# Create your tests here.
# base_dir = '/Users/sokirlov/Pictures/2024-02-16 kriss__ti/'
# base_dir = '/Users/sokirlov/Pictures/2024-04-28/big'
base_dir = '/Users/sokirlov/Pictures/2024-04-30/big'
base_title = 'SGirl'
base_slug = 'sgirl'
gallery = 'Sexys'

def upload_from_directory(img_path, index):

    mime_type, _ = mimetypes.guess_type(img_path)
    data = {
        'title': f"{base_title}-{index}",
        'slug': f"{base_slug}_{index}",
        'gallery': gallery,
        "is_public": 'true',
        # 'image': (img_path.split('/')[-1], f, mime_type)
    }

    with open(img_path, 'rb') as f:
        # content = await f.read()
        # form_data.add_field('image', content, filename=img_path.split('/')[-1], content_type=mime_type)
        file = {'image': (img_path.split('/')[-1], f, mime_type)}
        response = requests.post('http://localhost:8000/api/photo/', data=data, files=file)
        return response

async def start(files):
    # auth = BasicAuth(login="root", password="root")


    tasks = []
    for i, file in enumerate(files):
        if file.endswith('.jpg'):
            fl = os.path.join(base_dir, file)
            if os.path.isfile(fl):
                result = await asyncio.to_thread(upload_from_directory, fl, i)
                print(f'Status Code: {result.status_code}')
                print(f'Content Length: {len(result.text)}')
                # tasks.append(upload_from_directory(fl, i))

    # await asyncio.gather(*tasks)
    print('All images are uploaded.')


if __name__ == '__main__':
    files = os.listdir(base_dir)
    asyncio.run(start(files))