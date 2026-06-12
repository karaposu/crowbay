# Frame Extraction Pipeline

## What is this concept and why does it matter?
The Frame Extraction Pipeline is an intelligent system that samples frames from video files at optimal intervals, balancing between capturing all important moments and minimizing processing costs. It matters because sending every frame to an LLM would be prohibitively expensive and slow, while random sampling might miss critical task completion moments.

## How does this concept help the overall project?
- **Cost Optimization**: Reduces LLM API calls by 90-95% compared to analyzing every frame
- **Performance**: Enables processing of longer videos within reasonable time constraints
- **Accuracy**: Focuses analysis on moments of change where actions actually occur
- **Scalability**: Makes it feasible to process hundreds of videos concurrently
- **Flexibility**: Adapts sampling rate based on video content dynamics

## What limitations does this concept introduce?
- **Missed Moments**: Risk of not capturing brief but important actions between samples
- **Complexity**: Requires sophisticated change detection algorithms
- **Processing Overhead**: Initial analysis pass adds latency before LLM processing
- **Storage**: Temporary storage needed for extracted frames
- **Quality Dependency**: Poor video quality affects change detection accuracy

## What inputs does this concept need?
- Video file (MP4, WebM, MOV formats)
- Task type hints (e.g., "form filling" vs "video watching")
- Event expectation script (sequence of expected actions)
- Platform context (Instagram, TikTok, Twitter, etc.)
- Desired confidence level (affects sampling density)
- Maximum frame budget (cost/performance constraint)
- Video metadata (duration, resolution, framerate)

## What process/logic should this concept follow?

### Phase 1: Event Expectation Script Generation
Generate a flexible sequence of expected events based on task requirements:
```
Example for "Like photo on Instagram profile":
1. finds/opens instagram app (allow home screen, app drawer, or already open)
2. navigates to search (via discover, search icon, or profile search)
3. enters search query (typing username)
4. selects profile from results
5. scrolls to find photos section
6. selects a photo
7. performs like action
```

### Phase 2: OpenCV Pre-Processing
1. **Scene Change Detection**:
   - Use frame differencing to detect transitions
   - Apply SSIM for structural similarity analysis  
   - Identify page changes, scrolls, popups, clicks
   - Create video segmentation map

2. **Segment Classification**:
   - Categorize each segment (transition, scroll, static, etc.)
   - Calculate change intensity and duration
   - Extract single key frame per segment for quick LLM tagging

3. **Relevance Filtering**:
   - Quick LLM check: "Is this segment about [expected task]?"
   - Mark segments as relevant/irrelevant/uncertain
   - Skip detailed analysis of irrelevant segments

### Phase 3: Multi-Pass Intelligent Sampling
1. **Scout Pass** (Low Density):
   - Focus only on relevant segments from OpenCV
   - Sample at 0.5 fps to confirm segment boundaries
   - Verify OpenCV classifications with visual inspection

2. **Event Detection Pass**:
   - Use OpenCV boundaries to target analysis
   - Match frames against event expectation script
   - Higher sampling at detected transition points

3. **Focused Extraction** (Variable Density):
   - **Transitions**: 5 fps at change boundaries
   - **Interactions**: 3 fps during clicks/typing
   - **Scrolling**: 1 fps for content scanning
   - **Static**: Skip or minimal sampling

### Phase 4: Adaptive Refinement
- If expected events not found, expand search regions
- Allow for sequence variations (user might search differently)
- Detect alternative paths to same outcome
- Handle interruptions or backtracking in user flow

### Phase 5: Frame Optimization
- Prioritize frames showing UI transitions
- Ensure text is readable (search queries, usernames)
- Capture frames with interactive elements (buttons, forms)
- Include confirmation frames (liked state, success messages)

## What outputs does this concept produce?
- Array of extracted frames with timestamps
- Frame metadata (change score, activity level)
- Sampling report (frames extracted, reason for selection)
- Estimated processing cost based on frame count
- Quality metrics (coverage percentage, confidence level)

## What's the ideal successful outcome?
The pipeline extracts 20-50 frames from a 5-minute video, capturing every significant interaction while skipping redundant static periods. The LLM receives perfectly timed frames showing task initiation, progression, and completion. Processing costs stay under $0.10 per video while maintaining 99% accuracy in capturing important moments.

## What failure modes should we watch for?
- **Over-sampling**: Extracting too many similar frames, wasting API calls
- **Under-sampling**: Missing critical task completion moments
- **Scene Detection Failures**: Misidentifying changes due to video artifacts
- **Memory Overflow**: Too many high-resolution frames in memory
- **Format Issues**: Extracted frames incompatible with LLM requirements
- **Temporal Confusion**: Losing frame ordering or timestamp accuracy