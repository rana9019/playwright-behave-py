# Test Automation Framework with Playwright & Behave

A comprehensive test automation framework using Playwright and Behave (Cucumber for Python) with integrated dashboarding, ML-based failure analysis, and advanced reporting capabilities for web application testing.

##  Features

- **Cross-browser UI Testing** with Playwright
- **Behavior-Driven Development (BDD)** using Gherkin syntax
- **Interactive Dashboards** for test result visualization
- **ML-based Failure Analysis** for pattern detection
- **Excel Integration** for comprehensive reporting
- **Page Object Model** for maintainable test code
- **Modular Architecture** with organized feature domains

##  Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

##  Installation & Setup

### 1. Clone and Setup Project
```bash
git clone <your-repository-url>
cd playwright-behave-py
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install
```

### 5. Environment Configuration
Configure the `.env` file in the `config/` folder:
```env
BASE_URL=http://localhost:3000
USERNAME=testuser
PASSWORD=securepassword123
```

##  Project Structure

```
playwright-behave-py/
├── .idea/                          # IDE configuration
├── .venv/                          # Python virtual environment
├── config/                         # Configuration files
│   └── .env                       # Environment variables
├── features/                       # Gherkin feature files
│   ├── alerts/
│   │   └── alerts.feature
│   ├── dositrace/
│   │   └── dositrace.feature
│   ├── exams/
│   │   └── exams.feature
│   ├── login/
│   │   └── login.feature
│   ├── nrd_nri/
│   │   └── nrd_nri.feature
│   ├── patients/
│   │   └── patients.feature
│   ├── protocoles_dositrace/
│   │   └── protocoles_dositrace.feature
│   ├── rapport/
│   │   └── rapport.feature
│   ├── risk_patient/
│   │   └── risk_patient.feature
│   ├── statistique/
│   │   └── statistique.feature
│   └── worklist/
│       └── worklist.feature
├── pages/                          # Page Object Model classes
│   ├── alerts_page.py
│   ├── dositrace_page.py
│   ├── exams_page.py
│   ├── login_page.py
│   ├── nrd_nri_page.py
│   ├── patients_page.py
│   ├── protocoles_dositrace_page.py
│   ├── rapport_page.py
│   ├── risk_patient_page.py
│   ├── statistique_page.py
│   └── worklist_page.py
├── reports/                        # Test execution reports
│   ├── cucumber_report.json       # Cucumber JSON report
│   └── test_results.db           # Additional test data
├── steps/                          # Step definition implementations
│   ├── alerts_steps.py
│   ├── dositrace_steps.py
│   ├── exams_steps.py
│   ├── login_steps.py
│   ├── nrd_nri_steps.py
│   ├── patients_steps.py
│   ├── protocoles_dositrace_steps.py
│   ├── rapport_steps.py
│   ├── risk_patient_steps.py
│   ├── statistique_steps.py
│   └── worklist_steps.py
├── utils/                          # Utility functions and tools
│   ├── analyze_failures.py         # ML-based failure analysis
│   ├── db_migration.py            # Database migration utilities
│   ├── excel_updater.py           # Excel reporting functionality
│   ├── init_db.py                 # Database initialization
│   └── playwright_dashboard.py    # Interactive test dashboard
├── cucumber_tests.db          # Test results database
├── environment.py                 # Test environment setup/teardown
├── readme.md                      # This file
└── requirements.txt               # Python dependencies
```

## ️ Running Tests

### Execute All Tests
```bash
behave
```

### Run Specific Feature
```bash
behave features/login/login.feature
```

### Run Tests with Tags
```bash
behave --tags=@smoke
behave --tags=@login
```

### Run Tests with Specific Browser
```bash
behave -D browser=chrome
behave -D browser=firefox
```

##  Reporting & Analysis

### 1. Interactive Dashboard
Launch the Streamlit dashboard to visualize test results:
```bash
streamlit run utils/playwright_dashboard.py -- --file reports/cucumber_report.json
```

Features:
- Overall test metrics and pass rates
- Feature-level performance analysis
- Test execution time trends
- Interactive filtering and sorting
- Visual status distribution

### 2. ML-Based Failure Analysis
Analyze test failures using machine learning techniques:
```bash
python utils/analyze_failures.py --file reports/cucumber_report.json
```

Capabilities:
- Error classification and clustering
- Pattern detection in failure messages
- Failure trend visualization
- Resolution recommendations

### 3. Excel Reports
Generate comprehensive Excel reports:
```bash
python utils/excel_updater.py
```

##  Test Domains

The framework supports testing across multiple application domains:

- **Authentication & Login** - User authentication workflows
- **Patient Management** - Patient record operations
- **Alerts System** - Alert handling and notifications
- **Dose Tracking (Dositrace)** - Radiation dose monitoring
- **Examinations** - Medical examination workflows
- **Protocols** - Protocol creation and management
- **Risk Assessment** - Patient risk evaluation
- **Reports** - Report generation and viewing
- **Statistics** - Statistical analysis features
- **Worklist Management** - Task and workflow management
- **NRD/NRI** - Nuclear medicine workflows

##  Configuration

### Environment Variables
Configure the following variables in your `config/.env` file:

```env
WEB_URL=http://localhost:3000      # Application base URL
WEB_USERNAME=testuser                   # Test user credentials
WEB_PASSWORD=securepassword123          # Test user password
```

##  Adding New Tests

### 1. Create Feature File
Add a new `.feature` file in the appropriate domain folder:
```gherkin
Feature: New Feature Name
  
  Scenario: Test scenario description
    Given I navigate to the application
    When I perform some action
    Then I should see expected result
```

### 2. Implement Step Definitions
Create corresponding step definitions in the `steps/` folder:
```python
from behave import given, when, then

@given('I navigate to the application')
def step_impl(context):
    context.page.goto(context.base_url)

@when('I perform some action')
def step_impl(context):
    # Implementation here
    pass

@then('I should see expected result')
def step_impl(context):
    # Assertion here
    pass
```

### 3. Create Page Object (if needed)
Add page objects in the `pages/` folder:
```python
class NewPage:
    def __init__(self, page):
        self.page = page
        self.selector = 'css-selector'
    
    def perform_action(self):
        self.page.click(self.selector)
```

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

##  Best Practices

- Follow the Page Object Model pattern
- Use descriptive scenario names in Gherkin
- Implement proper wait strategies
- Add appropriate assertions
- Use tags for test organization
- Keep step definitions reusable
- Document complex test scenarios

##  Troubleshooting

### Common Issues

**Tests failing to start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Playwright browsers are installed: `playwright install`

**Browser launch issues:**
- Check if the browser is specified correctly in configuration
- Try running in headless mode first

**Element not found errors:**
- Verify selectors are correct and up-to-date
- Implement proper wait strategies
- Check for dynamic content loading

## Dependencies

Core dependencies include:
- `playwright` - Browser automation
- `behave` - BDD testing framework
- `streamlit` - Dashboard creation
- `plotly` - Data visualization
- `scikit-learn` - Machine learning analysis
- `openpyxl` - Excel file manipulation
- `python-dotenv` - Environment variable management

See `requirements.txt` for the complete list.# playwright-behave-py
# playwright-behave-py
# playwright-cucumber-py
# playwright-behave-py
# playwright-behave-py
# playwright-behave-py
# playwright-behave-py
# playwright-behave-py
# playwright-behave-py
# playwright-behave-py
