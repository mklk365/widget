

def filter_by_state(list_dict, state='EXECUTED'):
    '''Функция принимает список словарей и опционально значение для ключа'''
    select_dict = []
    for i in list_dict:
      if i['state'] == 'EXECUTED':
        select_dict.append(i)
    return select_dict


def sort_by_date():
    '''Функция принимает список словарей и необязательный параметр, задающий порядок сортировки'''
    pass
