# GA4 API Data Extraction with Python

## Overview
This script extracts data from the Google Analytics 4 (GA4) API using the [Google Analytics Data API (v1beta)](https://developers.google.com/analytics/devguides/reporting/data/v1/basics). It allows for dynamic querying of dimensions, metrics, filters, and ordering, handling pagination efficiently to retrieve large datasets.

## Features
- Establishes a secure connection using a service account.
- Dynamically constructs API requests with flexible dimensions, metrics, and filters.
- Handles pagination to fetch complete datasets.
- Converts API responses into a structured Pandas DataFrame for further analysis.

## Requirements
### Python Packages:
Ensure you have the required dependencies installed:
```sh
pip install google-analytics-data pandas google-auth
```

### Service Account Credentials:
- You need a Google service account with access to your GA4 property.
- Download the JSON key file and specify its path in the script.

## Usage
1. **Set Up Credentials:**
   - Replace `"credentials.json"` with the path to your service account key file.
   - Replace `"YOUR-GA4-PROPERTY-ID"` with your GA4 property ID.

2. **Modify Query Parameters:**
   - Adjust `dimensions`, `metrics`, `dimensions_filter`, and `order_bys` as needed.

3. **Run the Script:**
   ```sh
   python script.py
   ```

4. **Output:**
   - The extracted data is stored in a Pandas DataFrame (`df`) for further analysis.

## Example Configuration
```python
start_date = "30daysAgo"
end_date = "today"
dimensions = ["date", "firstUserCampaignName"]
dimensions_filter = {"continent": ["Europe"]}
metrics = ["sessions", "totalUsers"]
order_bys = []
```

## Error Handling
- The script includes exception handling for connection failures and API errors.
- If an error occurs during data retrieval, it provides meaningful error messages.

## Notes
- The script uses `MAX_ROWS_PER_REQUEST = 100000` to optimize pagination.
- Modify the request parameters as needed for different GA4 reporting requirements.

## License
This script is provided under the MIT License.
