import importlib


def crawler(event: dict, context: dict):
    ''''
    Faz a extração dos dados externos conforme os parâmetros passados

    :param event: contém os parâmetros que vão ser usados na extração
        - folder: string da pasta do external_data
        - file: arquivo .py da pasta do external_data/folder
        - params: parâmetros da função de extração
    '''

    # Parâmetros da extração
    file = event['file']
    folder = event['folder']

    # Importação da exportação
    f = importlib.import_module(f'external_data.{folder}.{file}')

    # Exportação
    f.extract(event)

if __name__ == '__main__':
    crawler({'name':'selic', 'folder': 'bacen', 'file': 'historic_series', 'params': {'url': 'https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=consultarValores', 'series': 11, 'start_date': '1900-01-01', 'end_date': ''}}, None)