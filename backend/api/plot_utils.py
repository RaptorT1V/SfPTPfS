import pygal
from pygal.style import Style
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.fftpack import fft
import os, logging, random
from datetime import datetime, timedelta


logger = logging.getLogger("plot_utils")
PLOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'graphics')
os.makedirs(PLOT_DIR, exist_ok=True)

# - - - - - - - - - - - Форматирование графиков - - - - - - - - - - - #

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
def generate_title(plot_type, unit, parameter, start_time, end_time):
    start_date = start_time.strftime('%m-%d')
    end_date = end_time.strftime('%m-%d')
    year = start_time.strftime('%Y')

    if start_time.date() == end_time.date():
        time_range = f"с {start_time.strftime('%H:%M:%S')} по {end_time.strftime('%H:%M:%S')}"
        return f"{plot_type} параметра {parameter} в {unit} в течение {start_date} {year} года {time_range}"
    elif (end_time - start_time).days <= 1:
        return f"{plot_type} параметра {parameter} в {unit} с {start_date} по {end_date} {year} года"
    else:
        return f"{plot_type} параметра {parameter} в {unit} с {start_time.strftime('%Y-%m-%d %H:%M:%S')} по {end_time.strftime('%Y-%m-%d %H:%M:%S')}"


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


# Оптимальное деление шкалы OX при крупных метках (шаг)
def adjust_ticks(data_length, max_ticks):
    return max(1, data_length // max_ticks)

# - - - - - - - - - - - Сами графики - - - - - - - - - - - #

  # Линейный график
def plot_linear(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        if isinstance(data[0]['registered_value'], datetime):
            start_time = data[0]['registered_value']
            end_time = data[-1]['registered_value']
        else:
            start_time = datetime.strptime(data[0]['registered_value'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(data[-1]['registered_value'], '%Y-%m-%d %H:%M:%S')

        plot_type = "Линейный график"
        title = generate_title(plot_type, unit, parameter, start_time, end_time)

        custom_style = Style(x_label_rotation=45)
        chart = pygal.Line(style=custom_style, show_minor_x_labels=True, width=1000)
        chart.title = title

        x_labels = [format_time_label(item['registered_value'], start_time, end_time) for item in data]
        max_ticks = determine_max_ticks(start_time, end_time)
        major_step = adjust_ticks(len(x_labels), max_ticks)

        chart.x_labels_major = x_labels[::major_step]
        chart.x_labels = x_labels

        chart.add(parameter, [item[parameter] for item in data])

        filepath = os.path.join(PLOT_DIR, f"{plot_type}_{unit}_{parameter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        chart.render_to_file(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения линейного графика: {e}")
        raise


  # График спектра (FFT)
def plot_spectrum(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        values = [item[parameter] for item in data]
        spectrum = np.abs(fft(values))
        frequencies = np.fft.fftfreq(len(values), d=1.043)  # Чтобы определить d, см. частоту добавления записей в БД

        plot_type = "График спектра"
        custom_style = Style(x_label_rotation=45)
        chart = pygal.Line(style=custom_style, width=1000)
        chart.title = generate_title(plot_type, unit, parameter, data[0]['registered_value'], data[-1]['registered_value'])

        chart.x_labels = [f"{freq:.2f}" for freq in frequencies[:len(frequencies)//2]]
        chart.add(parameter, spectrum[:len(spectrum)//2])

        filepath = os.path.join(PLOT_DIR, f"{plot_type}_{unit}_{parameter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        chart.render_to_file(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения графика спектра: {e}")
        raise


  # Гистограмма распределения значений
def plot_histogram(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        values = [item[parameter] for item in data]

        plot_type = "Гистограмма распределения значений"
        custom_style = Style()
        chart = pygal.Histogram(style=custom_style, width=1000)

        chart.title = generate_title(plot_type, unit, parameter, data[0]['registered_value'], data[-1]['registered_value'])

        bins = np.histogram_bin_edges(values, bins='auto')
        histogram, bin_edges = np.histogram(values, bins=bins)
        chart.add(parameter, [(count, float(bin_edges[i]), float(bin_edges[i + 1])) for i, count in enumerate(histogram)])

        filepath = os.path.join(PLOT_DIR, f"{plot_type}_{unit}_{parameter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        chart.render_to_file(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения гистограммы распределения значений: {e}")
        raise


  # График производной
def plot_derivative(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        values = [item[parameter] for item in data]
        derivative = np.gradient(values)

        plot_type = "График производной"
        custom_style = Style(x_label_rotation=45)
        chart = pygal.Line(style=custom_style, width=1000)
        chart.title = generate_title(plot_type, unit, parameter, data[0]['registered_value'], data[-1]['registered_value'])

        x_labels = [format_time_label(item['registered_value'], data[0]['registered_value'], data[-1]['registered_value']) for item in data]
        chart.x_labels = x_labels
        chart.add(f"Производная {parameter}", derivative)

        filepath = os.path.join(PLOT_DIR, f"{plot_type}_{unit}_{parameter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        chart.render_to_file(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения графика производной: {e}")
        raise


  # Скользящее среднее (пока не является доп. опцией к линейному графику)
def plot_moving_average(data, parameters: list, unit: str, parameter: str, window=5, format="svg"):
    try:
        values = [item[parameter] for item in data]
        moving_avg = np.convolve(values, np.ones(window)/window, mode='valid')

        plot_type = "Скользящее среднее"
        custom_style = Style(x_label_rotation=45)
        chart = pygal.Line(style=custom_style, width=1000)
        chart.title = generate_title(plot_type, unit, parameter, data[0]['registered_value'], data[-1]['registered_value'])

        x_labels = [format_time_label(data[i]['registered_value'], data[0]['registered_value'], data[-1]['registered_value']) for i in range(len(moving_avg))]
        chart.x_labels = x_labels
        chart.add(f"Скользящее среднее {parameter}", moving_avg)

        filepath = os.path.join(PLOT_DIR, f"{plot_type}_{unit}_{parameter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        chart.render_to_file(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения скользящего среднего: {e}")
        raise


  # Линия тренда (пока не является доп. опцией к линейному графику)
def plot_trend_line(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        values = [item[parameter] for item in data]

        trend_type = random.choice(['linear', 'exponential'])
        if trend_type == 'linear':
            slope, intercept = np.polyfit(range(len(values)), values, 1)
            trend_line = [slope * x + intercept for x in range(len(values))]
        else:  # exponential
            trend_line = [values[0] * (1.05 ** i) for i in range(len(values))]

        plot_type = f"Линия тренда ({trend_type.capitalize()})"
        custom_style = Style(x_label_rotation=45)
        chart = pygal.Line(style=custom_style, width=1000)
        chart.title = generate_title(plot_type, unit, parameter, data[0]['registered_value'], data[-1]['registered_value'])

        x_labels = [format_time_label(item['registered_value'], data[0]['registered_value'], data[-1]['registered_value']) for item in data]
        chart.x_labels = x_labels
        chart.add(f"{trend_type} Линия тренда {parameter}", trend_line)

        filepath = os.path.join(PLOT_DIR, f"{plot_type}_{unit}_{parameter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}")
        chart.render_to_file(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения {trend_type} линии тренда: {e}")
        raise


  # Карта тепловых зон (пока не для нескольких параметров)
def plot_heatmap(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        if not data:
            raise ValueError("Пустой набор данных для построения тепловой карты.")

        df = pd.DataFrame(data)
        pivoted = df.pivot_table(index='registered_value', values=parameter)

        plt.figure(figsize=(12, 6))
        sns.heatmap(pivoted.T, cmap="YlGnBu", cbar_kws={'label': parameter})

        plot_type = "Карта тепловых зон"
        title = generate_title(plot_type, unit, parameter, data[0]['registered_value'], data[-1]['registered_value'])
        plt.title(title)

        filepath = os.path.join(PLOT_DIR, f"heatmap_seaborn_{unit}_{parameter}.svg")
        plt.savefig(filepath, format="svg")
        plt.close()
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения тепловой карты: {e}")
        raise


  # Диаграмма рассеяния (пока не для нескольких параметров)
def plot_scatter(data, parameters: list, unit: str, parameter: str, format="svg"):
    try:
        if not data:
            raise ValueError("Пустой набор данных для построения диаграммы рассеяния.")

        df = pd.DataFrame(data)
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x="registered_value", y=parameter, data=df)

        plot_type = "Диаграмма рассеяния"
        title = generate_title(plot_type, unit, parameter, data[0]['registered_value'], data[-1]['registered_value'])
        plt.title(title)

        filepath = os.path.join(PLOT_DIR, f"scatter_seaborn_{unit}_{parameter}.svg")
        plt.savefig(filepath, format="svg")
        plt.close()
        return filepath
    except Exception as e:
        logger.error(f"Ошибка построения диаграммы рассеяния: {e}")
        raise