import json
import re

import requests
from bs4 import BeautifulSoup


def extract(url: str) -> str:
    '''
    Faz a extração dos dados populacionais do ibge, esses dados podem ser acessados de 3 maneiras
        - País
        - Estado
        - Municipio
    Para mais informações sobre esses dados acessar: https://cidades.ibge.gov.br/brasil/panorama

    :param url: Url do sistema a ser extraído
    :return:
    '''
    response = requests.get(url)

    soup = BeautifulSoup(response.text, features="html.parser")

    data = []
    for tr in soup.find('table', {'class': 'lista'}).findAll('tr'):
        value = [text.strip() for text in tr.text.split('\n') if text.strip()]
        if len(value) > 2:
            data.append({'data': value[0], 'year': re.sub('\[|\]','',value[1]), 'value': value[2], 'unit': value[3] if len(value) > 3 else None})

    return json.dumps(data)

if __name__ == '__main__':
    extract('https://cidades.ibge.gov.br/brasil/sp/sao-paulo/panorama')