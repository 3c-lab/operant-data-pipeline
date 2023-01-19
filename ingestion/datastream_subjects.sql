DROP TABLE IF EXISTS subject;

CREATE TABLE subject (
    rfid VARCHAR(255) PRIMARY KEY,
    rat VARCHAR(255),
    cohort integer, -- integer
    experiment_group VARCHAR(255),
    drug_group VARCHAR(255),
    sex VARCHAR(255),
    arrival_date DATE,
    age_at_arrival integer, -- integer
    uv varchar(255),
    brevital varchar(255),
    brevital_date DATE,
    brevital_technicians VARCHAR(255), --text[]
    lga_15_date DATE,
    lga_16_date DATE,
    lga_17_date DATE,
    lga_18_date DATE,
    lga_19_date DATE,
    lga_20_date DATE,
    age_at_lga integer,
    long_access_start_date DATE,
    long_access_end_date DATE,
    age_at_sha integer, -- integer
    short_access_start_date DATE,
    short_access_end_date DATE,
    pre_shock_date DATE,
    shock_1_date DATE,
    shock_2_date DATE,
    shock_3_date DATE,
    female_swab_1_technicians VARCHAR(255),
    female_swab_1_date DATE,
    female_swab_1_analysis VARCHAR(255),
    female_swab_2_technicians VARCHAR(255),
    female_swab_2_date DATE,
    female_swab_2_analysis VARCHAR(255),
    female_swab_3_technicians VARCHAR(255),
    female_swab_3_date DATE,
    female_swab_3_analysis VARCHAR(255),
    irritability_1_technicians VARCHAR(255), --text[]
    irritability_1_date DATE,
    irritability_2_technicians VARCHAR(255), --text[]
    irritability_2_date DATE,
    von_frey_1_technicians VARCHAR(255), --text[]
    von_frey_1_date DATE,
    von_frey_2_technicians VARCHAR(255), --text[]
    von_frey_2_date DATE,
    tail_immersion_1_technicians VARCHAR(255), --text[]
    tail_immersion_1_date DATE,
    tail_immersion_2_technicians VARCHAR(255), --text[]
    tail_immersion_2_date DATE,
    tail_immersion_3_technicians VARCHAR(255), --text[]
    tail_immersion_3_date DATE,
    lga_pre_treatment_1_date DATE,
    lga_pre_treatment_2_date DATE,
    lga_pre_treatment_3_date DATE,
    lga_pre_treatment_4_date DATE,
    lga_post_treatment_1_date DATE,
    lga_post_treatment_2_date DATE,
    lga_post_treatment_3_date DATE,
    lga_post_treatment_4_date DATE,
    progressive_ratio_1_date DATE,
    progressive_ratio_2_date DATE,
    progressive_ratio_3_date DATE,
    treatment_1_date DATE,
    treatment_1_group varchar(255),
    treatment_1_start_time time,
    treatment_2_date DATE,
    treatment_2_group varchar(255),
    treatment_2_start_time time,
    treatment_3_date DATE,
    treatment_3_group varchar(255),
    treatment_3_start_time time,
    treatment_4_date DATE,
    treatment_4_group varchar(255),
    treatment_4_start_time time,
    coat_color VARCHAR(255),
    date_of_birth DATE,
    date_of_eye_bleed DATE,
    date_of_ship DATE,
    date_of_wean DATE,
    age_at_dissection integer, -- integer
    dissection_group VARCHAR(255),
    dissection_date DATE,
    ear_punch VARCHAR(255),
    group_pre_shock VARCHAR(255),
    group_shock VARCHAR(255),
    handled_by VARCHAR(255), --text[]
    litter_number integer, -- integer
    litter_size integer, -- integer 
    rack VARCHAR(255),
    recatheter_surgeon VARCHAR(255),
    recatheter_surgery_date DATE,
    shipping_box VARCHAR(255), -- integer
    surgeon VARCHAR(255),
    surgery_assist VARCHAR(255),
    surgery_date DATE,
    age_at_surgery integer, -- integer
    date_of_death DATE,
    days_of_experiment integer, -- integer
    exit_day DATE,
    last_good_session varchar(255),
    exit_code varchar(255),
    complete varchar(255),
    tissue_collected varchar(255),
    exit_notes text,
    replaced_by varchar(255)
)