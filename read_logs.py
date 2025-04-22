import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import argparse

TABLE_NAME = "VisitorCounter"

def read_logs(limit=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    try:
        response = table.scan()
        items = response.get("Items", [])

        # Filter out the main counter
        logs = [item for item in items if not item["id"].startswith("visitor_count")]

        # Sort by timestamp
        logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        if limit:
            logs = logs[:limit]

        print(f"\n📝 Found {len(logs)} visitor log entries:\n")
        for entry in logs:
            ip = entry.get("ip", "unknown")
            ts = entry.get("timestamp", "unknown")
            ua = entry.get("user_agent", "unknown")[:60]  # Truncate for readability
            print(f"📍 {ip} @ {ts}\n    {ua}\n")

    except ClientError as e:
        print(f"Error reading from DynamoDB: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read visitor logs from DynamoDB.")
    parser.add_argument("--limit", type=int, help="Number of most recent logs to display")
    args = parser.parse_args()

    read_logs(limit=args.limit)
