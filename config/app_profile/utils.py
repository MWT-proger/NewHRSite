def set_if_not_none(mapping, key, value):
    """Сортировочная функция для фильтра"""
    if value is not None:
        mapping[key] = value


def set_if_value(mapping, key, value):
    """Сортировочная функция для фильтра"""
    if value:
        mapping[key] = value


def true_if_not_none(mapping, key, value):
    """Сортировочная функция для фильтра"""
    if value is not None:
        mapping[key] = True
