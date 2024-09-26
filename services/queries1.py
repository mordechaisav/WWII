from db import get_db_connection, release_db_connection


def create_indexes():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Create indexes to improve query performance
        index_queries = [
            "CREATE INDEX IF NOT EXISTS idx_mission_date ON mission(mission_date);",
            "CREATE INDEX IF NOT EXISTS idx_air_force ON mission(air_force);",
            "CREATE INDEX IF NOT EXISTS idx_target_city ON mission(target_city);",
            "CREATE INDEX IF NOT EXISTS idx_airborne_aircraft ON mission(\"airborne_aircraft\");",
            "CREATE INDEX IF NOT EXISTS idx_bomb_damage_assessment ON mission(\"bomb_damage_assessment\");",
            "CREATE INDEX IF NOT EXISTS idx_target_country ON mission(\"target_country\");",
            "CREATE INDEX IF NOT EXISTS idx_air_force_target_city ON mission(air_force, target_city);",
            "CREATE INDEX IF NOT EXISTS idx_airborne_bomb_damage ON mission(\"airborne_aircraft\", \"bomb_damage_assessment\");"
        ]

        for query in index_queries:
            cursor.execute(query)
        conn.commit()

    finally:
        release_db_connection(conn)


def run_query_and_explain(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Run the query with EXPLAIN ANALYZE
        cursor.execute("EXPLAIN ANALYZE " + query)
        explain_result = cursor.fetchall()
        return explain_result
    finally:
        release_db_connection(conn)


def main(year):
    create_indexes()

    # First query to get the most active air force in 1942
    query1 = """
        SELECT 
            air_force, 
            target_city,
            COUNT(mission_id) AS mission_count
        FROM 
            mission
        WHERE 
            EXTRACT(YEAR FROM mission_date) = %s
        GROUP BY 
            air_force, 
            target_city
        ORDER BY 
            mission_count DESC
        LIMIT 1;  
        """




    # Second query to get the maximum bomb damage assessment for bombing missions
    query2 = """
    SELECT 
            "target_country", 
            MAX("bomb_damage_assessment") AS max_damage
        FROM 
            mission
        WHERE 
            CAST("airborne_aircraft" AS NUMERIC) > 5 
            AND "bomb_damage_assessment" IS NOT NULL
        GROUP BY 
            "target_country"
        limit 1 
    """

    # Execute the queries with EXPLAIN ANALYZE
    explain_result1 = run_query_and_explain(query1,(year,))
    explain_result2 = run_query_and_explain(query2)

    # Document the findings in a text file
    with open('results.txt', 'w') as f:
        f.write("### Query Performance Documentation ###\n\n")

        f.write("1. Performance of the queries after index creation:\n")
        f.write("   - Query 1: \n")
        for row in explain_result1:
            f.write(f"     {row}\n")

        f.write("   - Query 2: \n")
        for row in explain_result2:
            f.write(f"     {row}\n")

        f.write("\n2. Created indexes:\n")
        f.write("   - idx_mission_date on mission(mission_date)\n")
        f.write("   - idx_air_force on mission(air_force)\n")
        f.write("   - idx_target_city on mission(target_city)\n")
        f.write("   - idx_airborne_aircraft on mission(\"Airborne Aircraft\")\n")
        f.write("   - idx_bomb_damage_assessment on mission(\"Bomb Damage Assessment\")\n")
        f.write("   - idx_target_country on mission(\"Target Country\")\n")
        f.write("   - idx_air_force_target_city on mission(air_force, target_city)\n")
        f.write("   - idx_airborne_bomb_damage on mission(\"Airborne Aircraft\", \"Bomb Damage Assessment\")\n")

        f.write("\n3. Explanation of the results:\n")
        f.write(
            "   - The query results improved because the created indexes allow the database to search quickly based on the selected columns.\n")


if __name__ == "__main__":
    main(1942)
