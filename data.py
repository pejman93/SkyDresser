import sqlite3
from sqlite3 import connect
import csv
import os
from datetime import datetime

# Ensure database directory exists
db_dir = os.path.join(os.path.dirname(__file__), "database")
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Create the database path
db_path = os.path.join(db_dir, "weatherincity.db")
conn = connect(db_path)
cursor = conn.cursor()


def create_table():
    # start navigation to DB
    nav = conn.cursor()
    # execute the code
    nav.execute("""
        CREATE TABLE IF NOT EXISTS weather_city 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            windspeed REAL,
            longitude REAL,
            latitude REAL,
            city TEXT,
            country TEXT, 
            timestamp TEXT,
            ai_clothing_advice TEXT
        )
                """
                )
    conn.commit()
    conn.close()


def insert_weather_data(temperature, windspeed, longitude, latitude, city, country, ai_clothing_advice):
    conn = sqlite3.connect(db_path)
    nav = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nav.execute("""
        INSERT INTO weather_city (temperature, windspeed, longitude, latitude, city, country, timestamp, ai_clothing_advice)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (temperature, windspeed, longitude, latitude, city, country, timestamp, ai_clothing_advice))
    conn.commit()
    conn.close()


def export_to_csv():
    conn = sqlite3.connect(db_path)
    nav = conn.cursor()
    nav.execute("SELECT * FROM weather_city")  # Changed from company_data to weather_city

    # Create CSV file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(os.path.dirname(db_path), f"weather_data_{timestamp}.csv")

    # Write to CSV
    with open(csv_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        # Write header
        csv_writer.writerow(['id', 'temperature', 'windspeed', 'longitude', 'latitude', 'city', 'country', 'timestamp'])
        # Write data
        csv_writer.writerows(nav.fetchall())

    conn.close()

    print(f"Data exported to {csv_file}")
