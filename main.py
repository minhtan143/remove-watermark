import os, glob
import random, string, base64
import requests
from requests_toolbelt import MultipartEncoder

url = 'https://be-prod-web.snapedit.app/api/object_removal/v5/erase_watermark'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpZ25vcmUiLCJwbGF0Zm9ybSI6IndlYiIsImV4cCI6MTcxNTIyNTUxODA4N30.NiPiIq7QB7BGx8c8uz63CHKjXqMrjQUuZMqKBTQbCjY'

def remove_watermark(image, output):
    fields = {'original_preview_image': (image.split('\\')[-1], open(image, 'rb'), 'image/jpg')}
    boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(fields=fields, boundary=boundary)

    headers = {
        'authorization': f'Bearer {token}',
        'Content-Type': m.content_type
    }

    response = requests.post(url, headers=headers, data=m)
    imgdata = base64.b64decode(response.json()['edited_image']['image'])

    os.makedirs(os.path.dirname(output), exist_ok=True)
    open(output, 'wb').write(imgdata)

def main():
    files = glob.glob('input/*')
    for file in files:
        remove_watermark(file, file.replace('input\\', 'output\\'))

if __name__ == "__main__":
    main()