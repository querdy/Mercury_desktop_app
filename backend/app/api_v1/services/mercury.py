import json

from bs4 import BeautifulSoup

from app.api_v1.services.vetis import Vetis


class Mercury:
    def __init__(self):
        self.is_auth = False
        self.client = Vetis(service_url='http://mercury.vetrf.ru/gve')

    def login(self, login: str, password: str, cookies: str = None) -> None:
        if cookies is not None:
            self.client.session.sess.cookies.update(json.loads(cookies))
        else:
            pass

        if not self._check_cookies():
            self.client.auth_by_login(login, password)

        try:
            user_name = self._get_mercury_username()
            print(f'Выполнен вход: {user_name}')
            self.is_auth = True
        except:
            print(f'Не удалось получить данные пользователя, попробуйте снова')
            self.is_auth = False

    def _check_cookies(self):
        return 'Пользователь:' in self.client.session.fetch('https://mercury.vetrf.ru/gve/operatorui').text

    def _get_mercury_username(self) -> str:
        mercury_page = self.client.session.fetch('https://mercury.vetrf.ru/gve/operatorui')
        soup = BeautifulSoup(mercury_page.content, 'html5lib')
        user_name = soup.find("div", {"id": "loggedas"}).find("b").getText().split('(')[0].strip()
        return user_name

    def get_products(self, transaction_pk: str) -> dict:
        page = self.client.session.fetch('https://mercury.vetrf.ru/gve/operatorui',
                                         params={
                                             '_action': 'showTransactionForm',
                                             'transactionPk': transaction_pk,
                                             'pageList': '1',
                                             'cancelAction': 'listTransaction',
                                             'anchor': ''
                                         })
        soup = BeautifulSoup(page.content, 'html5lib')
        all_products = soup.find_all('a')
        created_products = dict()
        for product in all_products:
            product_link = product.get('href')
            if 'listProduced&stateMenu=2' in product_link:
                traffic_pk = product_link.split('&')[1].split('=')[1]
                product_name = product.getText().split('-')[0].strip()
                created_products.update({product_name: traffic_pk})
        return created_products

    def get_products_in_incomplete_transaction(self, transaction_pk: str) -> dict:
        page = self.client.session.fetch('https://mercury.vetrf.ru/gve/operatorui',
                                         params={
                                             '_action': 'listProduceOperationAjax',
                                             'transactionPk': transaction_pk,
                                         })
        soup = BeautifulSoup(page.content, 'html.parser')
        all_products = soup.find_all("tr")
        created_products = dict()
        for product in all_products:
            try:
                traffic_pk = product.find("a").getText()
                product_name = product.find_all('td')[2].getText().strip()
                created_products.update({product_name: traffic_pk})
            except AttributeError:
                continue
        return created_products


manager = Mercury()
