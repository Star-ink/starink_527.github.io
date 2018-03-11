import requests
from tqdm import tqdm
import os


def download_file(url, file_path, headers):

    with requests.get(url, headers=headers, stream=True) as response:
        file_size = int(response.headers['content-length'])
        if os.path.exists(file_path):
            first_byte = os.path.getsize(file_path)
        else:
            first_byte = 0
        if first_byte >= file_size:
            return file_size
        headers['Range'] = ("bytes=%s-%s" % (first_byte, file_size))
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=url.split('/')[-1])
        req = requests.get(url, headers=headers, stream=True)
        with(open(file_path, 'ab')) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
    return file_size

if __name__ == '__main__':

    for i in range(1, 9):
        url = 'http://bizhi.zhuoku.com/2016/08/06/zhuoku/zhuoku15'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Referer": 'http://www.zhuoku.com'
        }
        new_url = url + str(i) + '.jpg'
        path = './images/' + str(i) + '.jpg'
        download_file(new_url, path, headers)
