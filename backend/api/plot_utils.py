import pygal
import os
import logging
from datetime import datetime

logger = logging.getLogger("plot_utils")

# Базовый путь для сохранения графиков
PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'graphics')

# Создаем папку, если её нет
os.makedirs(PLOT_DIR, exist_ok=True)

def plot_graph(data, parameters: list, unit: str, parameter: str, format="svg"):
    """
    Построение графика.
    :param data: Список данных для графика.
    :param parameters: Список параметров.
    :param unit: Агрегат.
    :param parameter: Название параметра.
    :param format: Формат графика (по умолчанию svg).
    """
    try:
        # Генерация названия файла
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{unit}_{parameter}_{date_str}.{format}"
        filepath = os.path.join(PLOT_DIR, filename)

        logger.info(f"Создаём график: {filepath}")

        # Построение графика с Pygal
        chart = pygal.Line()
        chart.title = f"{unit}: {parameter} over time"
        chart.x_labels = [str(item['registered_value']) for item in data]
        chart.add(parameter, [item[parameter] for item in data])

        # Сохранение в указанном формате
        chart.render_to_file(filepath)

        logger.info(f"График сохранён в {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"Ошибка построения графика: {e}")
        raise