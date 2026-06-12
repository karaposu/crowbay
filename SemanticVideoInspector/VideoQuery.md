# VideoQuery

## What is VideoQuery?

VideoQuery is a smart video search engine that extracts structured information from video content by actively searching for specific events, actions, and UI elements. Instead of analyzing every frame of a video, it intelligently hunts for requested information using computer vision and LLM-powered understanding, returning a time-indexed script of findings.

Think of it as "grep for videos" - you tell it what to look for, and it efficiently finds and extracts those moments with their context.

## How VideoQuery Contributes to SemanticVideoInspector

VideoQuery serves as the **information extraction layer** of SemanticVideoInspector:

1. **Efficient Analysis**: Reduces video processing from blind full-analysis to targeted searching
2. **Cost Optimization**: Cuts LLM API costs by 80-90% through intelligent sampling
3. **Structured Output**: Provides clean, time-indexed data that verification modules can evaluate
4. **Reusable Intelligence**: Separates the "understanding" from the "judging" - VideoQuery understands, other modules verify
5. **Platform Agnostic**: Works with any video content, not tied to specific verification logic

Within SemanticVideoInspector, VideoQuery handles all the "what happened in this video?" questions, while other modules handle "did it meet requirements?"

## What VideoQuery Abstracts Away

VideoQuery hides the complexity of:

- **Frame Extraction Logic**: Automatically handles sampling rates, keyframe selection
- **OpenCV Processing**: Scene detection, motion analysis, change detection
- **LLM Integration**: Batching, prompting, retries, provider management
- **Video Format Handling**: Works with MP4, WebM, MOV without user dealing with codecs
- **Optimization Decisions**: Automatically chooses resolution, compression, sampling density
- **Temporal Correlation**: Links events across time, maintains context between frames
- **Cost Management**: Optimizes frame selection to minimize API calls

Users simply ask "find X in this video" and get structured results.

## What VideoQuery Doesn't Handle

VideoQuery explicitly does NOT:

- **Make Verification Decisions**: Doesn't determine pass/fail
- **Store Videos**: Processes and discards, doesn't maintain video library
- **Real-time Processing**: Not designed for live stream analysis
- **Video Editing**: Read-only analysis, no modification capabilities
- **Audio Analysis**: Currently focuses on visual content only
- **Business Logic**: No knowledge of task requirements or payment rules
- **User Management**: No authentication, authorization, or user tracking
- **Quality Judgments**: Reports what happened, not how well

## Features

### Core Features:
1. **Targeted Search**: Look for specific events/elements instead of analyzing everything
2. **Smart Sampling**: Adaptive frame extraction based on activity levels
3. **Scene Segmentation**: Breaks video into logical chunks using OpenCV
4. **Multi-pass Analysis**: Quick scan → Relevant segment detection → Detailed extraction
5. **Downsampling**: Automatic resolution/framerate optimization
6. **Early Stopping**: Stops processing once all targets found
7. **Batch Processing**: Efficient LLM API usage through frame batching
8. **Text Extraction**: OCR and LLM-based text reading from UI

### Advanced Features:
- **Event Expectation Scripts**: Define flexible sequences of expected actions
- **Alternative Path Recognition**: Handles different ways to complete same action
- **Confidence Scoring**: Reports certainty for each finding
- **Evidence Extraction**: Captures key frames for each discovered event
- **Platform Templates**: Pre-built patterns for common platforms (Instagram, TikTok, etc.)

## Inputs

### Required Inputs:
```python
{
    "video": "path/to/video.mp4",  # or video URL
    "queries": [                    # What to look for
        "Instagram app opening",
        "Searching for username",
        "Profile @specificuser",
        "Like button interaction"
    ]
}
```

### Optional Inputs:
```python
{
    "mode": "targeted",              # "targeted" or "full"
    "platform": "instagram",         # Helps optimize detection
    "max_processing_time": 60,       # Timeout in seconds
    "quality": "balanced",           # "fast", "balanced", "thorough"
    "early_stop": true,             # Stop when all queries found
    "downsample": {
        "resolution": "720p",        # Target resolution
        "fps": 5                     # Max frames per second
    },
    "event_script": {...}           # Expected sequence of events
}
```

## Outputs

### Primary Output - Video Script:
```json
{
    "status": "success",
    "processing_time": 23.5,
    "frames_analyzed": 42,
    "video_duration": 180,
    
    "timeline": [
        {
            "timestamp": "00:00:03",
            "event": "Instagram app opened",
            "confidence": 0.95,
            "frame_number": 90,
            "details": {
                "ui_screen": "Instagram home feed",
                "transition_from": "Phone home screen"
            }
        },
        {
            "timestamp": "00:00:08", 
            "event": "Search initiated",
            "confidence": 0.98,
            "frame_number": 240,
            "details": {
                "action": "Tapped search icon",
                "ui_element": "Bottom navigation bar"
            }
        },
        {
            "timestamp": "00:00:15",
            "event": "Text entered",
            "confidence": 0.92,
            "frame_number": 450,
            "details": {
                "text_entered": "johndoe123",
                "input_field": "Search bar"
            }
        }
    ],
    
    "extracted_data": {
        "text_found": ["johndoe123", "Follow", "Liked"],
        "ui_screens": ["Home", "Search", "Profile", "Photo"],
        "interactions": ["tap", "scroll", "double_tap"],
        "usernames": ["@johndoe123"]
    },
    
    "segments": [
        {
            "start": "00:00:00",
            "end": "00:00:05",
            "type": "app_launch",
            "relevant": true
        },
        {
            "start": "00:00:05",
            "end": "00:00:20",
            "type": "search_interaction",
            "relevant": true
        }
    ],
    
    "queries_found": {
        "Instagram app opening": true,
        "Searching for username": true,
        "Profile @specificuser": true,
        "Like button interaction": false
    }
}
```

### Secondary Outputs:
- **Evidence Package**: Key frames for each found event
- **Processing Metrics**: Frames extracted, API calls made, costs incurred
- **Debug Log**: Detailed processing steps (optional)
- **Confidence Report**: Reliability assessment of findings