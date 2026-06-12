# filepath: progressive_verification.md

# Progressive Verification System

## Overview

Crowd implements a multi-tier progressive verification system that balances user privacy with platform trust. Users verify only what's needed for their desired tasks, creating a flexible system that grows with user engagement.

## Core Principles

1. **Verify Only When Needed**: Users aren't forced to complete all verification levels upfront
2. **Task-Driven Requirements**: Verification requirements are determined by task specifications
3. **Privacy by Design**: Users control their data; verification details are encrypted and isolated
4. **Cross-Validation**: Multiple data points validate each other to prevent fraud
5. **Progressive Benefits**: Higher verification tiers unlock better opportunities and may unlock better pay

## Verification Tiers

### Tier 0: Basic Registration (Required)
**Purpose**: Establish basic account security and communication
- Email address (with validation)
- Phone number (with SMS verification)
- Username and secure password
- Terms of Service acceptance
- Basic CAPTCHA completion

**Unlocks**: 
- Browse available tasks
- View platform statistics
- Access to help/support

### Tier 1: Demographics (Performer Requirement)
**Purpose**: Enable basic demographic filtering
- Full legal name
- Birth date
- Gender
- Country of residence
- City/Region
- Preferred language(s)
- Timezone

**Unlocks**:
- Accept basic tasks (no demographic requirements)
- Appear in general performer pool
- Basic earnings capability

### Tier 2: Identity Verification
**Purpose**: Confirm real human identity and prevent duplicate accounts
- Government-issued ID upload (passport, driver's license, national ID)
- Live selfie with liveness detection
- Facial recognition matching between ID and selfie
- Address verification (utility bill or bank statement)

**Cross-Validation**:
- Name matches Tier 1 data
- Birth date matches ID
- Gender presentation matches declared gender
- Location matches declared country/city

**Unlocks**:
- Higher-value tasks
- Tasks requiring "verified humans only"
- Increased daily task limits
- Priority task notifications

### Tier 3: Socioeconomic Profile
**Purpose**: Enable precise demographic targeting for specialized campaigns
- Current occupation/job title
- Employment status (employed, student, retired, etc.)
- Education level completed
- Field of study/work
- Marital status
- Number of children
- Household income bracket (optional)
- Interests and hobbies

**Unlocks**:
- Demographic-specific tasks (e.g., "parents only", "IT professionals")
- Premium task access
- Specialized campaign participation

### Tier 4: Digital Footprint Verification
**Purpose**: Verify social media presence and enable platform-specific tasks
- Social media account linking:
  - Instagram (username, follower count, account age)
  - LinkedIn (profile completeness, connections)
  - TikTok (username, follower count, engagement rate)
  - X/Twitter (username, followers, account age)
  - Reddit (karma score, account age)
  - Threads (profile verification)
  - Bluesky (handle verification)
- Account ownership verification (OAuth where possible)
- Activity level assessment
- Authenticity score calculation

**Cross-Validation**:
- Profile photos match verified selfie
- Name consistency across platforms
- Age/location consistency

**Unlocks**:
- Platform-specific engagement tasks
- Influencer-tier tasks
- Multi-platform campaign participation
- Higher commission rates

### Tier 5: Specialized Credentials
**Purpose**: Verify specific qualifications for high-value specialized tasks
- Educational credentials:
  - Diploma/degree certificate upload
  - University email verification (.edu)
  - Transcript verification (optional)
- Professional certifications
- Skill-specific proofs
- Language proficiency certificates
- Special qualifications

**Unlocks**:
- Highest-paying specialized tasks
- Professional opinion tasks
- Educational content creation
- Expert review opportunities

## Implementation Details

### Verification States

```python
class VerificationState(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"
```

### User Verification Model

```python
class UserVerification:
    user_id: str
    tier_0: TierZeroData  # Always required
    tier_1: Optional[TierOneData]
    tier_2: Optional[TierTwoData]
    tier_3: Optional[TierThreeData]
    tier_4: Optional[TierFourData]
    tier_5: Optional[TierFiveData]
    
    verification_scores: Dict[str, float]
    cross_validation_results: Dict[str, bool]
    last_updated: datetime
    next_reverification: datetime
```

### Task Requirement Specification

When posters create tasks, they specify required verification levels:

```python
class TaskRequirements:
    minimum_tier: int  # Minimum verification tier required
    required_fields: List[str]  # Specific fields that must be verified
    preferred_demographics: Dict[str, Any]  # Filtering criteria
    
    # Example:
    # {
    #     "minimum_tier": 2,
    #     "required_fields": ["education_level", "location"],
    #     "preferred_demographics": {
    #         "education_level": "bachelors_or_higher",
    #         "location": {"country": "US", "city": "New York"},
    #         "age_range": {"min": 25, "max": 35}
    #     }
    # }
```

### Verification Flow

1. **Prompted Verification**: When a performer tries to accept a task requiring higher verification
2. **Voluntary Verification**: Performers can proactively verify to access better tasks
3. **Bulk Verification**: Complete multiple tiers in one session for convenience

### Privacy and Security

1. **Data Encryption**: All verification documents encrypted at rest
2. **Access Control**: Verification data accessible only to:
   - The user themselves
   - Automated verification systems
   - Manual review team (when necessary)
3. **Data Minimization**: Posters see only aggregate matches, not individual profiles
4. **Right to Deletion**: Users can request removal of verification data
5. **Audit Trail**: All access to verification data is logged

### Cross-Validation Matrix

| Data Point | Validated Against | Tier |
|------------|------------------|------|
| Birth Date | Government ID | 2 |
| Gender | Selfie + ID | 2 |
| Name | ID + Social Media | 2,4 |
| Location | ID + Utility Bill | 2 |
| Education | Diploma + LinkedIn | 5,4 |
| Employment | LinkedIn + Verification | 3,4 |

### Verification Expiry and Maintenance

- **Tier 0-1**: No expiry
- **Tier 2**: Reverify every 2 years
- **Tier 3**: Update annually
- **Tier 4**: Continuous monitoring
- **Tier 5**: Depends on credential type

### Benefits by Tier

| Tier | Task Access | Daily Limit | Commission Rate | Special Features |
|------|------------|-------------|-----------------|------------------|
| 0 | Browse only | 0 | N/A | Platform access |
| 1 | Basic tasks | 5 | Standard | Task notifications |
| 2 | Verified tasks | 20 | Standard | Priority queue |
| 3 | Demographic tasks | 50 | +5% bonus | Campaign access |
| 4 | Platform tasks | 100 | +10% bonus | Influencer perks |
| 5 | Specialized | Unlimited | +15% bonus | Expert status |

## Task Visibility Settings

When creating a task, posters can configure visibility options:

### Visibility Modes

1. **Exclusive Mode**: Task visible only to performers who meet ALL requirements
   - Ensures only qualified performers see the task
   - Reduces noise and irrelevant applications
   - Best for urgent or specialized tasks

2. **Inclusive Mode** (Recommended): Task visible to all, but clearly marked with requirements
   - Unqualified performers see the task but cannot apply
   - Shows required verifications needed to unlock the task
   - Creates "verification incentive" - performers are motivated to complete verifications
   - Displays: "Complete Tier 3 verification to unlock this $50 task"

3. **Hybrid Mode**: Visible to partially qualified performers
   - Shows to performers meeting some but not all requirements
   - Indicates which specific verifications are missing
   - Allows performers to plan their verification journey

### Example Task Display for Unqualified Performers

```
┌─────────────────────────────────────┐
│ 🔒 Premium Task - $50               │
│ "Review our tech product"           │
│                                     │
│ Requirements not met:               │
│ ❌ Tier 3: Job verification needed  │
│ ❌ Must verify: IT Professional     │
│ ✅ Location: New York (verified)    │
│                                     │
│ [Complete Verification to Unlock]   │
└─────────────────────────────────────┘
```

## Task Matching Algorithm

When a poster creates a task with specific requirements:

1. **Query Verification Database**: Find all performers meeting minimum tier
2. **Apply Required Fields Filter**: Check specific verified fields
3. **Apply Demographic Filters**: Match preferred demographics
4. **Calculate Match Score**: Weight by verification completeness
5. **Apply Visibility Settings**: Determine who can see vs. who can apply
6. **Return Statistics**: Show poster both qualified and potential performer counts

## Fraud Prevention

1. **Duplicate Detection**: Biometric matching prevents multiple accounts
2. **Cross-Validation Failures**: Automatic flag for manual review
3. **Behavioral Analysis**: Unusual verification patterns trigger reviews
4. **Document Authentication**: AI-powered document verification
5. **Periodic Reverification**: Ensure continued validity

## User Experience

### For Performers

1. **Dashboard View**: Clear visualization of verification status
2. **Guided Process**: Step-by-step verification with progress tracking
3. **Benefit Preview**: Show what tasks become available at each tier
4. **Privacy Controls**: Choose what data to share and when

### For Posters

1. **Audience Calculator**: Real-time count of matching performers
2. **Verification Requirements Builder**: Intuitive interface to set requirements
3. **Cost Estimator**: Show how requirements affect performer pool and costs
4. **Quality Indicators**: See average verification level of matching performers

## Future Enhancements

1. **Blockchain Verification**: Immutable verification records
2. **Third-Party Integration**: Connect with external verification services
3. **Reputation Score**: Combine verification with performance history
4. **Regional Adaptations**: Country-specific verification methods
5. **AI-Powered Fraud Detection**: Advanced pattern recognition

## Compliance Considerations

1. **GDPR Compliance**: Right to access, correct, and delete data
2. **KYC Requirements**: Meet financial regulations for high-value transactions
3. **Age Verification**: Ensure all performers are 18+
4. **Data Localization**: Store data according to regional requirements
5. **Audit Readiness**: Maintain logs for regulatory review