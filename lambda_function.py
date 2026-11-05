import json
import boto3
from datetime import datetime, timezone

ssm = boto3.client("ssm")

def get_param(name):
    response = ssm.get_parameter(Name=name)
    return response["Parameter"]["Value"]


def get_stats():
    db_host = get_param("/grocerymate/db_host")
    db_name = get_param("/grocerymate/db_name")
    db_user = get_param("/grocerymate/db_user")
    print(f"Konfiguration geladen: host={db_host}, db={db_name}, user={db_user}")
    return {
        "total_users": 100,
        "total_list_items": 20,
        "db_status": "simuliert",
        "db_name": db_name,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }
    try:
        stats = get_stats()
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(stats)
        }
    except Exception as e:
        print(f"Fehler: {e}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "Statistiken konnten nicht geladen werden"})
        }

if __name__ == "__main__":
    print(lambda_handler({}, None))
