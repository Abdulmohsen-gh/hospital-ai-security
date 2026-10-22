
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "hospital.db"


def search_equipment(keyword: str) -> str:
    """Search synthetic hospital equipment records."""

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT id, name, department, status,
                   last_maintenance, next_maintenance
            FROM equipment
            WHERE name LIKE ? OR department LIKE ?
            """,
            (f"%{keyword}%", f"%{keyword}%")
        )
        records = cursor.fetchall()

    if not records:
        return "No equipment found."

    return "\n".join(str(record) for record in records)


if __name__ == "__main__":
    print(search_equipment("ICU"))


OUTBOX_PATH = Path(__file__).resolve().parent / "data" / "sent_emails.txt"


def send_email(to: str, subject: str, body: str) -> str:
    """
    Simulated email tool.
    VULNERABLE: no authentication or authorization checks.
    """
    with OUTBOX_PATH.open("a", encoding="utf-8") as file:
        file.write(
            f"TO: {to}\n"
            f"SUBJECT: {subject}\n"
            f"BODY: {body}\n"
            "---\n"
        )

    return f"SIMULATED email recorded for {to}"
