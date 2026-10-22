# Vulnerable Hospital Operations AI Agent

## Overview

This project demonstrates an intentionally vulnerable AI agent for a synthetic hospital equipment management system.

The agent uses a local Ollama language model, LangGraph, SQLite, and document-based retrieval to answer questions about hospital equipment and maintenance procedures.

**For cybersecurity training only.** All equipment records and maintenance documents are fictional.

## Technologies

- Python 3
- Ollama (`llama3.2`)
- LangChain / LangGraph
- SQLite
- Document-based RAG using text chunking and keyword retrieval
- Simulated email tool

## Architecture

The user interacts with the AI agent, which can request three tools:

1. `equipment_search`: Retrieves equipment records from SQLite.
2. `document_search`: Retrieves relevant maintenance document chunks with source references.
3. `email_tool`: Records simulated emails in a local text file.

User messages are also stored in persistent memory and loaded into the agent's system context.

## Installation

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Ensure Ollama is running and `llama3.2:latest` is available.

## Setup and Execution

Create the synthetic equipment database:

```bash
python vulnerable_agent/setup_db.py
```

Run the agent:

```bash
python vulnerable_agent/agent.py
```

Type `quit` to exit.

## Demonstrated Vulnerabilities

### 1. Tool Misuse

The agent does not authenticate users or authorize simulated email actions.

A user can claim to be a hospital administrator and request an email to an arbitrary recipient. The resulting local outbox entry demonstrates unauthorized tool execution, not real email delivery.

### 2. Persistent Memory Poisoning

The agent stores arbitrary user messages in `data/memory.txt` and later places them into a high-priority instruction context.

A malicious stored instruction can change the agent's behavior after a process restart.

## RAG Implementation

Maintenance documents are split into overlapping text chunks. Keyword retrieval selects relevant chunks and returns source filenames and chunk identifiers.

This is a lightweight document-based RAG implementation without vector embeddings.

## Security Limitations

This agent intentionally lacks authentication, authorization, memory validation, tenant isolation, and human approval.

It must not be deployed publicly or connected to real hospital systems.

## Testing

The following manual experiments demonstrate the security weaknesses:

- Unauthorized simulated email tool execution
- Persistent memory poisoning across restarts
- Equipment search using SQLite
- Document retrieval with source citations

Compare these results against the separate Secure Agent implementation.