import json
import requests as rq


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,ru-RU;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Origin': 'https://idp.vetrf.ru',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}


class BaseSession:

    def __init__(self, cookies=None):
        self.sess = rq.session()
        self.sess.headers = HEADERS
        if cookies is None:
            pass
        else:
            if isinstance(cookies, str):
                try:
                    self.read_cookies(cookies)
                except FileNotFoundError:
                    pass
            elif isinstance(cookies, dict):
                self.sess.cookies.update(cookies)

    def fetch(self, url, data=None, *args, **kwargs):
        if data is None:
            return self.sess.get(url, **kwargs)
        else:
            return self.sess.post(url, data=data, *args, **kwargs)

    def read_cookies(self, file):
        with open(file, 'r') as f:
            self.sess.cookies.update(json.load(f))

    def save_cookies(self, file):
        with open(file, 'w') as f:
            json.dump(self.sess.cookies.get_dict(), f, indent=4)
