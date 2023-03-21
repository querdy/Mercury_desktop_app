from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

from app.api_v1.crud.research_crud import get_enterprise
from app.api_v1.crud.transaction_crud import save_transaction, save_traffic
from app.api_v1.crud.user_crud import get_active_user
from app.api_v1.models import validate_research
from app.api_v1.schemas.transaction_schema import TrafficMsgSchema, TransactionMsgSchema
from app.api_v1.services.mercury import manager


def get_traffics(transaction_pk: int, enterprise_uuid: int, db: Session):
    user = get_active_user(db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    manager.login(login=user.login,
                  password=user.password,
                  cookies=user.cookies
                  )

    try:
        save_transaction(db=db, transaction=transaction_pk)
    except HTTPException:
        pass

    enterprise = get_enterprise(db=db, enterprise_uuid=enterprise_uuid)
    main_researches = []
    for research in enterprise.researches:
        if research.product == 'main':
            main_researches.append(research)

    created_products = manager.get_products(transaction_pk=str(transaction_pk))
    if not created_products:
        created_products = manager.get_products_in_incomplete_transaction(transaction_pk=transaction_pk)

    traffics = []
    for traffic in created_products:
        traffics.append(jsonable_encoder(TrafficMsgSchema(traffic=created_products.get(traffic),
                                                          product_name=traffic,
                                                          status='try')))
    return TransactionMsgSchema(transaction_pk=transaction_pk, traffics=traffics)


def push_research(enterprise_uuid: int, transaction_pk: int, traffic: int, product: str, db: Session):
    test_url = 'https://mercury.vetrf.ru/gve/operatorui?_action=addLaboratory&_language=ru&trafficPk='
    if manager.client.session.fetch(f'{test_url}{traffic}').status_code == 500:
        return TrafficMsgSchema(traffic=traffic, product_name=product, status='inactive')
    try:
        save_traffic(db=db, transaction=transaction_pk, traffic=traffic)
    except HTTPException:
        return TrafficMsgSchema(traffic=traffic, product_name=product, status='already')
    enterprise = get_enterprise(db=db, enterprise_uuid=enterprise_uuid)
    main_researches = []
    is_added = False
    for research in enterprise.researches:
        if research.product == 'main':
            main_researches.append(research)
        if research.product == product:
            is_added = True
            if validate_research(research=research):
                manager.client.session.fetch('https://mercury.vetrf.ru/gve/operatorui', data={
                    'actNumber': '',
                    'actDate': '',
                    'laboratory': research.laboratory,
                    'disease': research.disease,
                    'researchDate': research.date_of_research,
                    'method': research.method,
                    'expertiseNumber': research.expertise_id,
                    'result': research.result,
                    'conclusion': research.conclusion,
                    '_action': 'addLaboratoryForm',
                    'realTrafficVUPk': traffic
                })
            else:
                TrafficMsgSchema(traffic=traffic, product_name=product, status='Skipped')
    if is_added:
        return TrafficMsgSchema(traffic=traffic, product_name=product, status='Ok! ~special')
    else:
        for main_research in main_researches:
            if validate_research(research=main_research):
                manager.client.session.fetch('https://mercury.vetrf.ru/gve/operatorui', data={
                    'actNumber': '',
                    'actDate': '',
                    'laboratory': main_research.laboratory,
                    'disease': main_research.disease,
                    'researchDate': main_research.date_of_research,
                    'method': main_research.method,
                    'expertiseNumber': main_research.expertise_id,
                    'result': main_research.result,
                    'conclusion': main_research.conclusion,
                    '_action': 'addLaboratoryForm',
                    'realTrafficVUPk': traffic
                })
            else:
                return TrafficMsgSchema(traffic=traffic, product_name=product, status='Skipped')
        return TrafficMsgSchema(traffic=traffic, product_name=product, status='Ok! ~base')
