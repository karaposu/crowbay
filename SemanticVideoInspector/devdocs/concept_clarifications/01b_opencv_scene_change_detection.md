# OpenCV Scene Change Detection (Sub-concept of Frame Extraction)

## What is this concept and why does it matter?
OpenCV Scene Change Detection uses computer vision algorithms to identify significant visual transitions in videos, such as page changes, app switches, or UI state transitions. By detecting these boundaries computationally before sending frames to LLMs, we can dramatically reduce semantic analysis costs while ensuring we capture all important state changes. This matters because it provides a fast, cheap pre-filter that identifies exactly when things change, allowing targeted LLM analysis only where needed.

## How does this concept help the overall project?
- **Cost Reduction**: 70-90% fewer LLM calls by pre-filtering static periods
- **Transition Precision**: Captures exact moments of UI changes
- **Event Boundaries**: Clearly defines start/end of user actions
- **Speed**: OpenCV processing is 100x faster than LLM analysis
- **Segmentation**: Breaks video into logical chunks for analysis

## What limitations does this concept introduce?
- **False Positives**: Animations or ads might trigger change detection
- **Threshold Tuning**: Different apps need different sensitivity settings
- **Subtle Changes**: Might miss small but important UI updates
- **Processing Pipeline**: Adds another step before LLM analysis
- **Memory Usage**: Requires frame buffering for comparison

## What inputs does this concept need?
- Raw video stream
- Sensitivity thresholds for different change types
- Region of interest masks (optional)
- Platform-specific change patterns
- Minimum change duration (to filter noise)

## What process/logic should this concept follow?

### Detection Pipeline:

#### 1. Frame Difference Calculation
```python
# Pseudo-code for basic detection
def detect_scene_change(frame1, frame2, threshold=30):
    # Convert to grayscale for faster processing
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Calculate absolute difference
    diff = cv2.absdiff(gray1, gray2)
    
    # Apply threshold
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    
    # Calculate percentage of changed pixels
    change_percentage = np.sum(thresh) / thresh.size
    
    return change_percentage > 0.15  # 15% change = scene change
```

#### 2. Advanced Detection Methods
- **Histogram Comparison**: Detect color distribution changes
- **Edge Detection**: Identify structural changes in UI
- **Optical Flow**: Track motion patterns for scrolling/swiping
- **Template Matching**: Detect specific UI elements appearing/disappearing
- **SSIM (Structural Similarity)**: More robust scene comparison

#### 3. Change Classification
```yaml
change_types:
  page_transition:
    characteristics:
      - >80% pixels change
      - Sharp transition (<3 frames)
      - New dominant colors
    action: "Full LLM analysis of new page"
    
  scrolling:
    characteristics:
      - Vertical motion vectors
      - Partial content change
      - Gradual transition
    action: "Sample key frames during scroll"
    
  popup_overlay:
    characteristics:
      - Central region change
      - Background unchanged
      - Sudden appearance
    action: "Analyze popup content"
    
  button_click:
    characteristics:
      - Small region change
      - Color/state change
      - Brief duration
    action: "Capture before/after state"
    
  video_playback:
    characteristics:
      - Continuous small changes
      - Confined to player region
    action: "Skip unless interaction needed"
```

#### 4. Intelligent Segmentation
1. **Detect Boundaries**: Find all scene changes in video
2. **Classify Changes**: Determine type of each transition
3. **Create Segments**: Group frames into logical chunks
4. **Tag Segments**: Quick LLM call to identify what each segment contains
5. **Filter Relevance**: Only fully analyze segments related to task

### Integration with Event Expectation:
```python
def smart_extraction(video, event_script, opencv_segments):
    relevant_segments = []
    
    for segment in opencv_segments:
        # Quick LLM check: "Is this segment about [expected_event]?"
        if is_relevant_to_script(segment.key_frame, event_script):
            relevant_segments.append(segment)
            
    # Dense sampling only in relevant segments
    for segment in relevant_segments:
        if segment.type == "page_transition":
            extract_frames(segment, fps=3)  # High density
        elif segment.type == "scrolling":
            extract_frames(segment, fps=1)  # Medium density
        else:
            extract_frames(segment, fps=0.5)  # Low density
```

## What outputs does this concept produce?
- Segment boundaries with timestamps
- Change type classifications
- Change intensity metrics
- Key frames representing each segment
- Relevance scores for each segment
- Motion vectors and patterns
- Processing time statistics

## What's the ideal successful outcome?
OpenCV detects every significant UI change with 99% accuracy while filtering out irrelevant motion like ads or background animations. A 3-minute video is segmented into 10-15 logical chunks, each tagged with its purpose. Only 3-4 segments require full LLM analysis, reducing costs by 80%. The exact moment of every button click, page load, and form submission is captured. The system adapts to different apps and UI styles automatically.

## What failure modes should we watch for?
- **Over-segmentation**: Too many tiny segments from noise
- **Under-segmentation**: Missing important subtle changes
- **Animation Confusion**: Treating decorative animations as scene changes
- **Threshold Brittleness**: Settings too specific to one app version
- **Region Blindness**: Missing changes in unexpected screen areas
- **Performance Degradation**: OpenCV processing becoming a bottleneck