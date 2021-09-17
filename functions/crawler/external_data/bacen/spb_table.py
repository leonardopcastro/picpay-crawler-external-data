import json

import requests
from bs4 import BeautifulSoup


def extract(url: str) -> str:
    '''
    Realiza a extração das tabelas estáticas do spb (Sistema de Pagamentos Brasileiro) do banen

    :param url: Url do sistema a ser extraído
    '''
    response = requests.get(url)

    soup = BeautifulSoup(response.text, features="html.parser")

    table = []
    header = None
    for tr in soup.findAll('tr', {'valign': 'top'}):
        if len(tr.findAll('td')) == 4:
            if not header:
                header = [td.text for td in tr.findAll('td')]
            elif header:
                value = [td.text for td in tr.findAll('td')]
                table.append({header[i]:value[i] for i in range(4)})

    return json.dumps(table)

if __name__ == '__main__':
    extract('https://www.bcb.gov.br/pom/spb/estatistica/port/clientesPlanX.asp?frame=1')
    extract('https://www.bcb.gov.br/pom/spb/estatistica/port/str0026_mensal.asp?frame=1')
