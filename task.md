# Tasks - ResolveAI Implementation

## Phase 1: Foundation & Infrastructure
- [ ] Create folder structure [/]
- [ ] Initialize `.env.example` and `docker-compose.yml` [ ]
- [ ] Define database models (PostgreSQL + SQLAlchemy) [ ]
- [ ] Set up Redis connection utility [ ]
- [ ] Create shared Pydantic schemas [ ]

## Phase 2: Mock Services & Webhook
- [ ] Implement Mock CRM service [ ]
- [ ] Create `/webhook/ticket` endpoint [ ]
- [ ] Implement Redis producer logic [ ]

## Phase 3: RAG Pipeline
- [ ] Create sample knowledge base documents [ ]
- [ ] Implement ingestion script (chunking, embedding, ChromaDB) [ ]
- [ ] Implement RAG retrieval tool [ ]

## Phase 4: AI Agent Worker
- [ ] Set up worker loop polling Redis [ ]
- [ ] Implement prompt templates with safety delimiters [ ]
- [ ] Implement agent logic (classification, tool calling) [ ]
- [ ] Implement response generation with guardrails [ ]
- [ ] Store triage results in PostgreSQL [ ]

## Phase 5: Human-in-the-Loop & Metrics
- [ ] Implement `/api/pending_approvals` [ ]
- [ ] Implement `/api/approve/{ticket_id}` [ ]
- [ ] Set up metrics tracking and `/metrics` endpoint [ ]

## Phase 6: Frontend Dashboard
- [ ] Initialize Next.js app with Tailwind CSS [ ]
- [ ] Build pending approvals view [ ]
- [ ] Build ticket detail view [ ]
- [ ] Build metrics overview dashboard [ ]

## Phase 7: Testing & Documentation
- [ ] Write unit tests for agent and tools [ ]
- [ ] Write API integration tests [ ]
- [ ] Generate final README with architecture diagram [ ]
- [ ] Final verification and cleanup [ ]
