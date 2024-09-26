from db import get_db_connection
from services.queries import (
    create_table_countries,
    create_table_cities,
    create_table_locations,
    create_table_targets,
    create_table_missions
)
import psycopg2


def normalize_db():
    source_conn = get_db_connection()
    target_conn = psycopg2.connect(
        dbname="normal_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

    # Create target tables
    with target_conn.cursor() as cur:
        cur.execute(create_table_countries)
        cur.execute(create_table_cities)
        cur.execute(create_table_locations)
        cur.execute(create_table_targets)
        cur.execute(create_table_missions)
        target_conn.commit()
    print("Build db created")

    # פתיחת cursor לטיפול בטבלה המקורית
    s_cur = source_conn.cursor()
    s_cur.execute("SELECT * FROM mission")

    # פתיחת cursor עבור פעולות ההכנסה למסד הנתונים
    cur = target_conn.cursor()

    while True:
        row = s_cur.fetchone()
        if row is None:
            print("No more rows to process.")
            break

        print(f"Processing row: {row}")
        # הוספת מדינה אם היא לא קיימת
        country_name = row[14]
        print(f"Country name: {country_name}")

        if country_name is None:
            print("Warning: Country name is None, skipping this row.")
            continue  # להמשיך אם אין שם מדינה

        # בדוק אם המדינה קיימת
        cur.execute("SELECT country_id FROM countries WHERE country_name = %s", (country_name,))
        result = cur.fetchone()

        if result is None:
            # אם המדינה לא קיימת, הוסף אותה
            cur.execute("INSERT INTO countries (country_name) VALUES (%s) RETURNING country_id", (country_name,))
            country_id = cur.fetchone()[0]  # קבל את ה-country_id החדש
            print(f"Inserted new country with ID: {country_id}")
        else:
            # אם המדינה קיימת, קבל את ה-country_id
            country_id = result[0]
            print(f"Found existing country with ID: {country_id}")
        target_conn.commit()
        # הוספת עיר אם היא לא קיימת
        city_name = row[15]
        print(f"City name: {city_name}")

        if city_name is None:
            print("Warning: City name is None, skipping this row.")
            continue  # להמשיך אם אין שם עיר

        # בדוק אם העיר קיימת
        cur.execute("SELECT city_id FROM cities WHERE city_name = %s", (city_name,))
        result = cur.fetchone()

        if result is None:
            # אם העיר לא קיימת, הוסף אותה
            cur.execute("INSERT INTO cities (city_name, country_id) VALUES (%s, %s) RETURNING city_id",
                        (city_name, country_id))
            city_id = cur.fetchone()[0]  # קבל את ה-city_id החדש
            print(f"Inserted new city with ID: {city_id}")
        else:
            # אם העיר קיימת, קבל את ה-city_id
            city_id = result[0]
            print(f"Found existing city with ID: {city_id}")

        if city_id is not None:
            print(f"City ID is valid: {city_id}")
        else:
            print(f"City not found: {city_name} in country_id {country_id}")
            continue  # או לעבור לשלב הבא של הלולאה
        target_conn.commit()
        # הוספת מיקום
        latitude = row[19]
        longitude = row[20]
        print(f"Inserting location with latitude: {latitude}, longitude: {longitude}")
        cur.execute("INSERT INTO locations (city_id, latitude, longitude) VALUES (%s, %s, %s) RETURNING location_id",
                    (city_id, latitude, longitude))
        location_id = cur.fetchone()[0]
        print(f"Inserted location with ID: {location_id}")

        # הוספת יעד
        target_type = row[16]
        target_industry = row[17]
        target_priority = row[18]
        print(f"Inserting target with type: {target_type}, industry: {target_industry}, priority: {target_priority}")
        cur.execute(
            "INSERT INTO targets (target_type, target_industry, target_priority, location_id) VALUES (%s, %s, %s, %s) RETURNING target_id",
            (target_type, target_industry, target_priority, location_id))
        target_id = cur.fetchone()[0]
        print(f"Inserted target with ID: {target_id}")
        target_conn.commit()
        # הוספת משימה
        mission_date = row[1]
        theater_of_operations = row[2]
        country = row[3]
        air_force = row[4]
        unit_id = row[5]
        aircraft_series = row[6]
        callsign = row[7]
        mission_type = row[8]
        takeoff_base = row[9]
        takeoff_location = row[10]
        takeoff_latitude = row[11]
        takeoff_longitude = row[12]

        altitude_hundreds_of_feet = row[21]
        airborne_aircraft = row[22]
        attacking_aircraft = row[23]
        bombing_aircraft = row[24]
        aircraft_returned = row[25]
        aircraft_failed = row[26]
        aircraft_damaged = row[27]
        aircraft_lost = row[28]
        high_explosives = row[29]
        high_explosives_type = row[30]
        high_explosives_weight_pounds = row[31]
        high_explosives_weight_tons = row[32]
        incendiary_devices = row[33]
        incendiary_devices_type = row[34]
        incendiary_devices_weight_pounds = row[35]
        incendiary_devices_weight_tons = row[36]
        fragmentation_devices = row[37]
        fragmentation_devices_type = row[38]
        fragmentation_devices_weight_pounds = row[39]
        fragmentation_devices_weight_tons = row[40]
        total_weight_pounds = row[41]
        total_weight_tons = row[42]
        time_over_target = row[43]
        bomb_damage_assessment = row[44]
        source_id = row[45]

        print(f"Inserting mission with date: {mission_date}, theater: {theater_of_operations}")
        cur.execute(
            "INSERT INTO missions (mission_date, theater_of_operations,country, air_force, unit_id, aircraft_series, callsign, "
            "mission_type, takeoff_base, takeoff_location, takeoff_latitude, takeoff_longitude, altitude_hundreds_of_feet, "
            "airborne_aircraft, attacking_aircraft, bombing_aircraft, aircraft_returned, aircraft_failed, aircraft_damaged, "
            "aircraft_lost, high_explosives, high_explosives_type, high_explosives_weight_pounds, high_explosives_weight_tons, "
            "incendiary_devices, incendiary_devices_type, incendiary_devices_weight_pounds, incendiary_devices_weight_tons, "
            "fragmentation_devices, fragmentation_devices_type, fragmentation_devices_weight_pounds, fragmentation_devices_weight_tons, "
            "total_weight_pounds, total_weight_tons, time_over_target, bomb_damage_assessment, source_id, target_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (mission_date, theater_of_operations,country, air_force, unit_id, aircraft_series, callsign, mission_type,
             takeoff_base,
             takeoff_location, takeoff_latitude, takeoff_longitude, altitude_hundreds_of_feet, airborne_aircraft,
             attacking_aircraft, bombing_aircraft, aircraft_returned, aircraft_failed, aircraft_damaged, aircraft_lost,
             high_explosives, high_explosives_type, high_explosives_weight_pounds, high_explosives_weight_tons,
             incendiary_devices, incendiary_devices_type, incendiary_devices_weight_pounds,
             incendiary_devices_weight_tons,
             fragmentation_devices, fragmentation_devices_type, fragmentation_devices_weight_pounds,
             fragmentation_devices_weight_tons, total_weight_pounds, total_weight_tons, time_over_target,
             bomb_damage_assessment, source_id, target_id))
        print("Inserted mission successfully")

        target_conn.commit()  # התחייבות של כל השינויים

    # סגירת ה-cursors והחיבורים
    cur.close()
    s_cur.close()
    target_conn.close()
    source_conn.close()
    print("Database connection closed")


def get_or_insert_city(cur, city_name, country_id):
    # תחילה, נבדוק אם העיר כבר קיימת
    cur.execute("SELECT city_id FROM cities WHERE city_name = %s", (city_name,))
    existing_city = cur.fetchone()

    if existing_city:
        # אם העיר קיימת, מחזירים את ה-ID שלה
        return existing_city[0]
    else:
        # אם העיר לא קיימת, נכנס אותה
        cur.execute("INSERT INTO cities (city_name, country_id) VALUES (%s, %s) RETURNING city_id",
                    (city_name, country_id))
        new_city_id = cur.fetchone()[0]
        return new_city_id
normalize_db()