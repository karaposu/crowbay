# filepath: devdocs/simplified_concept_clarifications/6_filter_based_task_matching.md

# Filter-Based Task Matching

## What it is and why it matters
Simple SQL queries that match tasks to performers based on verification tier requirements and demographic filters. No scoring, ranking, or algorithms - just binary matches where performers either qualify or don't. This provides basic but functional task distribution.

## How this concept helps the overall project
- **Dead simple implementation** - Basic WHERE clauses in SQL
- **Completely transparent** - Users understand exactly why they match or don't
- **Fast execution** - Simple queries perform well
- **Easy debugging** - No complex logic to trace
- **Predictable results** - Same filters always yield same matches

## How this concept limits the overall project
- **No optimization** - Can't prioritize better performers
- **Binary matching** - No partial matches or "close enough"
- **Potential imbalance** - Some performers get many tasks, others none
- **No learning** - System doesn't improve over time
- **Basic distribution** - Can't intelligently spread load

## What kind of information this concept needs as input
- Task requirements (minimum tier, required demographics)
- Performer verification tier
- Performer demographics (location, age, gender, education)
- Performer availability status (not overloaded)
- Task type and platform

## What kind of process this concept should use
1. **Parse Requirements** - Extract tier and demographic requirements from task
2. **Build Query** - Create SQL WHERE clause with AND conditions
3. **Execute Match** - Find all performers meeting ALL requirements
4. **Apply Limits** - Cap results to prevent spam (e.g., first 100 matches)
5. **Random Selection** - If needed, randomly select subset
6. **Send Notifications** - Alert matched performers about task
7. **Track Acceptance** - Monitor who accepts the task

## What kind of information this concept outputs or relays
- List of matching performer IDs
- Total count of matches
- Binary match status (match/no match)
- Missing requirements for non-matches
- Task distribution count
- Zero-match warnings to posters

## Good expected outcome of realizing this concept
Tasks find appropriate performers quickly with simple, understandable logic. Posters see exact match counts before posting. The system handles hundreds of tasks without performance issues. Clear requirements prevent confusion. The simplicity means few bugs and easy maintenance. Basic matching covers 80% of use cases effectively.

## Bad unwanted outcome of realizing this concept
Popular performers get overwhelmed while others sit idle. Binary matching means near-misses get nothing. Posters frustrated by zero matches when filters are too specific. No way to prefer higher quality performers. The rigid system can't adapt to supply/demand imbalances. Lack of intelligence means poor user experience compared to smarter platforms.