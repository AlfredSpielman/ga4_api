# GA4 Analytics Client

## Overview
This script extracts data from the Google Analytics 4 (GA4) API using the [Google Analytics Data API (v1beta)](https://developers.google.com/analytics/devguides/reporting/data/v1/basics). It allows for dynamic querying of dimensions, metrics, filters, and ordering, handling pagination efficiently to retrieve large datasets.

## Features
- Establishes a secure connection using a service account.
- Dynamically constructs API requests with flexible dimensions, metrics, and filters.
- Handles pagination to fetch complete datasets.
- Converts API responses into a structured Pandas DataFrame for further analysis.

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your credentials:
   - Create a service account in Google Cloud Console
   - Download the JSON credentials file
   - Copy `.env` file and update with your credentials path and GA4 property ID

3. Run the script:
```bash
python ga4_app.py
```

## Usage
```python
from ga4_app import GA4AnalyticsClient

client = GA4AnalyticsClient()

# Get report as DataFrame
df = client.get_report(
    start_date="2025-06-01",
    end_date="yesterday",
    dimensions=["date", "deviceCategory"],
    metrics=["sessions", "users"]
)

# Export to CSV
client.export_report(
    output_path="report.csv",
    start_date="2025-06-01",
    end_date="yesterday",
    dimensions=["date", "deviceCategory"],
    metrics=["sessions", "users"]
)
```

## License
MIT License
