# filepath: devdocs/simplified_concept_clarifications/7_basic_fraud_detection.md

# Basic Fraud Detection

## What it is and why it matters
A focused anti-fraud system with two main components: biometric duplicate detection (preventing multiple accounts) and pattern-based suspicious activity flagging. Maintains the multi-layer architecture while focusing on the most critical fraud vectors.

## How this concept helps the overall project
- **Stops obvious fraud** - Prevents the most common attack vectors
- **Maintains platform integrity** - Ensures real humans perform tasks
- **Simple to implement** - Biometric APIs and pattern rules are straightforward
- **Low false positives** - Focused approach reduces incorrect flagging
- **Expandable architecture** - Can add more detection layers later

## How this concept limits the overall project
- **Misses sophisticated fraud** - Advanced schemes may go undetected
- **Limited behavioral analysis** - Only catches obvious patterns
- **No network analysis** - Can't detect coordinated fraud rings
- **Manual review burden** - Suspicious flags need human checking
- **Reactive not proactive** - Mostly catches known patterns

## What kind of information this concept needs as input
- Selfie photos from verification process
- Government ID photos for cross-matching
- Account creation velocity and patterns
- Task completion rates and timing
- IP addresses and device fingerprints
- Payment account reuse patterns

## What kind of process this concept should use
1. **Biometric Extraction** - Generate face encodings from photos
2. **Duplicate Search** - Compare against all existing users
3. **Pattern Detection** - Monitor for suspicious activity (too fast, too many, etc.)
4. **Risk Scoring** - Combine signals into risk score
5. **Automated Actions** - Block obvious fraud, flag borderline cases
6. **Manual Review** - Queue suspicious accounts for human check
7. **Learning Loop** - Update patterns based on confirmed fraud

## What kind of information this concept outputs or relays
- Duplicate probability percentage
- List of potentially linked accounts
- Suspicious activity flags with reasons
- Risk score (0-100)
- Recommended actions (allow/review/block)
- Pattern match details
- Manual review queue entries

## Good expected outcome of realizing this concept
The system prevents 90% of duplicate accounts and catches 75% of fraudulent behavior. False positive rate stays below 2%. Manual review queue remains manageable (< 50 per day). The focused approach provides strong ROI on implementation effort. Platform maintains reputation for authenticity. Architecture allows smooth addition of advanced fraud detection.

## Bad unwanted outcome of realizing this concept
Sophisticated fraudsters easily bypass the basic checks. False positives frustrate legitimate users, especially from certain ethnicities where face matching performs poorly. Manual review becomes overwhelming as platform grows. Pattern detection creates arms race with fraudsters. Privacy concerns arise from biometric storage. The basic system provides false confidence while fraud continues.