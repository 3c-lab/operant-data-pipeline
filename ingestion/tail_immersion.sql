DROP TABLE IF EXISTS tail_immersion;

CREATE TABLE tail_immersion (
    rfid                                bigint,
    subject                             varchar(255),
    cohort                              integer,
    sex                                 varchar(255),
    experiment_group                    varchar(255),
    drug                                varchar(255),
    tail_immersion_1_time               float,
    tail_immersion_2_time               float,
    tail_immersion_3_time               float,
    tail_immersion_difference_tolerance float,
    tail_immersion_1_date               date,
    tail_immersion_2_date               date,
    tail_immersion_3_date               date,
    constraint tail_immersion_pk
        primary key (rfid, cohort, experiment_group)
)