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

    charge_temperature = 60  # температура шихты (С°)
    speed = 5.5  # скорость (м/мин)
    rarefaction = 200  # разрежение (мм. вод. ст.)

    while not stop_signal:
        charge_temperature += random.uniform(-1.0, 4.0)
        speed += random.uniform(-0.1, 0.4)
        rarefaction += random.uniform(-10, 30)

        cursor.execute("""
            INSERT INTO sinteringMachine (charge_temperature, speed, rarefaction)
            VALUES (%s, %s, %s);
        """, (charge_temperature, speed, rarefaction))

        conn.commit()
        sleep(1.5)


# – Доменная печь –
def generate_blast_furnace_data(conn):
    cursor = conn.cursor()

    blast_flow_rate = 1000  # объёмный расход дутья (м³/мин)
    blast_pressure = 3  # давление дутья (кгс/см²)
    natural_gas_flow_rate = 5000  # объёмный расход природного газа (м³/час)

    while not stop_signal:
        blast_flow_rate += random.uniform(-100, 400)
        blast_pressure += random.uniform(-0.1, 0.4)
        natural_gas_flow_rate += random.uniform(-300, 1500)

        cursor.execute("""
            INSERT INTO blastFurnace (blast_flow_rate, blast_pressure, natural_gas_flow_rate)
            VALUES (%s, %s, %s);
        """, (blast_flow_rate, blast_pressure, natural_gas_flow_rate))

        conn.commit()
        sleep(1.5)


# – Гибкая модульная печь –
def generate_flexible_modular_furnace_data(conn):
    cursor = conn.cursor()

    argon_flow_rate = 500  # объёмный расход аргона (л/мин)
    oxygen_flow_rate = 1000  # объёмный расход кислорода (м³/ч)
    power = 20000  # мощность (кВт/ч)

    while not stop_signal:
        argon_flow_rate += random.uniform(-20, 100)
        oxygen_flow_rate += random.uniform(-50, 500)
        power += random.uniform(-1000, 3000)

        cursor.execute("""
            INSERT INTO flexibleModularFurnace (argon_flow_rate, oxygen_flow_rate, power)
            VALUES (%s, %s, %s);
        """, (argon_flow_rate, oxygen_flow_rate, power))

        conn.commit()
        sleep(1.5)


# – Паровой котёл среднего давления –
def generate_medium_pressure_boiler_data(conn):
    cursor = conn.cursor()

    temperature = 100  # температура (С°)
    pressure = 3.5  # давление (МПа)
    steam_output = 50  # выработка пара (т/ч)

    while not stop_signal:
        temperature += random.uniform(-5, 20)
        pressure += random.uniform(-0.2, 1)
        steam_output += random.uniform(-3, 15)

        cursor.execute("""
            INSERT INTO mediumPressureBoiler (temperature, pressure, steam_output)
            VALUES (%s, %s, %s);
        """, (temperature, pressure, steam_output))

        conn.commit()
        sleep(1.5)


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
