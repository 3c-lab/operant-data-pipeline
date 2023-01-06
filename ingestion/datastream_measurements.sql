DROP TABLE IF EXISTS measurement;

CREATE TABLE measurement (
    rfid integer PRIMARY KEY,
    measurement_name VARCHAR(255) PRIMARY KEY,
    measurement_value integer,
    group varchar(255),
    measure_number integer PRIMARY KEY,
    date_measured DATE,
    technician text[]
)