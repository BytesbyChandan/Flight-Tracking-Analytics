
from flask import Flask, jsonify, render_template
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )


@app.route("/")
def home():
    return "Flight Tracking Dashboard Backend is Running!"

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/api/test")
def test_api():

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM FLIGHT_TRACKING
        """)

        result = cursor.fetchone()

        return jsonify({
            "status": "success",
            "total_aircraft": result[0]
        })

    finally:
        cursor.close()
        conn.close()

@app.route("/api/dashboard")
def dashboard_data():

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        dashboard = {}

        # Q1: Total Aircraft
        cursor.execute("""
            SELECT COUNT(*)
            FROM FLIGHT_TRACKING
        """)
        dashboard["total_aircraft"] = cursor.fetchone()[0]

        # Q2: Airborne vs Grounded
        cursor.execute("""
            SELECT
                CASE
                    WHEN ON_GROUND = TRUE THEN 'Grounded'
                    ELSE 'Airborne'
                END AS STATUS,
                COUNT(*)
            FROM FLIGHT_TRACKING
            GROUP BY ON_GROUND
        """)
        dashboard["ground_status"] = [
            {"status": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Q3: Top 10 Countries
        cursor.execute("""
            SELECT ORIGIN_COUNTRY, COUNT(*) AS TOTAL
            FROM FLIGHT_TRACKING
            GROUP BY ORIGIN_COUNTRY
            ORDER BY TOTAL DESC
            LIMIT 10
        """)
        dashboard["top_countries"] = [
            {"country": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Q4: Top 10 Fastest Aircraft
        cursor.execute("""
            SELECT ICAO24, CALLSIGN, ORIGIN_COUNTRY, VELOCITY
            FROM FLIGHT_TRACKING
            WHERE VELOCITY IS NOT NULL
            ORDER BY VELOCITY DESC
            LIMIT 10
        """)
        dashboard["fastest_aircraft"] = [
            {
                "icao24": row[0],
                "callsign": row[1],
                "country": row[2],
                "velocity": float(row[3])
            }
            for row in cursor.fetchall()
        ]
        
        # Q5: Country-wise Average Velocity
        cursor.execute("""
            SELECT ORIGIN_COUNTRY, AVG(VELOCITY)
            FROM FLIGHT_TRACKING
            WHERE VELOCITY IS NOT NULL
            GROUP BY ORIGIN_COUNTRY
            ORDER BY AVG(VELOCITY) DESC
            LIMIT 10
        """)
        dashboard["avg_velocity"] = [
            {"country": row[0], "velocity": float(row[1])}
            for row in cursor.fetchall()
        ]

        # Q6: Country-wise Average Barometric Altitude
        cursor.execute("""
            SELECT ORIGIN_COUNTRY, AVG(BARO_ALTITUDE)
            FROM FLIGHT_TRACKING
            WHERE BARO_ALTITUDE IS NOT NULL
            GROUP BY ORIGIN_COUNTRY
            ORDER BY AVG(BARO_ALTITUDE) DESC
            LIMIT 10
        """)
        dashboard["avg_altitude"] = [
            {"country": row[0], "altitude": float(row[1])}
            for row in cursor.fetchall()
        ]

        # Q7: Country-wise Ground vs Airborne
        cursor.execute("""
            SELECT
                ORIGIN_COUNTRY,
                SUM(IFF(ON_GROUND = TRUE, 1, 0)) AS GROUNDED,
                SUM(IFF(ON_GROUND = FALSE, 1, 0)) AS AIRBORNE
            FROM FLIGHT_TRACKING
            GROUP BY ORIGIN_COUNTRY
            ORDER BY GROUNDED DESC
            LIMIT 10
        """)
        dashboard["country_status"] = [
            {
                "country": row[0],
                "grounded": row[1],
                "airborne": row[2]
            }
            for row in cursor.fetchall()
        ]

        # Q8: Top 10 Grounded Countries
        cursor.execute("""
            SELECT ORIGIN_COUNTRY, COUNT(*)
            FROM FLIGHT_TRACKING
            WHERE ON_GROUND = TRUE
            GROUP BY ORIGIN_COUNTRY
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """)
        dashboard["grounded_countries"] = [
            {"country": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Q9: Missing Callsign by Country
        cursor.execute("""
            SELECT ORIGIN_COUNTRY, COUNT(*)
            FROM FLIGHT_TRACKING
            WHERE CALLSIGN IS NULL
            GROUP BY ORIGIN_COUNTRY
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """)
        dashboard["missing_callsign"] = [
            {"country": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]

        # Q10: Country-wise Ground Percentage
        cursor.execute("""
            SELECT
                ORIGIN_COUNTRY,
                ROUND(
                    100.0 * COUNT_IF(ON_GROUND = TRUE)
                    / NULLIF(COUNT_IF(ON_GROUND IS NOT NULL), 0),
                    2
                ) AS GROUND_PERCENTAGE
            FROM FLIGHT_TRACKING
            GROUP BY ORIGIN_COUNTRY
            ORDER BY GROUND_PERCENTAGE DESC
            LIMIT 10
        """)
        dashboard["ground_percentage"] = [
            {"country": row[0], "percentage": float(row[1])}
            for row in cursor.fetchall()
            if row[1] is not None
        ]
        cursor.execute("""
    SELECT COUNT(DISTINCT ORIGIN_COUNTRY)
    FROM FLIGHT_TRACKING
""")

        dashboard["total_countries"] = cursor.fetchone()[0]

        return jsonify(dashboard)

    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    app.run(debug=True)


