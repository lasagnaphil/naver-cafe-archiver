import urllib
import uuid
from typing import List
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, Future
import re

def download_url_blocking(url: str, filename: str) -> uuid.UUID:
    print('Downloading {} from url {}'.format(filename, url))
    with urllib.request.urlopen(url) as conn:
        with open(filename, 'wb') as f:
            f.write(conn.read())
    print('Downloading {} finished!'.format(filename))

class FileDownloader(ThreadPoolExecutor):
    def __init__(self):
        ThreadPoolExecutor.__init__(self, max_workers=4)
        self.url_regex = re.compile(r"\.(\w+)(\?type=\w+)?$")
        self.futures = []

    def download_url(self, url: str) -> uuid.UUID:
        match = self.url_regex.match(url)
        if match:
            extension = match.group(1)
        else:
            extension = 'jpeg'
        file_uuid = uuid.uuid4()
        filename = "{}.{}".format(file_uuid, extension)

        future = self.submit(download_url_blocking, url, filename)
        self.futures.append(future)

        return file_uuid

    def finish(self):
        concurrent.futures.wait(self.futures)

fd = FileDownloader()
for i in range(100):
    fd.download_url('https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?type=asdf')
fd.finish()
fd.shutdown()
