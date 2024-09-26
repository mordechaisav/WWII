create_table_countries = """
CREATE TABLE countries
(
    country_id   SERIAL PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE NOT NULL
);
"""
create_table_cities = """
create table cities
(
    city_id    SERIAL PRIMARY KEY,
    city_name  VARCHAR(100) UNIQUE NOT NULL,
    country_id int,
    FOREIGN KEY (country_id) REFERENCES countries (country_id),
    unique (city_name,country_id)
);
"""

create_table_locations = """
CREATE TABLE locations
(
    location_id SERIAL PRIMARY KEY,
    city_id     int,
    FOREIGN KEY (city_id) REFERENCES cities (city_id),
    latitude    NUMERIC(10, 6),
    longitude   NUMERIC(10, 6)
);"""

create_table_targets = """
CREATE TABLE targets
(
    target_id       SERIAL PRIMARY KEY,
    target_type     VARCHAR(100),
    target_industry VARCHAR(255),
    target_priority VARCHAR(5),
    location_id     INTEGER,
    FOREIGN KEY (location_id) REFERENCES locations (location_id)
);
"""
create_table_missions = """
CREATE TABLE missions
(
    mission_id                          SERIAL PRIMARY KEY,
    mission_date                        DATE,
    theater_of_operations               VARCHAR(100),
    country                             VARCHAR(100),
    air_force                           VARCHAR(100),
    unit_id                             VARCHAR(100),
    aircraft_series                     VARCHAR(100),
    callsign                            VARCHAR(100),
    mission_type                        VARCHAR(100),
    takeoff_base                        VARCHAR(255),
    takeoff_location                    VARCHAR(255),
    takeoff_latitude                    VARCHAR(15),
    takeoff_longitude                   NUMERIC(10, 6),
    target_id                           INTEGER,
    altitude_hundreds_of_feet           NUMERIC(7, 2),
    airborne_aircraft                   NUMERIC(4, 1),
    attacking_aircraft                  INTEGER,
    bombing_aircraft                    INTEGER,
    aircraft_returned                   INTEGER,
    aircraft_failed                     INTEGER,
    aircraft_damaged                    INTEGER,
    aircraft_lost                       INTEGER,
    high_explosives                     VARCHAR(255),
    high_explosives_type                VARCHAR(255),
    high_explosives_weight_pounds       VARCHAR(25),
    high_explosives_weight_tons         NUMERIC(10, 2),
    incendiary_devices                  VARCHAR(255),
    incendiary_devices_type             VARCHAR(255),
    incendiary_devices_weight_pounds    NUMERIC(10, 2),
    incendiary_devices_weight_tons      NUMERIC(10, 2),
    fragmentation_devices               VARCHAR(255),
    fragmentation_devices_type          VARCHAR(255),
    fragmentation_devices_weight_pounds NUMERIC(10, 2),
    fragmentation_devices_weight_tons   NUMERIC(10, 2),
    total_weight_pounds                 NUMERIC(10, 2),
    total_weight_tons                   NUMERIC(10, 2),
    time_over_target                    VARCHAR(8),
    bomb_damage_assessment              VARCHAR(255),
    source_id                           VARCHAR(100),
    foreign key (target_id) references targets(target_id)
);

"""