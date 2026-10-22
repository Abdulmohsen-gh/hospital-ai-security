
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "hospital.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    status TEXT NOT NULL,
    last_maintenance TEXT NOT NULL,
    next_maintenance TEXT NOT NULL
)
""")

equipment = [
    (1, "MRI Scanner", "Radiology", "Operational",
     "2026-09-10", "2026-12-10"),
    (2, "Ventilator", "ICU", "Maintenance Required",
     "2026-08-15", "2026-10-25"),
    (3, "CT Scanner", "Radiology", "Operational",
     "2026-09-20", "2026-12-20"),
    (4, "Infusion Pump", "Emergency", "Out of Service",
     "2026-07-12", "2026-10-15"),
    (5, "Ultrasound Machine", "Cardiology", "Operational",
     "2026-09-01", "2026-12-01")
]

cursor.executemany("""
INSERT OR REPLACE INTO equipment
(id, name, department, status, last_maintenance, next_maintenance)
VALUES (?, ?, ?, ?, ?, ?)
""", equipment)

connection.commit()
connection.close()

print("Hospital database created successfully!")
