# Task Verification Logic

## What it is and why it matters
Task Verification Logic matches the observed actions from LLM analysis against the required task steps to determine if the task was completed successfully. It supports three core task types (social engagement, form submission, navigation) with clear pass/fail outcomes. It matters because this transforms raw observations into actionable verification decisions that determine payment.

## How this concept helps the overall project
- **Clear Decisions**: Binary pass/fail removes ambiguity
- **Task Support**: Covers most common crowdsourcing tasks
- **Extensibility**: Architecture supports adding task types
- **Automation**: No human review needed for clear cases
- **Consistency**: Same criteria applied to all verifications

## How this concept limits the overall project
- **Binary Outcomes**: No partial credit or quality scoring
- **Limited Tasks**: Only 3 task types initially supported
- **Rigid Matching**: May reject valid alternative completion paths
- **No Confidence**: Can't express uncertainty about edge cases
- **Manual Updates**: New platforms require code changes

## What kind of information this concept needs as input
- LLM analysis results (detected actions and UI states)
- Task specification with required steps
- Task type category (social/form/navigation)
- Expected outcomes and success criteria
- Optional elements vs mandatory elements

## What kind of process this concept should use
1. **Task Type Router**: Direct to appropriate verification logic
2. **Social Engagement Tasks**:
   - Check: Profile/content found?
   - Check: Interaction performed (like/follow/share)?
   - Check: Confirmation visible (heart filled, following status)?
3. **Form Submission Tasks**:
   - Check: Form fields identified?
   - Check: Required fields filled?
   - Check: Submit action detected?
   - Check: Success confirmation shown?
4. **Navigation Tasks**:
   - Check: Starting point reached?
   - Check: Target destination reached?
   - Check: Required pages visited in sequence?
5. **Result Determination**: All required checks passed = PASS, else FAIL

## What kind of information this concept outputs or relays
- Verification status (PASS/FAIL)
- Completed steps checklist
- Missing or failed steps
- Timestamp of completion (if passed)
- Reason for failure (if failed)
- Evidence references (frame numbers)

## Good expected outcome of realizing this concept
The system correctly verifies 95% of properly completed tasks and rejects 98% of incomplete attempts. Verification logic is transparent and explicable. Adding new task patterns within the three categories is straightforward. False positives are extremely rare, maintaining platform trust.

## Bad unwanted outcome of realizing this concept
Rigid logic rejects valid task completions that took unexpected paths. Binary decisions force rejection of 95% complete tasks. The system can't distinguish between minor issues and complete failure. New platform updates break verification logic. Users game the system by learning exact requirements.