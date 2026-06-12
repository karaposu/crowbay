# filepath: simplified_concepts_to_implement.md

# Simplified Core Concepts for Prototype

## 1. Basic User Verification
Simple two-tier system: unverified (email/phone only) and verified (government ID + selfie). Just enough to establish identity and enable basic demographic filtering.

## 2. Telegram Bot Interface
Basic conversational bot that can create tasks through simple commands and menus. Focus on core task creation and status updates.

## 3. Manual Task Verification
Human review of task completion with simple approve/reject workflow. Screen recordings uploaded but reviewed manually for prototype.

## 4. Simple Escrow Payment
Basic USDT payment flow: poster deposits, held in escrow, released to performer after verification. Single blockchain, fixed commission.

## 5. Basic Task Matching
Simple filter matching based on verified demographics. No complex algorithms, just SQL queries matching requirements.

## 6. Essential Anti-Fraud
Duplicate account prevention using selfie matching. Basic rate limiting and manual review flags for suspicious activity.

## 7. Minimal Audit Logging
Log essential actions only: task creation, verification decisions, payments. Simple database table, no complex infrastructure.