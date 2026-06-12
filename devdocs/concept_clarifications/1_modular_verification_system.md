# filepath: devdocs/concept_clarifications/1_modular_verification_system.md

# Modular Verification System

## What it is and why it matters
A flexible verification framework where users complete independent verification modules (identity, social media, education, employment) in any order based on their needs. Each module unlocks specific task types without artificial tier progression, allowing users to verify only what's relevant while maintaining the architecture to derive tier systems from usage data later.

## How this concept helps the overall project
- **User autonomy** - Performers choose verifications based on tasks they want
- **Precise targeting** - Posters specify exact verification requirements
- **Reduced friction** - No forced progression through irrelevant verifications
- **Data-driven evolution** - Can derive optimal tier systems from actual usage
- **Platform differentiation** - More flexible than rigid tier-based competitors

## How this concept limits the overall project
- **Complex UI/UX** - Many verification options can overwhelm users
- **No instant trust signal** - Can't quickly assess overall verification level
- **Harder pricing models** - Can't easily tier commission rates
- **Missing gamification** - No clear progression path for motivation
- **Poster complexity** - Must understand and select from many options

## What kind of information this concept needs as input
- Basic: Email, phone number
- Identity: Government ID, selfie/video
- Social Media: Account credentials, OAuth tokens
- Education: Diploma, transcripts, certificates
- Employment: Work ID, pay stubs, LinkedIn
- Platform data: Follower counts, engagement rates
- User consent for each verification type

## What kind of process this concept should use
1. **Module catalog** - Present available verification modules
2. **User selection** - Let users choose based on task availability
3. **Independent processing** - Each module verified separately
4. **Continuous state** - Users can verify more modules anytime
5. **Requirement matching** - Tasks specify required modules
6. **Visibility control** - Show tasks based on completed modules
7. **Future tier derivation** - Analyze patterns to create tier systems

## What kind of information this concept outputs or relays
- Module verification status (per module)
- Extracted data (demographics, follower counts, etc.)
- Task eligibility based on verifications
- Missing modules for locked tasks
- Verification timestamps and expiry
- Module-specific metadata
- Aggregate verification completeness
- Future tier assignments (when implemented)

## Good expected outcome of realizing this concept
The platform launches with maximum flexibility, attracting diverse users who appreciate the freedom to verify only what they need. Rich data accumulates showing which module combinations are most valuable. Future tier systems are perfectly aligned with actual usage. Posters get precise targeting while performers maintain control. The system scales elegantly as new verification types are added.

## Bad unwanted outcome of realizing this concept
Analysis paralysis prevents users from starting verification. Posters create overly complex requirements that few can meet. The lack of clear progression reduces user engagement. Competitors with simple tier systems appear more professional. The flexibility becomes technical debt when trying to standardize. Support burden increases as users struggle to understand which verifications they need.