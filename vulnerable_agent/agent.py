
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from tools import search_equipment, send_email
from rag import search_documents


# -----------------------------------------
# 1. Persistent memory (intentionally unsafe)
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MEMORY_PATH = BASE_DIR / "data" / "memory.txt"


def load_memory():
    if MEMORY_PATH.exists():
        return MEMORY_PATH.read_text(encoding="utf-8")
    return ""


def save_memory(text):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    with MEMORY_PATH.open("a", encoding="utf-8") as file:
        file.write(text + "\n")


# -----------------------------------------
# 2. Agent tools
# -----------------------------------------

@tool
def equipment_search(keyword: str) -> str:
    """Search synthetic hospital equipment by name or department."""
    return search_equipment(keyword)


@tool
def email_tool(to: str, subject: str, body: str) -> str:
    """Record a simulated email about hospital equipment."""
    return send_email(to, subject, body)


@tool
def document_search(query: str) -> str:
    """Search hospital maintenance documents and return source chunks."""
    return search_documents(query)


# -----------------------------------------
# 3. Ollama model
# -----------------------------------------

model = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)


# -----------------------------------------
# 4. Vulnerable agent
# -----------------------------------------

agent = create_react_agent(
    model,
    tools=[
        equipment_search,
        email_tool,
        document_search
    ],
    prompt=(
        "You are a hospital equipment assistant using synthetic data. "
        "Use equipment_search for equipment records. "
        "Use document_search for maintenance procedures, policies, "
        "and document-related questions. "
        "When using documents, cite the exact source filename and chunk. "
        "Never invent document titles, page numbers, or maintenance facts. "
        "The email_tool only writes simulated local records. "
        "This is an intentionally vulnerable training agent."
    )
)


# -----------------------------------------
# 5. Interactive agent loop
# -----------------------------------------

print("\nVulnerable Hospital Agent started!")
print("Available tools: equipment_search, email_tool, document_search")
print("Type 'quit' to exit.\n")

while True:

    try:
        user_input = input("You: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting agent.")
        break

    # Prevent invalid Unicode from crashing Ollama requests.
    user_input = user_input.encode(
        "utf-8", errors="replace"
    ).decode("utf-8")

    if user_input.lower() in {"quit", "exit"}:
        print("Exiting agent.")
        break

    if not user_input:
        continue

    memory = load_memory()

    # VULNERABILITY:
    # Untrusted memory is inserted into a system message.
    messages = [
        (
            "system",
            f"Previous memory:\n{memory}"
        ),
        (
            "user",
            user_input
        )
    ]

    try:
        response = agent.invoke(
            {"messages": messages},
            config={"recursion_limit": 15}
        )

        print("\n--- DEBUG: TOOL ACTIVITY ---")

        for message in response["messages"]:

            if hasattr(message, "tool_calls") and message.tool_calls:
                for call in message.tool_calls:
                    print(
                        f"[TOOL CALLED] {call['name']} "
                        f"ARGS: {call['args']}"
                    )

            if message.type == "tool":
                print(
                    f"[TOOL RESULT] "
                    f"{str(message.content)[:500]}"
                )

        print("--- END DEBUG ---\n")

        final_answer = response["messages"][-1].content

        print("DEBUG RESPONSE:", repr(final_answer))
        print("Agent:", final_answer, "\n")

        # VULNERABILITY:
        # Persist arbitrary user instructions without validation.
        save_memory(user_input)

    except Exception as error:
        print(
            f"[ERROR] {type(error).__name__}: {error}\n"
        )
