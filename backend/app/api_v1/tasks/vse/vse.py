
from bs4 import BeautifulSoup
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.api_v1.crud.user_crud import get_active_user
from app.api_v1.schemas.vse_schema import VseParamSchema, TargetVseSchema
from app.api_v1.services.mercury import manager
import xmltodict


def parse_vse_parameters(vse_pk: str) -> list[VseParamSchema]:
    response = manager.client.session.fetch(
        url=f'https://mercury.vetrf.ru/gve/operatorui?_action=listIndex&pk={vse_pk}')
    vse_params = []
    try:
        for item in xmltodict.parse(response.text).get('list').get('element'):
            vse_params.append(VseParamSchema(value=item.get('value'), view=item.get('view')))
    except AttributeError:
        pass
    return vse_params


def parse_target_list():
    response = manager.client.session.fetch(url='https://mercury.vetrf.ru/gve/operatorui?_action=loadTargetList')
    targets = []
    for item in xmltodict.parse(response.text).get('list').get('element'):
        targets.append(TargetVseSchema(value=item.get('value'), view=item.get('view')))
    return targets


def choose_enterprise(enterprise_pk: str):
    manager.client.session.fetch(
        url=f"https://mercury.vetrf.ru/gve/operatorui?enterprisePk={enterprise_pk}&_action=chooseServicedEnterprise")


def add_base_vse(traffic_pk: str, enterprise_pk: str) -> str:
    choose_enterprise(enterprise_pk=enterprise_pk)
    traffic_page = manager.client.session.fetch(
        url=f"https://mercury.vetrf.ru/gve/operatorui?_action=showRealTrafficVUForm&pageList=&stateMenu=2&trafficPk={traffic_pk}")
    soup = BeautifulSoup(traffic_page.content, 'html5lib')
    weight = soup.find('td', class_="label", text="Остаток:").findNext().get_text().split(" ")[0]
    if weight == "0":
        raise ValueError('Остаток продукции равен 0')
    add_vse_page = manager.client.session.fetch(url='https://mercury.vetrf.ru/gve/operatorui', data={
        "weight": weight,
        "quantity": "0",
        "_action": "addExpertise",
        "realTrafficVU.pk": traffic_pk,
        "stateMenu": "2"})
    soup = BeautifulSoup(add_vse_page.content, 'html5lib')
    return soup.find('input', {"name": "pk"}).get('value')


def get_vse_guid(vse_pk: str) -> str:
    add_expertise_form_page = manager.client.session.fetch(
        url=f'https://mercury.vetrf.ru/gve/operatorui?_action=addExpertiseIndexForm&pk={vse_pk}')
    soup = BeautifulSoup(add_expertise_form_page.content, 'html5lib')
    return soup.find('input', {"name": "expertise.guid"}).get('value')


def push_vse(vse_index: str, fact_value: str, conclusion: str, vse_pk: str, vse_guid: str):
    manager.client.session.fetch(url='https://mercury.vetrf.ru/gve/operatorui',
                                 data={
                                     "index.pk": vse_index,
                                     "factValue": fact_value,
                                     "result": 1,
                                     "conclusion": conclusion,
                                     "_action": "addExpertiseIndex",
                                     "expertise.pk": vse_pk,
                                     "expertise.guid": vse_guid
                                 })


def save_vse(target_pk: str, vse_pk: str):
    manager.client.session.fetch(url='https://mercury.vetrf.ru/gve/operatorui',
                                 data={
                                     "expertiseStatus": "1",
                                     "target.pk": target_pk,
                                     "_action": "addConclusion",
                                     "pk": vse_pk
                                 })


def get_vse_products(transaction_pk: str, db: Session):
    user = get_active_user(db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    manager.login(login=user.login,
                  password=user.password,
                  cookies=user.cookies
                  )
    created_products = manager.get_products(transaction_pk=transaction_pk)
    return created_products
