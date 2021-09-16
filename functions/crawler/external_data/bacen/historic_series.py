import json
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from utils.utils import convert_date


def str_to_float(text: str) -> Optional[float]:
    '''
    Função para converter de str em float

    :param text: string a ser convertido
    '''
    try:
        return float(text.replace('.', '').replace(',', '.'))
    except Exception:
        return None

def extract(url: str, series: int, start_date: str, end_date: str) -> str:
    ''''
    Função para extração de séries temporais do bacen


    :param url: Url do sistema a ser extraído
    :param series: indice da série segundo o site do bacen
    :param start_date: Data inicial da série
    :param end_date: Data final da série
    '''

    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    form_data = {
        'optSelecionaSerie': series,
        'dataInicio': convert_date(start_date, '%d/%m/%Y'),
        'dataFim': convert_date(end_date, '%d/%m/%Y'),
        'selTipoArqDownload': 2,
        'chkPaginar': 'on',
        'hdOidSeriesSelecionadas': series,
        'hdPaginar': 'false',
        'bilServico': '[SGSFW2301]'
    }

    response = requests.post(url, data=form_data)

    soup = BeautifulSoup(response.text, features="html.parser")

    try:
        unit = soup.findAll('tr', {'class': 'fundoPadraoAClaro1'})[2].findAll(True, {'class': 'textoPequeno'})[-1].text
        unit = unit.strip().split('\n')[-1].strip()
    except:
        unit = None

    soup_tr = soup.findAll('tr',{'class':['fundoPadraoAClaro2','fundoPadraoAClaro3']})

    series = []
    for tr in soup_tr:
        data = tr.findAll(True, {'class': 'textoPequeno'})
        value = str_to_float(data[1].text.strip()) if len(data) > 1 else None
        if value:
            series.append({'date': data[0].text.strip(), 'value': value, 'unit': unit})

    return json.dumps(series)