	-- - ! - - - - - - | Блок DROP'ов | - - - - - - ! - --
DROP TABLE IF EXISTS SinteringMachine CASCADE;
DROP TABLE IF EXISTS BlastFurnace CASCADE;
DROP TABLE IF EXISTS FlexibleModularFurnace CASCADE;
DROP TABLE IF EXISTS MediumPressureBoiler CASCADE;
-- -- -- -- -- -- -- -- -- -- -- -- --
-- DROP TYPE IF EXISTS;
-- -- -- -- -- -- -- -- -- -- -- -- --
-- DROP INDEX IF EXISTS;
-- -- -- -- -- -- -- -- -- -- -- -- --
-- DROP FUNCTION IF EXISTS;
-- -- -- -- -- -- -- -- -- -- -- -- --
-- DROP TRIGGER IF EXISTS;
-- -- -- -- -- -- -- -- -- -- -- -- --
-- DROP EXTENSION IF EXISTS;
-- -- -- -- -- -- -- -- -- -- -- -- --

	-- - - - - - - - - | Подключение расширений | - - - - - - - - --
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;
	
	-- - - - - - - - - | Создание перечислений | - - - - - - - - --
-- CREATE TYPE as {}
	-- - ! - - - - - - | Создание таблиц (+ Primary Key) | - - - - - - ! - --
CREATE TABLE SinteringMachine ( -- Агломерационная машина
    value_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- может быть вообще не нужна эта колонка? всё равно по registered_value всегда выборку делаем.
    charge_temperature float8 NOT NULL, -- температура шихты (С°)
    speed float8 NOT NULL, -- скорость (м/мин)
    rarefaction float8 NOT NULL, -- разрежение (мм. вод. ст.)
    registered_value timestamp DEFAULT CURRENT_TIMESTAMP -- может быть сделать эту колонку PRIMARY KEY, а value_id убрать?
);
--
CREATE TABLE BlastFurnace ( -- Доменная печь
    value_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- может быть вообще не нужна эта колонка? всё равно по registered_value всегда выборку делаем.
    blast_flow_rate float8 NOT NULL, -- объёмный расход дутья (м³/мин)
    blast_pressure float8 NOT NULL, -- давление дутья (кгс/см²)
    natural_gas_flow_rate float8 NOT NULL, -- объёмный расход природного газа (м³/час)
    registered_value timestamp DEFAULT CURRENT_TIMESTAMP -- может быть сделать эту колонку PRIMARY KEY, а value_id убрать?
);
--
--
CREATE TABLE FlexibleModularFurnace ( -- Гибкая модульная печь
    value_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- может быть вообще не нужна эта колонка? всё равно по registered_value всегда выборку делаем.
    argon_flow_rate float8 NOT NULL, -- объёмный расход аргона (л/мин)
    oxygen_flow_rate float8 NOT NULL, -- объёмный расход кислорода (м³/ч)
    power float8 NOT NULL, -- мощность (кВт/ч)
    registered_value timestamp DEFAULT CURRENT_TIMESTAMP -- может быть сделать эту колонку PRIMARY KEY, а value_id убрать?
);
--
CREATE TABLE MediumPressureBoiler ( -- Паровой котёл среднего давления
    value_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- может быть вообще не нужна эта колонка? всё равно по registered_value всегда выборку делаем.
    temperature float8 NOT NULL, -- температура (С°)
    pressure float8 NOT NULL, -- давление (МПа)
    steam_output float8 NOT NULL, -- выработка пара (т/ч)
    registered_value timestamp DEFAULT CURRENT_TIMESTAMP -- может быть сделать эту колонку PRIMARY KEY, а value_id убрать?
);

	-- - ! - - - - - - | Создание ограничений: Foreign Key, Check | - - - - - - ! - --
-- ALTER TABLE U.. ADD CONSTRAINT FK_U.. FOREIGN KEY (t.._id) REFERENCES T.. (t.._id);
-- -- -- --
-- ALTER TABLE ... ADD CONSTRAINT ... UNIQUE (...);
-- -- -- -- -- -- -- --
/*
ALTER TABLE ...
ADD CONSTRAINT ... -- Проверка маски e-mail и запрещённых символов
CHECK (...);
*/

	-- - ! - - - - - - | Создание функций и хранимых процедур | - - - - - - ! - --
/*
CREATE OR REPLACE FUNCTION ...()
*/

	-- - ! - - - - - - | Создание триггеров | - - - - - - ! - --
/*
CREATE OR REPLACE FUNCTION ...() RETURNS TRIGGER AS $$
BEGIN
  ...
  ...
END;
$$ LANGUAGE plpgsql;
--
CREATE OR REPLACE TRIGGER ...
BEFORE INSERT ON ...
FOR EACH ROW
EXECUTE FUNCTION ...();
*/

	-- - ! - ! - - - - | | | Запросы | | | - - - - ! - ! - --
/*
select
*/