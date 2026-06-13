# filepath: simplified_concepts_to_implement.md

# Simplified Core Concepts for Prototype

## 1. Attribute Verification Pipeline
Modular pipeline with three components: Attribute Requirements (task needs), Predefined Proof Uploading (email, phone, ID+selfie, social media credentials), and Attribute Extraction (deriving verified attributes from proofs). Handles both app-level and task-level verifications seamlessly.

## 2. Command-Based Telegram Interface
Structured command system with guided conversational flows instead of full NLP. Uses inline keyboards and step-by-step forms while maintaining the conversational feel for task creation.

## 3. Task Completion Verification
Hybrid system for verifying screen recordings where AI extracts key information and humans make final approval decisions. Ensures tasks are completed correctly.

## 4. Single-Chain Payment System
USDT on Polygon with basic escrow functionality. Supports wallet generation and automated distribution but focuses on one blockchain for simplicity.

## 5. Filter-Based Task Matching
Simple database queries that match tasks to performers based on verification tier requirements and demographic filters. Pure SQL matching without scoring or algorithms.

## 6. Core Demographics Filtering
Supports essential demographics: location (country/city), age range, gender, and education level. Reduces complexity while keeping the filtering framework intact.

## 7. Basic Fraud Detection
Focus on duplicate account prevention via biometric matching and suspicious pattern detection. Simplified but maintains the multi-check architecture.

## 8. Event-Based Audit System
Logs critical events (tasks, verifications, payments) with structured data. Simplified from comprehensive logging but maintains queryable architecture.

## 9. Simple Trust Score
Three-component score: verification level (40%), task success rate (40%), account age (20%). Simplified calculation but maintains the scoring framework.

## 10. Basic Privacy Protection
Database-level encryption for sensitive fields and secure document storage. Simplified from field-level encryption but maintains privacy architecture.