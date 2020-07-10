import sys, os
import json, urllib3, argparse, datetime
from splunk import get_results
from utils import send_email


def main():
    """
    Usage:
    export FROMEMAIL='xxxxx@xxxxxxx.com'
    export SENDGRID_API_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    python positka.py --ip 3.86.128.32 --username admin --password xxxxx --email xxxx@xxxxx.com --query 'index="_internal" | head 1000' --earliest_time '2020-07-01 12:03:30' --latest_time '2020-07-10 12:03:30'
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    p = argparse.ArgumentParser(description="splunk: query results")
    p.add_argument("--username", "--username", required=True, help="username")
    p.add_argument("--ip", "--ip", required=True, help="server ip address")
    p.add_argument("--password", "--password", required=True, help="password")
    p.add_argument(
        "--earliest_time",
        "--earliest_time",
        required=True,
        help="earliest time, format: 2020-07-10 12:03:30",
    )
    p.add_argument(
        "--latest_time",
        "--latest_time",
        required=True,
        help="latest time, format: 2020-07-10 12:03:30",
    )
    p.add_argument(
        "--email", "--email", required=True, help="email addr to send results"
    )
    p.add_argument("--query", "--query", required=True, help="query string")
    args = p.parse_args()

    # query search results
    base_url = "https://%s:8089" % args.ip
    earliest_time = int(
        datetime.datetime.strptime(args.earliest_time, "%Y-%m-%d %H:%M:%S").timestamp()
    )
    latest_time = int(
        datetime.datetime.strptime(args.latest_time, "%Y-%m-%d %H:%M:%S").timestamp()
    )
    results = get_results(base_url, args.query, earliest_time, latest_time)
    with open("results.json", "w") as f:
        json.dump(results, f)

    # email sending
    sub = "Splunk Query Results"
    content = "Query: %s" % args.query
    attachment = "results.json"
    sg_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("FROMEMAIL")
    if sg_key and from_email:
        send_email(from_email, args.email, attachment, sub, content, sg_key)


main()
