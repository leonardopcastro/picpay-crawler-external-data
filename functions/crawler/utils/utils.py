from datetime import datetime


def convert_date(date: str, date_format: str) -> str:
    '''
    Converte a formatação de uma data

    :param date: data a ser formatada
    :param date_format: formata a data (seguir padrão do datetime)
    '''
    return datetime.strptime(date, '%Y-%m-%d').strftime(date_format)