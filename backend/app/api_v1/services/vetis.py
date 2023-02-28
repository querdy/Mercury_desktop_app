from bs4 import BeautifulSoup

from app.api_v1.services.base_session import BaseSession


class Vetis:
    def __init__(self, service_url: str):
        self.URL = service_url
        self.session = BaseSession()

    def auth_by_login(self, login: str, password: str) -> bool:
        page = self.session.fetch(self.URL)
        soup = BeautifulSoup(page.content, 'html5lib')
        form = soup.find('form')
        fields = form.findAll('input')
        form_data = dict((field.get('name'), field.get('value')) for field in fields if field.get('name') is not None)
        page = self.session.fetch(form['action'], data=form_data)
        if page.history:
            form_data['j_username'] = login
            form_data['j_password'] = password
            form_data['_eventId_proceed'] = ''
            form_data['ksid'] = 'sasat'
            soup = BeautifulSoup(page.content, 'html5lib')
            form = soup.find('form')
            page = self.session.fetch(page.history[0].headers['Location'], data=form_data)
            soup = BeautifulSoup(page.content, 'html5lib')
            form = soup.find('form')
            fields = form.findAll('input')
            temp_data = dict((field.get('name'), field.get('value')) for field in fields if field.get('name') is not None)
            try:
                form_data['SAMLResponse'] = temp_data['SAMLResponse']
                del form_data['SAMLRequest']
            except KeyError:
                print('неудачная авторизация, проверить верность логина и пароля')
                return False
            try:
                self.session.fetch(form['action'], data=form_data)
            except:
                print('неудачная авторизация, ...')
                return False
            return True



