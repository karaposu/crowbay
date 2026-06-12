# Simplified Core Concepts for Prototype

## 1. Smart Frame Extraction
Adaptive video sampling using OpenCV scene detection and basic event expectations to minimize LLM calls.
   - Focus on scene change detection only (no complex event scripts initially)
   - Fixed sampling rates based on detected activity levels

## 2. Batch LLM Analysis
Efficient processing of extracted frames through vision models with task-aware prompting.
   - Single LLM provider (GPT-4V)
   - Basic batch processing (5 frames per call)

## 3. Task Verification Logic
Simple matching of observed actions against required task steps with binary outcomes.
   - Support for 3 task types: social engagement, form submission, navigation
   - Pass/fail determination without confidence scoring

## 4. Evidence Collection
Capture key screenshots and extracted text as proof of task completion.
   - Store 3-5 key frames per verification
   - Basic text extraction from identified moments

## 5. REST API Interface
Simple HTTP endpoint for submitting videos and retrieving verification results.
   - Synchronous processing for videos under 2 minutes
   - Basic status polling for longer videos