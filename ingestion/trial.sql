DROP TABLE IF EXISTS trial_lga;
DROP TABLE IF EXISTS trial_sha;
DROP TABLE IF EXISTS trial_pr;
DROP TABLE IF EXISTS trial_shock;
DROP TABLE IF EXISTS trial_note;

-- LGA for both COC and OXY (19 columns)
create table trial_lga
(
    rfid                   bigint,
    subject                varchar(255),
    room                   varchar(255),
    cohort                 integer,
    trial_id               varchar(255),
    drug                   varchar(255),
    box                    integer,
    start_time             time,
    end_time               time,
    start_date             date,
    end_date               date,
    active_lever_presses   integer,
    inactive_lever_presses integer,
    reward_presses         integer,
    timeout_presses        integer,
    active_timestamps      text,
    inactive_timestamps    text,
    reward_timestamps      text,
    timeout_timestamps     text,
    constraint trial_lga_pk
        primary key (rfid, trial_id, drug)
);

-- SHA for both COC and OXY (19 columns)
create table trial_sha
(
    rfid                   bigint,
    subject                varchar(255),
    room                   varchar(255),
    cohort                 integer,
    trial_id               varchar(255),
    drug                   varchar(255),
    box                    integer,
    start_time             time,
    end_time               time,
    start_date             date,
    end_date               date,
    active_lever_presses   integer,
    inactive_lever_presses integer,
    reward_presses         integer,
    timeout_presses        integer,
    active_timestamps      text,
    inactive_timestamps    text,
    reward_timestamps      text,
    timeout_timestamps     text,
    constraint trial_sha_pk
        primary key (rfid, trial_id, drug, start_time)
);

-- PR for both COC and OXY (17 columns)
CREATE TABLE trial_pr (
    rfid                   bigint,
    subject                varchar(255),
    room                   varchar(255),
    cohort                 integer,
    trial_id               varchar(255),
    drug                   varchar(255),
    box                    integer,
    start_time             time,
    end_time               time,
    start_date             date,
    end_date               date,
    last_ratio             integer,
    breakpoint             integer,
    active_lever_presses   integer,
    inactive_lever_presses integer,
    reward_presses         integer,
    reward_timestamps      text,
    constraint trial_pr_pk
        primary key (rfid, trial_id, drug)
)

-- SHOCK for COC only (18 columns)
CREATE TABLE trial_shock (
    rfid                         varchar(255),
    subject                      varchar(255),
    room                         varchar(255),
    cohort                       integer,
    trial_id                     varchar(255),
    drug                         varchar(255),
    box                          integer,
    start_time                   time,
    end_time                     time,
    start_date                   date,
    end_date                     date,
    total_active_lever_presses   integer,
    total_inactive_lever_presses integer,
    total_shocks                 integer,
    total_reward                 integer,
    rewards_after_first_shock    integer,
    rewards_got_shock            text,
    reward_timestamps            text,
    constraint trial_shock_pk
        primary key (rfid, trial_id, drug, start_time)
)

-- NOTE for all daily issues of COCAINE and OXYCODONE
CREATE TABLE trial_note (
    rfid                 bigint,
    subject              varchar(255),
    cohort               integer,
    sex                  varchar(255),
    drug                 varchar(255),
    experiment_group     varchar(255),
    trial_id             varchar(255),
    start_date           date,
    code                 varchar(255),
    to_do                varchar(255),
    note                 text
)