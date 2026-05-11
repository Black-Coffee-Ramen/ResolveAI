# Multi-Domain Support Triage Agent

A terminal-based support triage agent that handles customer support tickets across three platforms: **HackerRank**, **Claude (Anthropic)**, and **Visa**.

---

## Overview

The agent reads support tickets from a CSV, retrieves relevant documentation, and for each ticket:
- Classifies the **request type** (product_issue, bug, feature_request, invalid)
- Identifies the **product area** (billing, access, fraud, test_management, etc.)
- Decides whether to **reply or escalate**
- Generates a **grounded, safe response** based only on the support corpus

---

## Project Structure

```
.
├── agent.py          # LLM triage logic (Ollama / llama3)
├── retriever.py      # TF-IDF + keyword retrieval
├── scraper.py        # Support corpus (40 documents across 3 domains)
├── utils.py          # Safety prechecks (fraud, injection, out-of-scope)
├── run.py            # Main entry point
├── requirements.txt  # Python dependencies
└── readme.md         # This file
```

---

## Setup

### 1. Install Ollama and pull the model

```bash
brew install ollama        # macOS
ollama pull llama3
ollama serve               # Run in a separate terminal
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Place the tickets CSV in the project folder

```
support_tickets.csv        # Columns: Issue, Subject, Company
```

---

## Run

```bash
python3 run.py
```

Outputs:
- `output.csv` — triage results for all tickets
- `log.txt` — full prompt/response log for every ticket

---

## How It Works

### 1. Corpus (`scraper.py`)
A hand-curated corpus of 40 documents covering all three support domains:
- **HackerRank**: score disputes, test access, extra time, rescheduling, subscriptions, user management, compatibility issues, certificates, billing, InfoSec
- **Claude**: workspace access, billing, conversation deletion, outages, bug bounty, web crawling, data retention, AWS Bedrock, LTI for education
- **Visa**: unauthorized transactions, lost/stolen cards, refunds/disputes, identity theft, emergency cash, traveller's cheques, minimum spend rules

### 2. Retrieval (`retriever.py`)
Hybrid retrieval combining:
- **TF-IDF cosine similarity** for semantic matching
- **Company/source boost** (+3.0) to prioritize docs from the correct platform
- **Keyword overlap bonus** for exact term matching

### 3. Safety Prechecks (`utils.py`)
Before calling the LLM, the agent checks for:
- **Fraud / identity theft / stolen cards** → immediate escalation with emergency contacts
- **Prompt injection attempts** (including multilingual) → declined and flagged
- **Harmful system commands** → declined
- **Out-of-scope requests** → politely declined as invalid

### 4. LLM Triage (`agent.py`)
Uses `llama3` via Ollama with:
- `temperature: 0.1` for consistent, grounded responses
- Strict prompt instructing the model to use only provided documentation
- JSON extraction with regex fallback
- Automatic escalation fallback if the model fails

---

## Output Format

`output.csv` contains these columns:

| Column | Description |
|---|---|
| `issue` | Original issue text |
| `subject` | Email subject |
| `company` | HackerRank / Claude / Visa / (blank) |
| `status` | `replied` or `escalated` |
| `product_area` | e.g. `billing`, `fraud_security`, `test_management` |
| `request_type` | `product_issue`, `bug`, `feature_request`, or `invalid` |
| `response` | Response generated for the customer |
| `justification` | Internal reasoning for the decision |

---

## Requirements

```
pandas
scikit-learn
requests
```

- Python 3.8+
- Ollama running locally with `llama3` model