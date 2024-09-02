def get_name_for_plot(first_class, second_class, feature, normalized_flag):
    normalized : str = ''
    if normalized_flag:
        normalized = '_normalized'
    return f'./plots/{feature}{normalized}:{get_name_class_for_plot(first_class)}-VS-{get_name_class_for_plot(second_class)}'

def get_name_class_for_plot(class_name : str):
    return '-'.join(class_name.split(' ')).lower()