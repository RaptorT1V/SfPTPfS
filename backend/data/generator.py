import psycopg2
from time import sleep
import random
import threading
from backend.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

stop_signal = False


def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn


# – Агломерационная машина –
def generate_sintering_machine_data(conn):
    cursor = conn.cursor()

    charge_temperature = 20  # температура шихты (С°)
    speed = 2.3  # скорость (м/мин)
    rarefaction = 190  # разрежение (мм. вод. ст.)

    while not stop_signal:
        charge_temperature += random.uniform(-1.0, 1.125)
        speed += random.uniform(-0.1, 0.1125)
        rarefaction += random.uniform(-10, 11.25)

        cursor.execute("""
            INSERT INTO sinteringMachine (charge_temperature, speed, rarefaction)
            VALUES (%s, %s, %s);
        """, (charge_temperature, speed, rarefaction))

        conn.commit()
        sleep(1)


# – Доменная печь –
def generate_blast_furnace_data(conn):
    cursor = conn.cursor()

    blast_flow_rate = 2100  # объёмный расход дутья (м³/мин)
    blast_pressure = 2.5  # давление дутья (кгс/см²)
    natural_gas_flow_rate = 5800  # объёмный расход природного газа (м³/час)

    while not stop_signal:
        blast_flow_rate += random.uniform(-100, 112.5)
        blast_pressure += random.uniform(-0.1, 0.1125)
        natural_gas_flow_rate += random.uniform(-300, 337.5)

        cursor.execute("""
            INSERT INTO blastFurnace (blast_flow_rate, blast_pressure, natural_gas_flow_rate)
            VALUES (%s, %s, %s);
        """, (blast_flow_rate, blast_pressure, natural_gas_flow_rate))

        conn.commit()
        sleep(1)


# – Гибкая модульная печь –
def generate_flexible_modular_furnace_data(conn):
    cursor = conn.cursor()

    argon_flow_rate = 555  # объёмный расход аргона (л/мин)
    oxygen_flow_rate = 999  # объёмный расход кислорода (м³/ч)
    power = 17123  # мощность (кВт/ч)

    while not stop_signal:
        argon_flow_rate += random.uniform(-20, 22.5)
        oxygen_flow_rate += random.uniform(-50, 62.5)
        power += random.uniform(-1000, 1125)

        cursor.execute("""
            INSERT INTO flexibleModularFurnace (argon_flow_rate, oxygen_flow_rate, power)
            VALUES (%s, %s, %s);
        """, (argon_flow_rate, oxygen_flow_rate, power))

        conn.commit()
        sleep(1)


# – Паровой котёл среднего давления –
def generate_medium_pressure_boiler_data(conn):
    cursor = conn.cursor()

    temperature = 100  # температура (С°)
    pressure = 3.9  # давление (МПа)
    steam_output = 54  # выработка пара (т/ч)

    while not stop_signal:
        temperature += random.uniform(-5, 6.25)
        pressure += random.uniform(-0.2, 0.125)
        steam_output += random.uniform(-3, 3.375)

        cursor.execute("""
            INSERT INTO mediumPressureBoiler (temperature, pressure, steam_output)
            VALUES (%s, %s, %s);
        """, (temperature, pressure, steam_output))

        conn.commit()
        sleep(1)


def main():
    global stop_signal
    stop_signal = False
    conn = connect_db()
    threads = [
        threading.Thread(target=generate_sintering_machine_data, args=(conn,)),
        threading.Thread(target=generate_blast_furnace_data, args=(conn,)),
        threading.Thread(target=generate_flexible_modular_furnace_data, args=(conn,)),
        threading.Thread(target=generate_medium_pressure_boiler_data, args=(conn,)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def stop_generator():
    global stop_signal
    stop_signal = True
