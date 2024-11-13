import pygal
from pygal.style import Style
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("plot_utils")

PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'graphics')
os.makedirs(PLOT_DIR, exist_ok=True)


# Форматирование единиц времени на оси OX в зависимости от условий
def format_time_label(registered_time, start_time, end_time):
    time_span = end_time - start_time

    if time_span <= timedelta(minutes=1):
        return registered_time.strftime('%S')  # Секунды
    elif time_span <= timedelta(hours=1):
        return registered_time.strftime('%M:%S')  # Минуты:Секунды
    elif time_span <= timedelta(days=1):
        return registered_time.strftime('%H:%M')  # Часы:Минуты
    else:
        return registered_time.strftime('%m-%d %H:%M')  # Месяц-День Часы:Минуты


# Генерация названия графика в зависимости от условий
def generate_title(unit, parameter, start_time, end_time):
    start_date = start_time.strftime('%m-%d')
    end_date = end_time.strftime('%m-%d')
    year = start_time.strftime('%Y')

    if start_time.date() == end_time.date():
        time_range = f"с {start_time.strftime('%H:%M:%S')} по {end_time.strftime('%H:%M:%S')}"
        return f"График параметра {parameter} в {unit} в течение {start_date} {year} года {time_range}"
    elif (end_time - start_time).days <= 1:
        return f"График параметра {parameter} в {unit} с {start_date} по {end_date} {year} года"
    else:
        return f"График параметра {parameter} в {unit} с {start_time.strftime('%Y-%m-%d %H:%M:%S')} по {end_time.strftime('%Y-%m-%d %H:%M:%S')}"


# Определение макс. кол-ва делений в зависимости от единиц времени
def determine_max_ticks(start_time, end_time):
    time_span = end_time - start_time
    if time_span <= timedelta(minutes=1):
        return 20  # Для секунд
    elif time_span <= timedelta(hours=1):
        return 12  # Для минут
    elif time_span <= timedelta(days=1):
        return 10  # Для часов
    else:
        return 8  # Для дней


# Оптимальное деление шкалы OX при крупных метках
def adjust_ticks(data_length, max_ticks):
    return max(1, data_length // max_ticks)


# Построение графика
def plot_graph(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        if isinstance(data[0]['registered_value'], datetime):
            start_time = data[0]['registered_value']
            end_time = data[-1]['registered_value']
        else:
            start_time = datetime.strptime(data[0]['registered_value'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(data[-1]['registered_value'], '%Y-%m-%d %H:%M:%S')

        title = generate_title(unit, parameter, start_time, end_time)

        custom_style = Style(x_label_rotation=45)
        chart = pygal.Line(style=custom_style, show_minor_x_labels=True, width=1000)
        chart.title = title

        x_labels = [format_time_label(item['registered_value'], start_time, end_time) for item in data]
        max_ticks = determine_max_ticks(start_time, end_time)

        major_step = adjust_ticks(len(x_labels), max_ticks)

        chart.x_labels_major = x_labels[::major_step]
        chart.x_labels = x_labels

        chart.add(parameter, [item[parameter] for item in data])

        filepath = os.path.join(PLOT_DIR, f"{unit}_{parameter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        chart.render_to_file(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения графика: {e}")
        raise