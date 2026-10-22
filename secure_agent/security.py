
from dataclasses import dataclass

# Synthetic users for local security testing only.
USERS = {
    "viewer1": {
        "password": "demo-viewer-123",
        "role": "viewer",
        "tenant": "hospital_a"
    },
    "tech1": {
        "password": "demo-tech-123",
        "role": "technician",
        "tenant": "hospital_a"
    },
    "manager1": {
        "password": "demo-manager-123",
        "role": "manager",
        "tenant": "hospital_a"
    },
    "viewer2": {
        "password": "demo-viewer2-123",
        "role": "viewer",
        "tenant": "hospital_b"
    }
}

ROLE_PERMISSIONS = {
    "viewer": {"equipment_search", "document_search"},
    "technician": {"equipment_search", "document_search"},
    "manager": {"equipment_search", "document_search", "email_tool"}
}


@dataclass(frozen=True)
class Session:
    username: str
    role: str
    tenant: str


def authenticate(username: str, password: str):
    user = USERS.get(username)

    if user is None or user["password"] != password:
        return None

    return Session(
        username=username,
        role=user["role"],
        tenant=user["tenant"]
    )


def authorize(session: Session, tool_name: str) -> bool:
    if session is None:
        return False

    return tool_name in ROLE_PERMISSIONS.get(session.role, set())


if __name__ == "__main__":
    session = authenticate("viewer1", "demo-viewer-123")

    print("Authenticated:", session is not None)
    print("Can search:", authorize(session, "equipment_search"))
    print("Can email:", authorize(session, "email_tool"))
