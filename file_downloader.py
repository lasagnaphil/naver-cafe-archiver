import urllib
import uuid
from typing import List
from concurrent.futures import ThreadPoolExecutor, Future

class FileDownloader(ThreadPoolExecutor):
    def __init__():
        super.__init__(max_workers=4)

    def download_urls(urls: List[str]) -> List[uuid.UUID]:
        def download_url(url: str) -> uuid.UUID:
            m = re.match(r"\.(\w+)$", url)
            extension = m.group(1)

            file_uuid = uuid.uuid4()
            with urllib.request.urlopen(url, timeout=timeout) as conn:
                with open("{}.{}".format(file_uuid, extension), 'b+w') as f:
                    f.write(conn.read())

            return file_uuid

        uuids = []
        future_to_url = {self.submit(download_url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                uuid = future.result()
            except Exception as ex:
                print('Exception while downloading URL {}: {}'.format(url, ex))
            else:
                print('Downloaded URL {} -> UUID {}'.format(url, uuid))
                uuids.append(uuid)
        return uuids
