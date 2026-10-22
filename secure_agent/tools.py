
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "hospital.db"


def search_equipment(keyword: str, tenant_id: str) -> str:
    """Search equipment belonging to the authenticated tenant only."""

    if not isinstance(keyword, str) or len(keyword) > 100:
        return "DENIED: Invalid search keyword."

    if not isinstance(tenant_id, str) or not tenant_id:
        return "DENIED: Invalid tenant."

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT id, name, department, status,
                   last_maintenance, next_maintenance
            FROM equipment
            WHERE tenant_id = ?
              AND (name LIKE ? OR department LIKE ?)
            """,
            (
                tenant_id,
                f"%{keyword}%",
                f"%{keyword}%"
            )
        ).fetchall()

    if not rows:
        return "No equipment found for your hospital."

    return "\n".join(str(row) for row in rows)


if __name__ == "__main__":
    print("Hospital A:")
    print(search_equipment("Ultrasound", "hospital_a"))

    print("\nHospital B:")
    print(search_equipment("Ultrasound", "hospital_b"))
