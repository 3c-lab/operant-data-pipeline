DROP TABLE IF EXISTS measurement;

CREATE TABLE measurement (
    rfid VARCHAR(255),
    measurement_name VARCHAR(255),
    measurement_value integer,
    drug_group varchar(255),
    cohort integer,
    measure_number integer,
    date_measured DATE,
    technician VARCHAR(255),
    PRIMARY KEY (rfid, measurement_name, measure_number)
)