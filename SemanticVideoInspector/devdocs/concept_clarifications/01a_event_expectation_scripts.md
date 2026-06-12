# Event Expectation Scripts (Sub-concept of Frame Extraction)

## What is this concept and why does it matter?
Event Expectation Scripts are flexible, human-readable sequences that describe the expected flow of user actions for a given task. They guide the frame extraction process to intelligently sample more densely around moments of interest. This matters because it transforms blind video sampling into targeted event hunting, dramatically improving both efficiency and accuracy.

## How does this concept help the overall project?
- **Smart Sampling**: Focuses computational resources on moments that matter
- **Flexibility**: Allows for human variation in task completion paths
- **Cost Reduction**: Reduces unnecessary frame extraction by 60-80%
- **Better Coverage**: Ensures critical moments aren't missed between samples
- **Context Awareness**: Understands what to look for based on platform and task type

## What limitations does this concept introduce?
- **Script Generation Overhead**: Must create scripts for each task type
- **Over-fitting Risk**: Scripts might be too specific to one path
- **Platform Variations**: Different app versions may break scripts
- **Human Unpredictability**: Users might take completely unexpected paths
- **Maintenance Burden**: Scripts need updates as platforms evolve

## What inputs does this concept need?
- Task description and requirements
- Platform/app identification
- Known UI patterns for the platform
- Common user behavior patterns
- Alternative completion paths
- Required vs optional steps

## What process/logic should this concept follow?

### Script Structure Example:
```yaml
task: "Like Instagram Photo"
platform: "Instagram"
version: "flexible"  # allows variations

expected_sequence:
  - step: "app_launch"
    variations: 
      - "tap instagram icon"
      - "switch from another app"
      - "app already open"
    sampling: "medium"
    
  - step: "navigate_to_search"
    variations:
      - "tap search icon"
      - "tap discover then search"
      - "pull down search"
    sampling: "high"  # important transition
    
  - step: "search_interaction"
    variations:
      - "type username"
      - "select from recent searches"
      - "voice search"
    critical: true  # must capture search query
    sampling: "maximum"
    
  - step: "profile_selection"
    variations:
      - "tap first result"
      - "scroll and select"
    sampling: "high"
    
  - step: "find_content"
    variations:
      - "already visible"
      - "scroll to photos"
      - "switch from reels to posts"
    sampling: "medium"
    
  - step: "like_action"
    variations:
      - "double tap photo"
      - "tap heart icon"
    critical: true
    sampling: "maximum"
    confirmation_needed: true  # verify liked state

parallel_indicators:
  - "notification popup"  # might appear anytime
  - "connection error"     # could interrupt flow
  - "ad display"          # might need to skip

timing_hints:
  app_launch: "0-5 seconds"
  search_interaction: "5-20 seconds"
  like_action: "15-60 seconds"
```

### Script Generation Process:
1. **Task Analysis**: Break down task into atomic actions
2. **Platform Research**: Understand UI patterns and common flows
3. **Variation Mapping**: Document alternative paths
4. **Critical Point Identification**: Mark must-capture moments
5. **Timing Estimation**: Add expected time windows
6. **Flexibility Rules**: Define acceptable deviations

### Script Execution:
1. **Lookahead Matching**: Predict upcoming events based on current state
2. **Sampling Adjustment**: Increase/decrease fps based on proximity to expected events
3. **Variation Tolerance**: Accept any documented variation as valid
4. **Recovery Logic**: If script diverges, attempt to re-sync with expected flow

## What outputs does this concept produce?
- Structured event expectation script (YAML/JSON)
- Sampling density map for video timeline
- Predicted event windows with confidence
- Alternative path documentation
- Critical moment flags for must-capture events
- Deviation report when actual differs from expected

## What's the ideal successful outcome?
The script accurately predicts 80% of user action sequences while remaining flexible enough to handle the other 20% of variations. Frame extraction becomes so efficient that a 3-minute video only needs 30-40 carefully chosen frames instead of 180 frames at 1fps. Critical moments like button clicks and form submissions are never missed. The system adapts when users take unexpected but valid paths.

## What failure modes should we watch for?
- **Rigid Scripts**: Rejecting valid but unexpected completion paths
- **Script Explosion**: Too many variations making scripts unmaintainable
- **Timing Misalignment**: Events happening outside expected windows
- **Platform Drift**: UI updates invalidating scripts
- **Over-sampling**: Scripts causing unnecessary frame extraction
- **Critical Miss**: Failing to capture essential moments despite script guidance