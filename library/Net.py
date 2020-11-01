from urllib.error import HTTPError
import urllib.request
import io


class Net:
    def scale(url):
        try:
            return io.BytesIO(urllib.request.urlopen(url).read())
        except HTTPError:
            return ""
