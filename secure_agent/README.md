# Secure Hospital Operations AI Agent

## Overview

This project demonstrates application-level security controls for an AI agent managing synthetic hospital equipment records.

It is designed for comparison with the intentionally vulnerable implementation.

All records, accounts, and email actions are simulated.

## Technologies

- Python 3
- Ollama (`llama3.2`)
- LangChain / LangGraph
- SQLite
- Document-based RAG
- Pytest
- JSONL audit logging

## Architecture and Security Controls

The agent uses a local language model to request actions, while Python backend functions enforce security policies.

### Authentication and RBAC

Local demonstration accounts provide role-based permissions.

Roles include Viewer, Technician, and Manager. Only the Manager role is permitted to request simulated email actions.

The demonstration uses fixed local credentials and is not production-grade authentication.

### Tenant Isolation

Equipment queries use the tenant identifier from the authenticated session.

The language model cannot select or override the tenant parameter.

### Input Validation and Least Privilege

Tool access is checked against backend permissions.

Email requests are validated before any simulated outbox record is written.

### Human Approval

Authorized email actions require explicit terminal confirmation.

A refusal or missing approval prevents the simulated action.

### Secure Memory

Only validated language preferences can persist between sessions.

Arbitrary instructions, including memory-poisoning attempts, are rejected.

### Audit Logging

Tool authorization results and approval decisions are recorded locally in `audit_log.jsonl`.

## Installation

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Ensure Ollama is running with `llama3.2:latest`.

## Execution

After preparing the synthetic database and documents, run:

```bash
python secure_agent/agent.py
```

Sign in using one of the local training accounts defined in `security.py`.

## Security Tests

Run the automated regression tests:

```bash
python -m pytest secure_agent/test_security.py -v
```

The test suite covers:

- Authentication
- RBAC restrictions
- Tenant isolation
- Memory-poisoning prevention
- Unauthorized email denial
- Required human approval

## Comparison With the Vulnerable Agent

The secure implementation blocks unauthorized simulated email execution, rejects persistent malicious instructions, and restricts equipment access to the authenticated hospital.

These are application-level safeguards. The demonstration does not establish security for production hospital use.