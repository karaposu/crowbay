# filepath: verification_table_clarification.md

# Verification System Database Architecture

This document explains how the verification tables work together to create a flexible, reusable proof system for Crowd.

## Table Overview

### 1. proof_types
**Purpose**: Defines what types of proofs can be uploaded to the system.

**Example Records**:
```
| id | proof_name          | proof_category | description                          |
|----|---------------------|----------------|--------------------------------------|
| 1  | government_id_photo | document       | Clear photo of government-issued ID  |
| 2  | selfie_video        | biometric      | Live video showing face              |
| 3  | diploma_scan        | credential     | Scanned copy of university diploma   |
```

**Key Concept**: This is a reference table that defines all possible proof types. No user data is stored here.

### 2. verification_types
**Purpose**: Defines what needs to be verified (the requirements).

**Example Records**:
```
| id | verification_name    | tier | description                        | expires_after_days |
|----|---------------------|------|------------------------------------|-------------------|
| 1  | basic_identity      | 2    | Verify user is who they claim      | 730 (2 years)     |
| 2  | age_verification    | 1    | Confirm user is 18+                | NULL (permanent)  |
| 3  | education_level     | 5    | Verify educational credentials     | NULL              |
| 4  | gender_verification | 1    | Confirm stated gender              | NULL              |
```

**Key Concept**: Each verification type belongs to a tier and may have different expiration rules.

### 3. verification_proof_requirements
**Purpose**: Links verification types to the proofs they require. This is where the flexibility comes in.

**Example Records**:
```
| id | verification_type_id | proof_type_id | is_mandatory | alternative_group |
|----|---------------------|---------------|--------------|-------------------|
| 1  | 1 (basic_identity)  | 1 (gov_id)    | true         | NULL              |
| 2  | 1 (basic_identity)  | 2 (selfie)    | true         | NULL              |
| 3  | 2 (age_verify)      | 1 (gov_id)    | true         | 1                 |
| 4  | 2 (age_verify)      | 2 (selfie)    | true         | 1                 |
```

**Key Concepts**:
- `is_mandatory = true` with `alternative_group = NULL`: This proof is required
- `is_mandatory = true` with same `alternative_group`: Either proof satisfies the requirement (OR logic)
- For basic_identity: BOTH government ID AND selfie are required
- For age_verification: EITHER government ID OR selfie is sufficient

### 4. user_proofs
**Purpose**: Stores actual proofs uploaded by users.

**Example Records**:
```
| id | user_id | proof_type_id | status   | extracted_data                              |
|----|---------|---------------|----------|---------------------------------------------|
| 1  | 101     | 1 (gov_id)    | verified | {"name": "John Doe", "dob": "1990-01-15"} |
| 2  | 101     | 2 (selfie)    | verified | {"age_estimate": 33, "gender": "male"}     |
```

**Key Concept**: One proof can contain multiple pieces of extracted data that can be used by different verifications.

### 5. user_verifications
**Purpose**: Tracks which verifications a user has completed.

**Example Records**:
```
| id | user_id | verification_type_id | status   | completed_at        |
|----|---------|---------------------|----------|---------------------|
| 1  | 101     | 1 (basic_identity)  | verified | 2024-01-15 10:30:00 |
| 2  | 101     | 2 (age_verify)      | verified | 2024-01-15 10:30:00 |
| 3  | 101     | 4 (gender)          | verified | 2024-01-15 10:30:00 |
```

### 6. verification_proof_usage
**Purpose**: Links specific proofs to specific verifications, showing how proofs were used.

**Example Records**:
```
| id | user_verification_id | user_proof_id | validation_result                           |
|----|---------------------|---------------|---------------------------------------------|
| 1  | 1 (basic_identity)  | 1 (gov_id)    | {"name_match": true, "doc_authentic": true}|
| 2  | 1 (basic_identity)  | 2 (selfie)    | {"face_match": true, "liveness": 0.98}    |
| 3  | 2 (age_verify)      | 1 (gov_id)    | {"age": 33, "is_adult": true}             |
| 4  | 3 (gender)          | 2 (selfie)    | {"gender_match": true}                     |
```

### 7. verification_data
**Purpose**: Stores extracted data in a searchable, structured format for efficient querying.

**Example Records**:
```
| id | user_id | field_name     | field_value | verification_source_id | confidence | is_current |
|----|---------|----------------|-------------|------------------------|------------|------------|
| 1  | 101     | birth_date     | 1990-01-15  | 1 (basic_identity)    | 0.95       | true       |
| 2  | 101     | full_name      | John Doe    | 1 (basic_identity)    | 0.98       | true       |
| 3  | 101     | gender         | male        | 1 (basic_identity)    | 0.92       | true       |
| 4  | 101     | education_level| bachelors   | 3 (education)         | 0.99       | true       |
```

**Key Benefits**:
- **Searchable**: Can query "SELECT * FROM verification_data WHERE field_name='birth_date' AND field_value LIKE '1990-%'"
- **Privacy**: Proof files can be deleted while keeping verified data
- **Cross-validation**: Easy to check if birth_date from ID matches birth_date from diploma

### 8. verification_history
**Purpose**: Complete audit trail of all verification-related actions for compliance and debugging.

**Example Records**:
```
| id | user_verification_id | action    | actor_type | action_details                        | created_at          |
|----|---------------------|-----------|------------|---------------------------------------|---------------------|
| 1  | 1                   | submitted | user       | {"files_uploaded": 2}                 | 2024-01-01 10:00:00 |
| 2  | 1                   | rejected  | system     | {"reason": "blurry_id_photo"}        | 2024-01-01 10:05:00 |
| 3  | 1                   | submitted | user       | {"retry_attempt": 1}                  | 2024-01-01 15:00:00 |
| 4  | 1                   | approved  | system     | {"confidence": 0.95, "ai_model": "v2"}| 2024-01-01 15:05:00 |
```

**Use Cases**:
- **Compliance**: "Show me who approved this verification and when"
- **Customer Support**: "Why was my verification rejected?"
- **Security**: Detect patterns of repeated failures or suspicious activity

## How It All Works Together

### Scenario: User Completes Identity Verification

1. **Setup** (Admin defines requirements):
   - Create `proof_types`: government_id_photo, selfie_video
   - Create `verification_types`: basic_identity (Tier 2)
   - Create `verification_proof_requirements`: basic_identity requires BOTH proofs

2. **User Uploads Proofs**:
   - User uploads government ID → Creates record in `user_proofs`
   - AI extracts: name, date of birth, document number
   - User uploads selfie video → Creates another record in `user_proofs`
   - AI extracts: estimated age, gender, liveness score

3. **Verification Process**:
   - System checks if user has all required proofs for basic_identity
   - Creates `user_verifications` record with status "pending"
   - Creates `verification_history` record: action="submitted"
   - Validates each proof against requirements
   - Creates `verification_proof_usage` records linking proofs to verification
   - Extracts searchable data and creates `verification_data` records:
     - birth_date → "1990-01-15"
     - full_name → "John Doe"
     - gender → "male"
   - Updates `user_verifications` status to "verified"
   - Creates `verification_history` record: action="approved"

4. **Proof Reuse**:
   - Same selfie automatically satisfies age_verification requirement
   - System creates new `user_verifications` record for age_verification
   - Links existing selfie proof via `verification_proof_usage`
   - May create new `verification_data` if new fields are extracted
   - No need to upload new proof!

## Key Benefits of This Design

### 1. Proof Reusability
A single selfie can be used for:
- Identity verification (face matching with ID)
- Age verification (AI age estimation)
- Gender verification (AI gender detection)

### 2. Flexible Requirements
- Can require ALL proofs (AND logic)
- Can require ANY proof from a group (OR logic)
- Easy to add new verification types using existing proofs

### 3. Audit Trail
- Every proof usage is tracked
- Validation results are stored
- Can see exactly which proofs supported which verifications

### 4. Efficient Storage
- Proofs uploaded once, used many times
- Extracted data stored separately from files
- Files can be deleted after processing while keeping extracted data

## Example Queries

### Get User's Current Verification Tier
```sql
SELECT MAX(vt.tier) as user_tier
FROM user_verifications uv
JOIN verification_types vt ON uv.verification_type_id = vt.id
WHERE uv.user_id = ? 
  AND uv.status = 'verified'
  AND (uv.expires_at IS NULL OR uv.expires_at > NOW())
```

### Check If User Can Accept a Task
```sql
-- For a task requiring Tier 3 and education verification
SELECT COUNT(DISTINCT vt.id) = 2 as can_accept
FROM user_verifications uv
JOIN verification_types vt ON uv.verification_type_id = vt.id
WHERE uv.user_id = ?
  AND uv.status = 'verified'
  AND (
    (vt.tier >= 3) OR 
    (vt.verification_name = 'education_level')
  )
```

### Find What Proofs User Needs for Next Tier
```sql
SELECT DISTINCT pt.proof_name, pt.description
FROM verification_proof_requirements vpr
JOIN proof_types pt ON vpr.proof_type_id = pt.id
JOIN verification_types vt ON vpr.verification_type_id = vt.id
WHERE vt.tier = ?
  AND NOT EXISTS (
    SELECT 1 FROM user_proofs up
    WHERE up.user_id = ?
      AND up.proof_type_id = pt.id
      AND up.status = 'verified'
  )
```

### Search Users by Verified Data
```sql
-- Find all verified users born in 1990
SELECT DISTINCT u.id, u.name, u.email
FROM users u
JOIN verification_data vd ON u.id = vd.user_id
WHERE vd.field_name = 'birth_date' 
  AND vd.field_value LIKE '1990-%'
  AND vd.is_current = true
  AND vd.confidence_score > 0.9
```

### Audit Verification Attempts
```sql
-- See why a user's verifications have been failing
SELECT vh.created_at, vh.action, vh.action_details, vt.verification_name
FROM verification_history vh
JOIN user_verifications uv ON vh.user_verification_id = uv.id
JOIN verification_types vt ON uv.verification_type_id = vt.id
WHERE uv.user_id = ?
  AND vh.action IN ('rejected', 'expired')
ORDER BY vh.created_at DESC
```

## Data Flow Diagram

```
User Upload → proof_types (definition)
     ↓              ↓
user_proofs ← AI Processing
     ↓
Extracted Data ──────────→ verification_data (searchable fields)
     ↓
verification_types ← verification_proof_requirements
     ↓                            ↓
user_verifications ← Validation Engine
     ↓                     ↓
     ↓              verification_history (audit log)
     ↓
verification_proof_usage (links proofs to verifications)
```

This architecture ensures that the verification system is both flexible and maintainable, allowing Crowd to adapt verification requirements without changing the core structure.





