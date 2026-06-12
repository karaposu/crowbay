# Smart Frame Extraction

## What it is and why it matters
Smart Frame Extraction uses OpenCV to detect scene changes and visual transitions, then applies adaptive sampling rates to extract the most relevant frames from videos. This reduces LLM API costs by 80% while ensuring critical moments aren't missed. It matters because blind sampling either wastes money on redundant frames or misses important actions.

## How this concept helps the overall project
- **Cost Efficiency**: Reduces frame count from hundreds to dozens per video
- **Performance**: Faster processing by analyzing fewer frames
- **Accuracy**: Focuses on moments of change where actions occur
- **Scalability**: Makes processing longer videos economically viable
- **Foundation**: Provides clean input for all downstream analysis

## How this concept limits the overall project
- **Missed Moments**: Risk of not capturing brief actions between samples
- **Tuning Required**: Different apps need different detection thresholds
- **Processing Overhead**: OpenCV analysis adds 5-10 seconds upfront
- **Memory Usage**: Must buffer frames for comparison
- **Platform Variance**: UI animations can trigger false positives

## What kind of information this concept needs as input
- Video file (MP4, WebM, MOV)
- Task type hint ("social media", "form filling", "navigation")
- Platform identifier (Instagram, TikTok, website)
- Maximum frame budget (e.g., 50 frames max)

## What kind of process this concept should use
1. **OpenCV Scene Detection**: Detect transitions using frame differencing and SSIM
2. **Segment Classification**: Label segments as transitions, scrolls, or static
3. **Activity-Based Sampling**:
   - Transitions: 3 fps for 2 seconds around change
   - Scrolling: 1 fps during scroll
   - Static: 0.2 fps or skip entirely
4. **Frame Selection**: Choose clearest frame from each sampling window
5. **Output Preparation**: Convert to optimal format for LLM processing

## What kind of information this concept outputs or relays
- Array of extracted frames with timestamps
- Segment map showing video structure
- Total frames extracted vs video duration
- Activity timeline (when changes occurred)
- Estimated LLM processing cost

## Good expected outcome of realizing this concept
The system extracts 30-40 frames from a 3-minute video, perfectly capturing every page change, button click, and form submission. OpenCV correctly identifies 95% of scene changes without false positives from ads or animations. Processing cost stays under $0.05 per video while maintaining high verification accuracy.

## Bad unwanted outcome of realizing this concept
Over-aggressive filtering misses critical quick actions like double-taps or rapid navigation. OpenCV gets confused by platform-specific animations and either over-samples or under-samples. The system becomes too rigid, requiring manual threshold adjustments for each new platform or app update.