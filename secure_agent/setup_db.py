
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "hospital.db"

equipment = [
    (1, "MRI Scanner", "Radiology", "Operational",
     "2026-09-10", "2026-12-10", "hospital_a"),

    (2, "Ventilator", "ICU", "Maintenance Required",
     "2026-08-15", "2026-10-25", "hospital_a"),

    (3, "CT Scanner", "Radiology", "Operational",
     "2026-09-20", "2026-12-20", "hospital_a"),

    (4, "Infusion Pump", "Emergency", "Out of Service",
     "2026-07-12", "2026-10-15", "hospital_a"),

    (5, "Ultrasound Machine", "Cardiology", "Operational",
     "2026-09-01", "2026-12-01", "hospital_b")
]

with sqlite3.connect(DB_PATH) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            status TEXT NOT NULL,
            last_maintenance TEXT NOT NULL,
            next_maintenance TEXT NOT NULL,
            tenant_id TEXT NOT NULL
        )
    """)

    conn.executemany("""
        INSERT OR REPLACE INTO equipment
        (id, name, department, status,
         last_maintenance, next_maintenance, tenant_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, equipment)

    conn.commit()

print("Secure hospital database ready!")
