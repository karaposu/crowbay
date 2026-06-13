# filepath: known_requirements.md

# Crowd - Known Requirements

## Functional Requirements

### User Management
- **Multi-tier user system**: Posters and Performers
- **Identity verification**: Multi-layer verification process for Performers
  - Phone number verification
  - Email verification
  - Advanced verification for specific demographics (e.g., diploma verification for "university graduate" filter)
- **User profiles** with demographic information
- **Authentication system** with JWT tokens
- **Password reset functionality**

### Task Management
- **Natural language task creation** via Telegram bot
- **Task specification** including:
  - Description of desired action
  - Target platform/URL
  - Budget allocation
  - Number of participants needed
  - Timeline for completion
  - Demographic filters
- **Task matching** based on performer demographics
- **Task acceptance** with heavy CAPTCHA verification
- **Task status tracking** (pending, in progress, completed, disputed)

### Demographic Filtering System
- **Location-based filtering** (country, city, region)
- **Age range filtering**
- **Education level filtering**
- **Occupation/job type filtering**
- **Interest-based filtering**
- **Political view filtering** (where legally permissible)
- **Custom criteria support**

### Payment System
- **Cryptocurrency wallet integration** (USDT, PEPE)
- **Automated wallet generation** for each task
- **Escrow system** - funds held until task completion
- **Commission calculation** (1-10% platform fee)
- **Withdrawal functionality** for Performers
- **Transaction history** and tracking
- **Balance management** for both Posters and Performers

### Verification System
- **Screen recording upload** functionality
- **AI-powered video analysis** to verify:
  - Task was actually performed
  - Correct profile/page was visited
  - Required actions were taken
  - Time spent on task meets requirements
- **Automated approval/rejection** based on AI analysis
- **Manual review option** for disputed tasks

### Communication System
- **Telegram bot integration** as primary interface
- **Natural language processing** for task creation
- **Notification system** for:
  - New tasks matching performer criteria
  - Task acceptance confirmations
  - Payment confirmations
  - Verification results

## Technical Requirements

### Platform Architecture
- **RESTful API** built with FastAPI
- **SQLite database** for development (PostgreSQL for production)
- **JWT-based authentication**
- **Modular service architecture**

### Security Requirements
- **Encrypted data storage** for sensitive information
- **Secure cryptocurrency transactions**
- **CAPTCHA integration** to prevent bot signups
- **Rate limiting** to prevent abuse
- **Secure screen recording upload** with size limits
- **Privacy protection** for both Posters and Performers

### Performance Requirements
- **Scalable video processing** for AI verification
- **Quick task matching** algorithm
- **Fast payment processing**
- **Efficient notification delivery**
- **Responsive Telegram bot** interactions

### Integration Requirements
- **Telegram Bot API** integration
- **Cryptocurrency payment gateway** integration
- **AI/ML service** for video analysis
- **Cloud storage** for screen recordings
- **Email service** for notifications

## Business Requirements

### Pricing Model
- **Transparent commission structure**: 1-10% of task value
- **No hidden fees**
- **Clear pricing display** before task creation
- **Flexible budget options** for task creators

### Quality Assurance
- **Reputation system** for Performers (future implementation)
- **Task completion quality metrics**
- **Dispute resolution process**
- **Refund mechanism** for unsatisfactory work

### Compliance Requirements
- **KYC (Know Your Customer)** for certain transaction thresholds
- **Data protection compliance** (GDPR where applicable)
- **Terms of Service** and **Privacy Policy**
- **Age verification** (18+ requirement)
- **Geographic restrictions** where necessary

## User Experience Requirements

### Telegram Bot Interface
- **Conversational UI** for natural interaction
- **Clear command structure** with help documentation
- **Progress indicators** for multi-step processes
- **Error handling** with helpful messages
- **Multi-language support** (future)

### Task Creation Flow
- **Intuitive task description** process
- **Budget recommendation** based on task complexity
- **Filter preview** showing potential performer pool
- **Confirmation summary** before payment

### Task Performance Flow
- **Easy task browsing** based on performer profile
- **Clear task requirements** display
- **Simple acceptance process**
- **Straightforward recording upload**
- **Payment tracking** visibility

## Future Requirements (Identified but Not Yet Implemented)

### Platform Expansion
- **Multi-platform support** (TikTok, YouTube, Twitter, LinkedIn)
- **Dedicated mobile applications** (iOS and Android)
- **Web portal** for advanced features
- **API access** for programmatic task creation

### Advanced Features
- **Batch task creation** for campaigns
- **Task templates** for recurring needs
- **Advanced analytics** and reporting
- **A/B testing support** for marketing campaigns
- **Team accounts** for agencies

### AGI Integration
- **Public API** for non-human intelligence access
- **Special verification** for AGI-created tasks
- **Ethical guidelines** for AGI use cases
- **Rate limiting** for automated task creation

### Enhanced Verification
- **Biometric verification** options
- **Behavioral analysis** for quality assurance
- **Fraud detection** systems
- **Continuous verification** improvements

## Constraints and Limitations

### Current Limitations
- **Telegram-only interface** (no web/mobile app yet)
- **Limited to supported cryptocurrencies**
- **Manual aspects** in verification process
- **Geographic limitations** for certain features
- **Language support** (initially English only)

### Technical Constraints
- **Video file size limits** for uploads
- **Processing time** for AI verification
- **Cryptocurrency transaction fees**
- **Platform scaling limitations**

### Legal Constraints
- **Compliance with platform ToS** (tasks cannot violate target platform rules)
- **Geographic restrictions** in certain jurisdictions
- **Cryptocurrency regulations** varying by country
- **Data retention requirements**