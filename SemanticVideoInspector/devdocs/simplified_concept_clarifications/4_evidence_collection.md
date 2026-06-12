# Evidence Collection

## What it is and why it matters
Evidence Collection captures and stores 3-5 key screenshots and any extracted text that proves task completion. These artifacts serve as an audit trail for disputes and quality reviews. It matters because stakeholders need concrete proof beyond just a "passed" status - they need to see what was actually done.

## How this concept helps the overall project
- **Trust Building**: Provides visual proof of task completion
- **Dispute Resolution**: Evidence resolves disagreements objectively
- **Quality Control**: Enables spot-checks of verification accuracy
- **Learning**: Collected evidence improves future verification
- **Compliance**: Maintains audit trail for platform requirements

## How this concept limits the overall project
- **Storage Costs**: Screenshots require significant space
- **Privacy Risk**: May capture sensitive information
- **Limited Evidence**: Only 3-5 frames might miss context
- **Processing Time**: Selecting best frames adds latency
- **Retention Policy**: Must balance storage vs availability

## What kind of information this concept needs as input
- All analyzed frames with their descriptions
- Task verification results (which steps completed)
- LLM-identified key moments
- Extracted text content
- Timestamps for each frame

## What kind of process this concept should use
1. **Key Moment Selection**:
   - Frame showing initial state
   - Frame showing main action (click, type, etc.)
   - Frame showing result/confirmation
   - Any frame with important text
2. **Screenshot Optimization**:
   - Compress images to ~200KB each
   - Maintain readability of text
   - Add timestamp overlay
3. **Text Extraction**:
   - Collect all entered text (comments, forms)
   - Extract usernames and profile names
   - Capture confirmation messages
4. **Evidence Package Creation**:
   - Bundle screenshots in chronological order
   - Include extracted text as JSON
   - Add verification summary
5. **Storage**: Save package with 30-day retention

## What kind of information this concept outputs or relays
- Evidence package (ZIP file or folder)
- 3-5 key screenshots with timestamps
- Extracted text document (JSON)
- Verification summary (1-page PDF)
- Package URL for retrieval
- Storage expiration date

## Good expected outcome of realizing this concept
Every verification includes perfectly selected screenshots that clearly show task initiation, execution, and completion. Evidence packages are under 1MB, load quickly, and convince reviewers immediately. Text extraction captures all relevant data. The evidence is so clear that disputes drop by 90%.

## Bad unwanted outcome of realizing this concept
Poor frame selection misses the actual moment of task completion. Screenshots are blurry or text is unreadable after compression. Sensitive information like passwords or payment details gets captured. Storage fills up quickly with redundant evidence. Evidence doesn't actually prove what the verification claimed.