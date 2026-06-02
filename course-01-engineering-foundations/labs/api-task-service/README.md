# Lab: API Task Service — API Design Fundamentals

## Overview
Build a small HTTP JSON API for creating and managing tasks. The goal is to practice API design fundamentals: request/response contracts, validation, error handling, pagination, and predictable status codes.

## Learning Objectives
- Design a stable API contract with clear status codes.
- Validate inputs and return consistent errors.
- Implement pagination for list endpoints.

## Prerequisites
- Python 3.10+

## Setup

```bash
cd course-01-engineering-foundations/labs/api-task-service/starter-code
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --port 8001
```

## Validation

```bash
# Create a task
curl -s -X POST http://localhost:8001/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Write syllabus updates","priority":2}' | jq

# List tasks (paginated)
curl -s 'http://localhost:8001/tasks?limit=2&offset=0' | jq

# Invalid input should return a 422 with a predictable error envelope
curl -s -X POST http://localhost:8001/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"","priority":99}' | jq
```

## Experiment
Change the pagination strategy.

1. Implement cursor pagination (`cursor` + `limit`) instead of offset pagination.
2. Create 10,000 tasks and compare latency for deep pages (e.g. offset 9000) vs cursor.

## Solution
See `../solution/` for a reference implementation with cursor pagination.
