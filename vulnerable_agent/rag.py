
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=60
)


def load_documents():
    """Load and split synthetic hospital documents."""
    chunks = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        parts = splitter.split_text(text)

        for index, part in enumerate(parts, start=1):
            chunks.append({
                "source": file_path.name,
                "chunk_id": index,
                "content": part
            })

    return chunks


def search_documents(query: str) -> str:
    """Retrieve relevant document chunks using keyword matching."""
    chunks = load_documents()
    keywords = set(query.lower().split())

    results = []

    for chunk in chunks:
        content = chunk["content"].lower()

        score = sum(
            1 for keyword in keywords
            if keyword in content
        )

        if score > 0:
            results.append((score, chunk))

    results.sort(key=lambda item: item[0], reverse=True)

    if not results:
        return "No relevant documents found."

    output = []

    for score, chunk in results[:3]:
        output.append(
            f"Source: {chunk['source']} "
            f"(Chunk {chunk['chunk_id']})\n"
            f"{chunk['content']}"
        )

    return "\n\n".join(output)


if __name__ == "__main__":
    print(search_documents("ventilator maintenance procedure"))
