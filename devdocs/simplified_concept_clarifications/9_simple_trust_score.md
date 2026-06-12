# filepath: devdocs/simplified_concept_clarifications/9_simple_trust_score.md

# Simple Trust Score

## What it is and why it matters
A three-component scoring system combining verification tier (40%), task success rate (40%), and account age (20%) into a single 0-100 score. This simplified calculation maintains the trust score architecture while being transparent and easy to understand.

## How this concept helps the overall project
- **Clear incentives** - Users understand exactly how to improve score
- **Easy calculation** - No black box algorithm concerns
- **Fair weighting** - Balances identity, performance, and loyalty
- **Quick implementation** - Simple formula with no ML required
- **Extensible design** - Can add components without restructuring

## How this concept limits the overall project
- **Less nuanced** - Misses subtle trust indicators
- **Gaming potential** - Simple formula easier to manipulate
- **No adaptability** - Fixed weights don't adjust to user types
- **Limited factors** - Only three inputs may be insufficient
- **Slow changes** - Account age component changes gradually

## What kind of information this concept needs as input
- User's current verification tier (0-3)
- Total tasks attempted and successfully completed
- Account creation date
- Any platform violations or flags
- Current score for change tracking

## What kind of process this concept should use
1. **Component Calculation** - Tier: 0=0pts, 1=10pts, 2=25pts, 3=40pts
2. **Success Rate** - (Completed/Attempted) × 40 points
3. **Account Age** - Min(months/12, 1) × 20 points
4. **Penalty Application** - Subtract points for violations
5. **Score Summation** - Add components for 0-100 score
6. **Change Tracking** - Store score history
7. **Display Logic** - Show score and breakdown to users

## What kind of information this concept outputs or relays
- Overall trust score (0-100)
- Component breakdown showing points from each factor
- Score change from last calculation
- Percentile ranking among all users
- Suggestions for improvement
- Score impact preview for actions
- Historical score graph

## Good expected outcome of realizing this concept
Users actively work to improve their scores, driving platform quality up. The transparent calculation builds trust in the system. New users see clear path to higher scores. The simple formula performs well even with millions of users. Scores effectively predict user reliability. The system requires minimal maintenance while providing valuable differentiation.

## Bad unwanted outcome of realizing this concept
Users focus obsessively on gaming the score rather than quality. The simple formula fails to catch sophisticated bad actors. Account age component frustrates new quality performers. Fixed weights prove inappropriate for different user segments. Score becomes meaningless as everyone optimizes for it. The simplified approach can't evolve to handle emerging trust issues.