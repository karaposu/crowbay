# Component-by-component

| Component | Difficulty | Solo time | The catch |
|---|---|---|---|
| FastAPI backbone + JWT + DB | Easy | 3–5 days | You've built this twice; the verification schema already exists |
| Telegram bot (command flows) | Easy-moderate | 4–6 days | Bots can only download files up to ~20MB — screen recordings blow past that. You'll need a self-hosted Bot API server or presigned-URL uploads. Plan 1–2 extra days |
| Email verification | Trivial | 0.5 day | Phone/SMS via Twilio adds 1 day + per-SMS cost — I'd defer phone entirely |
| ID + selfie verification (hybrid) | Hard | 5–8 days | LLM-OCR of the ID + face-embedding match (InsightFace) is days of work. Real liveness detection is weeks and still weak — MVP answer is a random-gesture video selfie + human spot-check |
| Biometric duplicate detection | Moderate | 1–2 days | Embedding + cosine similarity is fine at MVP scale; false positives go to the review queue |
| USDT escrow on one chain | Hard | 7–12 days | Not algorithmically hard — operationally hard |
| Video verification (hybrid) | Moderate | 5–8 days | Making it demo-work is 2 days. The human approver is what makes it shippable |
| Matching + notifications | Easy | 1–2 days | Your docs already scoped it to SQL WHERE clauses — correctly |
| Trust score, audit log, encryption | Easy | 2–3 days | Formula is arithmetic; audit is one table |
| Admin review tooling | Moderate | 3–5 days | The component everyone forgets: you need approve/reject queues for IDs, task completions, and disputes. Cheapest version: an admin Telegram channel with inline buttons |
