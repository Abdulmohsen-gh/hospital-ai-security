
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from security import authorize, Session

BASE_DIR = Path(__file__).resolve().parent
AUDIT_FILE = BASE_DIR / "audit_log.jsonl"
OUTBOX_FILE = BASE_DIR / "sent_emails.txt"

ALLOWED_DOMAIN = "hospital.test"


def audit_event(session, action, outcome, details):
    """Record security decisions in a local audit log."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "username": session.username if session else "unknown",
        "tenant": session.tenant if session else "unknown",
        "action": action,
        "outcome": outcome,
        "details": details
    }

    with AUDIT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


def send_secure_email(
    session: Session,
    to: str,
    subject: str,
    body: str,
    approval_callback=None
):
    """Authorize, validate and approve simulated email."""

    if not authorize(session, "email_tool"):
        audit_event(session, "email_tool", "DENIED", "Insufficient role")
        return "DENIED: You are not authorized to send emails."

    if not all(isinstance(x, str) for x in (to, subject, body)):
        audit_event(session, "email_tool", "DENIED", "Invalid fields")
        return "DENIED: Invalid email fields."

    if not re.fullmatch(
        r"[a-zA-Z0-9._%+\-]+@" + re.escape(ALLOWED_DOMAIN),
        to
    ):
        audit_event(session, "email_tool", "DENIED", "Unapproved recipient")
        return "DENIED: Email recipient is not approved."

    if not subject.strip() or not body.strip():
        audit_event(session, "email_tool", "DENIED", "Empty content")
        return "DENIED: Subject and body are required."

    if len(subject) > 120 or len(body) > 1000 or "\n" in subject or "\r" in subject:
        audit_event(session, "email_tool", "DENIED", "Invalid content length or format")
        return "DENIED: Invalid email content."

    approved = approval_callback(to, subject, body) if approval_callback else False

    if not approved:
        audit_event(session, "email_tool", "DENIED", "Human approval missing")
        return "DENIED: Human approval was not granted."

    with OUTBOX_FILE.open("a", encoding="utf-8") as file:
        file.write(
            f"TO: {to}\n"
            f"SUBJECT: {subject}\n"
            f"BODY: {body}\n"
            "---\n"
        )

    audit_event(session, "email_tool", "APPROVED", "Simulated email recorded")
    return f"SIMULATED: Approved email recorded for {to}"


def terminal_approval(to, subject, body):
    print("\n--- HUMAN APPROVAL REQUIRED ---")
    print("Recipient:", to)
    print("Subject:", subject)
    print("Body:", body)
    answer = input("Approve simulated email? [y/N]: ").strip().lower()
    return answer == "y"


if __name__ == "__main__":
    from security import authenticate

    session = authenticate("manager1", "demo-manager-123")

    result = send_secure_email(
        session,
        "audit@hospital.test",
        "Maintenance Report",
        "Synthetic maintenance test",
        approval_callback=terminal_approval
    )

    print(result)
