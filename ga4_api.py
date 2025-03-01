from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import Filter, FilterExpression, FilterExpressionList, OrderBy, RunReportRequest
from google.oauth2 import service_account
import pandas as pd

MAX_ROWS_PER_REQUEST: int = 100000  # Maximum rows per API request


def establish_connection(secrets: str) -> BetaAnalyticsDataClient:
    """Establishes a connection to the GA4 API using service account credentials."""
    try:
        credentials = service_account.Credentials.from_service_account_file(secrets)
        client = BetaAnalyticsDataClient(credentials=credentials)
        return client
    except Exception as e:
        raise RuntimeError(f"Failed to establish a connection: {e}")


def create_request(property_id: str, start_date: str, end_date: str, dimensions: list = None,
                   dimensions_filter: dict = None, metrics: list = None, order_bys: list = None,
                   offset=0, limit=100000) -> RunReportRequest:
    """Constructs a RunReportRequest object with the provided parameters."""
    request_dict = {
        "property": f"properties/{property_id}",
        "date_ranges": [{"start_date": start_date, "end_date": end_date}],
        "dimensions": [{"name": dim} for dim in (dimensions or [])],
        "metrics": [{"name": metric} for metric in (metrics or [])],
        "keep_empty_rows": True,
        "offset": offset,
        "limit": limit
    }

    # Apply optional dimension filters if provided
    if dimensions_filter:
        request_dict["dimension_filter"] = FilterExpression(
            and_group=FilterExpressionList(expressions=dimension_filtering(dimensions_filter))
        )

    # Apply optional ordering if provided
    if order_bys:
        request_dict["order_bys"] = [OrderBy(dimension={"dimension_name": ord}) for ord in (order_bys or [])]

    return RunReportRequest(**request_dict)


def dimension_filtering(dimensions_filter: list) -> list:
    """Creates filter expressions based on the provided dimension filters."""
    filter_expressions = []

    for dimension, values in dimensions_filter.items():
        if isinstance(values, list):  # Use "in list" filter for multiple values
            filter_expressions.append(FilterExpression(
                filter=Filter(
                    field_name=dimension,
                    in_list_filter=Filter.InListFilter(values=values)
                )
            ))
        elif isinstance(values, str):  # Use "contains" filter for single string value
            filter_expressions.append(FilterExpression(
                filter=Filter(
                    field_name=dimension,
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                        value=values
                    )
                )
            ))

    return filter_expressions


def run_paginated_request(client: BetaAnalyticsDataClient, property_id: str, start_date: str, end_date: str,
                          dimensions: list = None, dimensions_filter: dict = None,
                          metrics: list = None, order_bys: list = None) -> list:
    """Executes paginated requests to fetch all data from the GA4 API."""
    all_rows = []
    offset = 0

    while True:
        request = create_request(property_id, start_date, end_date, dimensions, dimensions_filter,
                                 metrics, order_bys, offset=offset, limit=MAX_ROWS_PER_REQUEST)
        try:
            response = client.run_report(request)

            if not response.rows:
                break  # Stop if there are no more rows to fetch

            all_rows.extend(response.rows)  # Append fetched rows
            offset += MAX_ROWS_PER_REQUEST  # Increase offset for next batch

        except Exception as e:
            raise RuntimeError(f"Failed to run request at offset {offset}: {e}")

    return all_rows


def convert_response_to_dataframe(all_data: list, dimensions: list, metrics: list) -> pd.DataFrame:
    """Converts the API response into a Pandas DataFrame."""
    try:
        data = [
            {dimensions[i]: row.dimension_values[i].value for i in range(len(dimensions))}
            | {metrics[i]: row.metric_values[i].value for i in range(len(metrics))}
            for row in all_data
        ]
        return pd.DataFrame(data)
    except Exception as e:
        raise RuntimeError(f"Failed to convert response to DataFrame: {e}")


if __name__ == "__main__":
    # CONNECTION TO GA4 API --------------------------------------------------------------------------------------------
    secrets = "credentials.json"  # Path to service account credentials
    property_id = "YOUR-GA4-PROPERTY-ID"
    client = establish_connection(secrets)

    # VARIABLES --------------------------------------------------------------------------------------------------------
    start_date = "30daysAgo"
    end_date = "today"
    dimensions = ["date", "firstUserCampaignName", "firstUserDefaultChannelGroup", "firstUserGoogleAdsAdGroupName",
                  "firstUserGoogleAdsAdNetworkType", "firstUserSourceMedium", "firstUserSourcePlatform"]
    dimensions_filter = {
        "continent": ["Europe"]
    }
    metrics = ["averageSessionDuration", "engagedSessions", "eventCount", "keyEvents", "newUsers", "screenPageViews",
               "sessions", "totalUsers", "userEngagementDuration"]
    order_bys = []

    # EXECUTION --------------------------------------------------------------------------------------------------------
    all_data = run_paginated_request(client, property_id,
                                     start_date, end_date, dimensions, dimensions_filter, metrics, order_bys)
    df = convert_response_to_dataframe(all_data, dimensions, metrics)
    df.to_csv("ga4_data.csv", index=False)
