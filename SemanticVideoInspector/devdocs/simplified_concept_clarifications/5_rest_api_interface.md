# REST API Interface

## What it is and why it matters
REST API Interface provides a simple HTTP endpoint for submitting videos and retrieving verification results. It handles videos under 2 minutes synchronously and longer videos asynchronously with status polling. It matters because this is the integration point with the Crowd platform, and poor API design would make the system unusable.

## How this concept helps the overall project
- **Simple Integration**: Standard REST patterns familiar to developers
- **Quick Start**: Minimal setup required to begin using
- **Flexibility**: Supports both sync and async patterns
- **Monitoring**: Easy to track usage and performance
- **Debugging**: Clear error messages and status codes

## How this concept limits the overall project
- **No Real-time**: Can't stream results as processing happens
- **Polling Overhead**: Clients must repeatedly check status
- **File Size Limits**: HTTP constraints on video uploads
- **Timeout Issues**: Long processing may hit gateway timeouts
- **No Batch Support**: Each video requires separate request

## What kind of information this concept needs as input
- Video file or URL to video
- Task specification (JSON format)
- API key for authentication
- Task type (social/form/navigation)
- Optional callback URL for async results

## What kind of process this concept should use
1. **Request Handling**:
   ```
   POST /verify
   Headers: 
     - Authorization: Bearer {api_key}
     - Content-Type: multipart/form-data
   Body:
     - video: file or URL
     - task_spec: JSON specification
     - task_type: "social_engagement"
   ```

2. **Synchronous Path** (< 2 min videos):
   - Validate request and auth
   - Process video immediately
   - Return results in response (30-60 seconds)

3. **Asynchronous Path** (>= 2 min videos):
   - Return job ID immediately
   - Process in background
   - Client polls: GET /verify/{job_id}/status

4. **Response Format**:
   ```json
   {
     "status": "completed",
     "result": "PASS",
     "evidence_url": "https://...",
     "completed_steps": [...],
     "processing_time": 45.2
   }
   ```

5. **Error Handling**: Clear HTTP status codes and error messages

## What kind of information this concept outputs or relays
- Job ID for tracking (async mode)
- Verification result (PASS/FAIL)
- Evidence package URL
- Processing time and cost
- Error details if failed
- Rate limit headers

## Good expected outcome of realizing this concept
The API handles hundreds of concurrent requests smoothly. Short videos return results in under 60 seconds. Long videos process reliably with clear status updates. Integration takes developers less than an hour. Error messages are actionable. The system maintains 99.9% uptime.

## Bad unwanted outcome of realizing this concept
Synchronous requests timeout before completion. Polling creates unnecessary server load. Large video uploads fail mysteriously. Status endpoints return inconsistent information. Authentication is confusing or broken. The API becomes a bottleneck preventing system scaling.